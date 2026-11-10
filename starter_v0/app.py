from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version
from chat import (
    ROOT,
    ARTIFACTS_DIR,
    now_iso,
    safe_slug,
    trim_history,
    run_model_tool_loop,
    write_transcript,
)

# Load environment variables
load_lab_env(ROOT)

st.set_page_config(
    page_title="Research Agent UI | Nhóm 456",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔬 Research Agent Tool & Evaluation Dashboard")
st.caption("AI20k Day 03 Lab — Interactive Multi-turn Tool-calling Research Agent")

# Sidebar Configuration
st.sidebar.header("⚙️ Cấu hình Agent")

provider_choice = st.sidebar.selectbox(
    "Provider",
    options=["gemini", "openrouter", "openai", "anthropic", "ollama"],
    index=0,
    help="Provider LLM dùng để sinh tool call và câu trả lời",
)

model_override = st.sidebar.text_input(
    "Model (để trống nếu dùng mặc định)",
    value="",
    placeholder="e.g. gemini-2.5-flash hoặc meta-llama/llama-3.3-70b-instruct",
)

version_choice = st.sidebar.selectbox(
    "Artifact Version",
    options=["v3", "v2", "v1", "v0"],
    index=0,
    help="Phiên bản prompt và tool declarations",
)

max_tool_rounds = st.sidebar.slider(
    "Max Tool Rounds",
    min_value=1,
    max_value=8,
    value=4,
    help="Số vòng lặp tối đa model được gọi tool trước khi dừng",
)

history_window = st.sidebar.slider(
    "History Window (turns)",
    min_value=1,
    max_value=10,
    value=5,
    help="Số lượt hội thoại gần nhất đưa vào context",
)

# Prompt & Tool Paths
system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
tools_path = ARTIFACTS_DIR / "tools.yaml"
transcripts_dir = ROOT / "transcripts"
transcripts_dir.mkdir(parents=True, exist_ok=True)

# Build Artifact Version
try:
    artifact_version = build_artifact_version(version_choice, system_prompt_path, tools_path)
    system_prompt = system_prompt_path.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(tools_path)
    openai_tools = to_openai_tools(tool_declarations)
except Exception as exc:
    st.sidebar.error(f"Lỗi load artifact: {exc}")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.subheader("📋 Phiên làm việc (Session)")

# Initialize session state
if "transcript" not in st.session_state or st.sidebar.button("🔄 Bắt đầu phiên mới (Reset Session)"):
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([
        safe_slug(version_choice),
        safe_slug(provider_choice),
        timestamp,
    ])
    transcript_file = transcripts_dir / f"{transcript_id}.transcript.json"

    st.session_state.transcript_id = transcript_id
    st.session_state.transcript_file = transcript_file
    st.session_state.messages = []  # For UI display
    st.session_state.chat_history = []  # For model memory
    st.session_state.turn_index = 0
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_choice,
        "model": model_override or "default",
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }

st.sidebar.code(f"ID: {st.session_state.transcript_id}\nLượt chat: {st.session_state.turn_index}", language="text")

# Quick prompt buttons in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("💡 Câu hỏi mẫu (Showdown Quick Prompts)")
sample_prompts = [
    ("🔍 Research tin tức", "Tìm tin tức mới nhất về DeepSeek-V3 trên mạng xã hội hôm nay."),
    ("❓ Thiếu thông tin (Clarify)", "Hãy tóm tắt bài báo này giúp tôi."),
    ("📢 Gửi Telegram (Cần xác nhận)", "Gửi bản tóm tắt nghiên cứu mới nhất lên kênh Telegram của nhóm."),
    ("📜 Tra cứu Policy", "Quy định công ty về việc sử dụng AI trong nghiên cứu là gì?"),
]

for label, prompt_text in sample_prompts:
    if st.sidebar.button(label, key=f"sample_{label}"):
        st.session_state.pending_prompt = prompt_text

# Display Chat Messages
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg.get("content", "")
    with st.chat_message(role):
        if role == "assistant" and msg.get("tool_events"):
            with st.status("🔧 Tool Execution Log", expanded=False, state="complete"):
                for event in msg["tool_events"]:
                    st.markdown(f"**Tool:** `{event.get('tool')}`")
                    st.json({"args": event.get("args"), "result": event.get("result")})
        st.markdown(content)

# Input handling
user_input = st.chat_input("Nhập câu hỏi hoặc yêu cầu cho Research Agent...")

# Handle pending prompt from sample buttons if any
if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_input:
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Prepare Agent Execution
    st.session_state.turn_index += 1
    turn_record: dict[str, Any] = {
        "turn_index": st.session_state.turn_index,
        "started_at": now_iso(),
        "user": user_input,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    messages_for_model = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.chat_history, history_window),
        {"role": "user", "content": user_input},
    ]

    with st.chat_message("assistant"):
        tool_status_container = st.status("Đang suy luận và chọn tool...", expanded=True)
        try:
            provider = make_provider(provider_choice)
            selected_model = model_override.strip() or getattr(provider, "default_model", None)

            result = run_model_tool_loop(
                provider=provider,
                messages=messages_for_model,
                tools=openai_tools,
                model=selected_model,
                max_tool_rounds=max_tool_rounds,
            )

            turn_record.update(result)
            assistant_text = result.get("assistant_text", "")
            tool_events = result.get("tool_events", [])

            # Update status container
            if tool_events:
                tool_status_container.update(
                    label=f"Đã thực thi {len(tool_events)} tool call(s)",
                    state="complete",
                    expanded=False,
                )
                with tool_status_container:
                    for ev in tool_events:
                        st.markdown(f"**Tool:** `{ev.get('tool')}`")
                        st.json({"args": ev.get("args"), "result": ev.get("result")})
            else:
                tool_status_container.update(label="Trả lời trực tiếp (không gọi tool)", state="complete", expanded=False)

            st.markdown(assistant_text)

            # Update session messages
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_text,
                "tool_events": tool_events,
            })
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})

        except Exception as exc:
            error_msg = f"{type(exc).__name__}: {str(exc)}"
            tool_status_container.update(label="Lỗi thực thi", state="error")
            st.error(error_msg)
            turn_record.update({
                "status": "provider_error",
                "error": error_msg,
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ Có lỗi xảy ra: {error_msg}",
            })

        turn_record["ended_at"] = now_iso()
        st.session_state.transcript["turns"].append(turn_record)
        write_transcript(st.session_state.transcript_file, st.session_state.transcript)
        st.caption(f"💾 Transcript đã lưu tại: `{st.session_state.transcript_file.name}`")


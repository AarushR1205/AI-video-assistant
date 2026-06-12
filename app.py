import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

#         progress_placeholder = st.empty()

#         def update_step(key, state):
#             st.session_state.pipeline_steps[key] = state

#         try:
#             with progress_placeholder.container():
#                 st.info("⚙️ Pipeline running — see sidebar for live status…")

#             update_step("audio", "active")
#             chunks = process_input(source)
#             update_step("audio", "done")

#             update_step("transcript", "active")
#             transcript = transcribe_all(chunks, language)
#             update_step("transcript", "done")

#             update_step("title", "active")
#             title = generate_title(transcript)
#             update_step("title", "done")

#             update_step("summary", "active")
#             summary = summarize(transcript)
#             update_step("summary", "done")

#             update_step("extract", "active")
#             action_items = extract_action_items(transcript)
#             decisions = extract_key_decisions(transcript)
#             questions = extract_questions(transcript)
#             update_step("extract", "done")

#             update_step("rag", "active")
#             rag_chain = build_rag_chain(transcript)
#             update_step("rag", "done")

#             st.session_state.result = {
#                 "title": title,
#                 "transcript": transcript,
#                 "summary": summary,
#                 "action_items": action_items,
#                 "key_decisions": decisions,
#                 "open_questions": questions,
#                 "rag_chain": rag_chain,
#             }
#             st.session_state.pipeline_done = True
#             progress_placeholder.success("✅ Analysis complete!")
#             time.sleep(0.5)
#             progress_placeholder.empty()
#             st.rerun()

#         except Exception as e:
#             for k in ["audio", "transcript", "title", "summary", "extract", "rag"]:
#                 if st.session_state.pipeline_steps.get(k) == "active":
#                     st.session_state.pipeline_steps[k] = "pending"
#             progress_placeholder.error(f"❌ Error: {e}")

# # ── Results ──────────────────────────────────────────────────────────────────────
# if st.session_state.result:
#     r = st.session_state.result

#     # Title banner
#     st.markdown(
#         f"""
#     <div class="card">
#         <div class="card-title">📌 Session Title</div>
#         <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:var(--text)">
#             {r["title"]}
#         </div>
#     </div>""",
#         unsafe_allow_html=True,
#     )

#     # Top row: summary + transcript
#     col1, col2 = st.columns([3, 2], gap="medium")

#     with col1:
#         st.markdown(
#             f"""
#         <div class="card">
#             <div class="card-title">📋 Summary</div>
#             <div class="card-content">{r["summary"]}</div>
#         </div>""",
#             unsafe_allow_html=True,
#         )

#     with col2:
#         with st.expander("📝 Full Transcript", expanded=False):
#             st.markdown(
#                 f'<div class="transcript-box">{r["transcript"]}</div>',
#                 unsafe_allow_html=True,
#             )

#     # Second row: action items | decisions | questions
#     c1, c2, c3 = st.columns(3, gap="medium")

#     with c1:
#         st.markdown(
#             f"""
#         <div class="card">
#             <div class="card-title">✅ Action Items</div>
#             <div class="card-content">{r["action_items"]}</div>
#         </div>""",
#             unsafe_allow_html=True,
#         )

#     with c2:
#         st.markdown(
#             f"""
#         <div class="card">
#             <div class="card-title">🔑 Key Decisions</div>
#             <div class="card-content">{r["key_decisions"]}</div>
#         </div>""",
#             unsafe_allow_html=True,
#         )

#     with c3:
#         st.markdown(
#             f"""
#         <div class="card">
#             <div class="card-title">❓ Open Questions</div>
#             <div class="card-content">{r["open_questions"]}</div>
#         </div>""",
#             unsafe_allow_html=True,
#         )

#     st.markdown("---")

#     # ── RAG Chat ──────────────────────────────────────────────────────────────
#     st.markdown(
#         "<div style=\"font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;margin-bottom:1rem\">💬 Chat with your Meeting</div>",
#         unsafe_allow_html=True,
#     )

#     # Chat history display
#     if st.session_state.chat_history:
#         chat_html = '<div class="chat-container">'
#         for msg in st.session_state.chat_history:
#             if msg["role"] == "user":
#                 chat_html += f"""
#                 <div class="chat-msg" style="align-items:flex-end">
#                     <span class="chat-label user-label">You</span>
#                     <div class="chat-bubble user-bubble">{msg["content"]}</div>
#                 </div>"""
#             else:
#                 chat_html += f"""
#                 <div class="chat-msg" style="align-items:flex-start">
#                     <span class="chat-label bot-label">🤖 Assistant</span>
#                     <div class="chat-bubble bot-bubble">{msg["content"]}</div>
#                 </div>"""
#         chat_html += "</div>"
#         st.markdown(chat_html, unsafe_allow_html=True)
#     else:
#         st.markdown(
#             """
#         <div class="card" style="text-align:center;padding:2rem">
#             <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
#             <div style="color:var(--text-muted);font-size:0.85rem">Ask anything about your meeting transcript</div>
#         </div>""",
#             unsafe_allow_html=True,
#         )

#     # Chat input
#     chat_col1, chat_col2 = st.columns([5, 1], gap="small")
#     with chat_col1:
#         user_input = st.text_input(
#             "Your question",
#             placeholder="What were the main decisions made?",
#             label_visibility="collapsed",
#         )
#     with chat_col2:
#         send_btn = st.button("Send →", use_container_width=True)

#     if send_btn and user_input.strip():
#         with st.spinner("Thinking…"):
#             answer = ask_question(r["rag_chain"], user_input.strip())
#         st.session_state.chat_history.append(
#             {"role": "user", "content": user_input.strip()}
#         )
#         st.session_state.chat_history.append({"role": "assistant", "content": answer})
#         st.rerun()

#     if st.session_state.chat_history:
#         if st.button("🗑️ Clear Chat", type="secondary"):
#             st.session_state.chat_history = []
#             st.rerun()

# else:
#     # Empty state
#     st.markdown(
#         """
#     <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:5rem 2rem;text-align:center">
#         <div style="font-size:4rem;margin-bottom:1rem">🎬</div>
#         <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:var(--text);margin-bottom:0.5rem">
#             Ready to Analyse
#         </div>
#         <div style="color:var(--text-muted);font-size:0.85rem;max-width:380px;line-height:1.7">
#             Paste a YouTube URL or local file path in the sidebar, choose your language, and hit <strong>Analyse</strong> to get started.
#         </div>
#         <div style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center">
#             <span class="badge badge-purple">Transcription</span>
#             <span class="badge badge-cyan">Summarisation</span>
#             <span class="badge badge-green">RAG Chat</span>
#         </div>
#     </div>""",
#         unsafe_allow_html=True,
#     )

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lens — AI Video Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

/* ── Token System ── */
:root {
    --ink:        #0f1117;
    --ink-2:      #2a2d3a;
    --ink-3:      #5a5f72;
    --paper:      #f7f5f0;
    --paper-2:    #eeebe3;
    --paper-3:    #e3dfd5;
    --amber:      #d97706;
    --amber-lt:   #fbbf24;
    --amber-dim:  rgba(217,119,6,0.12);
    --teal:       #0d9488;
    --teal-dim:   rgba(13,148,136,0.1);
    --red:        #dc2626;
    --red-dim:    rgba(220,38,38,0.1);
    --rule:       rgba(15,17,23,0.1);
    --shadow-sm:  0 1px 3px rgba(15,17,23,0.08), 0 1px 2px rgba(15,17,23,0.04);
    --shadow-md:  0 4px 12px rgba(15,17,23,0.1), 0 2px 4px rgba(15,17,23,0.06);
    --radius:     10px;
    --radius-sm:  6px;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--paper) !important;
    color: var(--ink) !important;
}

.stApp {
    background: var(--paper) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--ink) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: var(--paper) !important;
}

[data-testid="stSidebar"] label {
    color: var(--paper-3) !important;
    font-size: 0.72rem !important;
    font-family: 'DM Mono', monospace !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: rgba(247,245,240,0.07) !important;
    border: 1px solid rgba(247,245,240,0.15) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--paper) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
    border-color: var(--amber-lt) !important;
    box-shadow: 0 0 0 2px rgba(251,191,36,0.2) !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(247,245,240,0.07) !important;
    border: 1px solid rgba(247,245,240,0.15) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--paper) !important;
    font-size: 0.85rem !important;
}

/* Sidebar button */
[data-testid="stSidebar"] .stButton > button {
    background: var(--amber) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.65rem 1.2rem !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--amber-lt) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(217,119,6,0.35) !important;
}

/* ── Main area inputs ── */
.stTextInput > div > div > input {
    background: white !important;
    border: 1.5px solid var(--paper-3) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.15s !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 3px var(--amber-dim) !important;
}

/* Main area buttons */
.stButton > button {
    background: var(--ink) !important;
    color: var(--paper) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    background: var(--ink-2) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-md) !important;
}

.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--ink-3) !important;
    border: 1.5px solid var(--paper-3) !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--ink-3) !important;
    color: var(--ink) !important;
    background: transparent !important;
    box-shadow: none !important;
}

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--ink) !important;
}

/* ── Wordmark ── */
.wordmark {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--paper);
    letter-spacing: -0.02em;
    line-height: 1;
}

.wordmark em {
    font-style: italic;
    color: var(--amber-lt);
}

.wordmark-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: rgba(247,245,240,0.35);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Page header ── */
.page-header {
    border-bottom: 1.5px solid var(--rule);
    padding-bottom: 1.25rem;
    margin-bottom: 1.75rem;
}

.page-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--amber);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 400;
    line-height: 1.1;
    color: var(--ink);
    margin: 0 0 0.4rem;
}

.page-desc {
    font-size: 0.9rem;
    color: var(--ink-3);
    font-weight: 300;
    letter-spacing: 0.01em;
}

/* ── Cards ── */
.card {
    background: white;
    border: 1.5px solid var(--paper-3);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.2s, box-shadow 0.2s;
}

.card:hover {
    border-color: var(--paper-3);
    box-shadow: var(--shadow-md);
}

.card-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-3);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.card-eyebrow::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--rule);
}

.card-content {
    font-size: 0.9rem;
    line-height: 1.75;
    color: var(--ink-2);
}

/* Accent cards */
.card-amber { border-left: 3px solid var(--amber); }
.card-teal  { border-left: 3px solid var(--teal);  }
.card-red   { border-left: 3px solid var(--red);   }

/* ── Session title banner ── */
.session-banner {
    background: var(--ink);
    border-radius: var(--radius);
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.session-banner-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
    margin-top: 2px;
}

.session-banner-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--amber-lt);
    margin-bottom: 0.35rem;
}

.session-banner-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    font-weight: 400;
    color: var(--paper);
    line-height: 1.2;
}

/* ── Pill tags ── */
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    font-weight: 500;
    text-transform: uppercase;
}

.pill-amber { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(217,119,6,0.25); }
.pill-teal  { background: var(--teal-dim);  color: var(--teal);  border: 1px solid rgba(13,148,136,0.25); }
.pill-ink   { background: rgba(15,17,23,0.07); color: var(--ink-2); border: 1px solid var(--rule); }

/* ── Pipeline steps (sidebar) ── */
.pipeline-step {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.55rem 0.75rem;
    border-radius: var(--radius-sm);
    margin: 0.25rem 0;
    font-size: 0.8rem;
    color: rgba(247,245,240,0.6);
    transition: background 0.15s;
}

.pipeline-step.done {
    color: rgba(247,245,240,0.9);
    background: rgba(247,245,240,0.05);
}

.pipeline-step.active {
    color: var(--amber-lt);
    background: rgba(251,191,36,0.08);
}

.step-icon {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    flex-shrink: 0;
    border: 1.5px solid rgba(247,245,240,0.15);
    color: rgba(247,245,240,0.3);
    font-family: 'DM Mono', monospace;
    font-weight: 500;
}

.step-icon.done  { background: #10b981; border-color: #10b981; color: white; }
.step-icon.active {
    border-color: var(--amber-lt);
    color: var(--amber-lt);
    animation: spin-ring 1.2s linear infinite;
}

@keyframes spin-ring {
    0%   { box-shadow: 0 0 0 0 rgba(251,191,36,0.5); }
    50%  { box-shadow: 0 0 0 3px rgba(251,191,36,0.15); }
    100% { box-shadow: 0 0 0 0 rgba(251,191,36,0); }
}

/* ── Sidebar divider ── */
.sidebar-rule {
    border: none;
    border-top: 1px solid rgba(247,245,240,0.1);
    margin: 1.1rem 0;
}

/* ── Chat ── */
.chat-wrap {
    background: white;
    border: 1.5px solid var(--paper-3);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    margin-bottom: 0.75rem;
}

.chat-header {
    padding: 0.75rem 1.2rem;
    border-bottom: 1px solid var(--rule);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.chat-header-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--ink-3);
}

.chat-body {
    padding: 1rem 1.2rem;
    max-height: 380px;
    overflow-y: auto;
}

.chat-row {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}

.chat-row-user { align-items: flex-end; }
.chat-row-bot  { align-items: flex-start; }

.chat-sender {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

.chat-sender-user { color: var(--amber); }
.chat-sender-bot  { color: var(--teal); }

.chat-bubble {
    padding: 0.65rem 1rem;
    border-radius: 10px;
    font-size: 0.875rem;
    line-height: 1.65;
    max-width: 88%;
}

.bubble-user {
    background: var(--ink);
    color: var(--paper);
    border-bottom-right-radius: 3px;
}

.bubble-bot {
    background: var(--paper-2);
    color: var(--ink-2);
    border: 1px solid var(--paper-3);
    border-bottom-left-radius: 3px;
}

/* ── Transcript ── */
.transcript-scroll {
    background: var(--paper-2);
    border: 1px solid var(--paper-3);
    border-radius: var(--radius-sm);
    padding: 1.1rem 1.3rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.9;
    max-height: 280px;
    overflow-y: auto;
    color: var(--ink-3);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Empty state ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5rem 2rem;
    text-align: center;
}

.empty-glyph {
    font-family: 'DM Serif Display', serif;
    font-size: 4rem;
    line-height: 1;
    color: var(--paper-3);
    margin-bottom: 1.5rem;
    letter-spacing: -0.05em;
}

.empty-headline {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    color: var(--ink);
    margin-bottom: 0.5rem;
}

.empty-body {
    font-size: 0.875rem;
    color: var(--ink-3);
    max-width: 340px;
    line-height: 1.7;
    font-weight: 300;
}

.empty-pills {
    margin-top: 2rem;
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    justify-content: center;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: var(--ink);
    margin-bottom: 0.9rem;
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
}

.section-heading::after {
    content: '';
    flex: 1;
    height: 1.5px;
    background: var(--rule);
}

/* ── Streamlit overrides ── */
.stProgress > div > div > div { background: var(--amber) !important; }
.stSpinner > div { border-top-color: var(--amber) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--ink-2) !important; }
label { color: var(--ink-3) !important; }

.stExpander {
    border: 1.5px solid var(--paper-3) !important;
    border-radius: var(--radius) !important;
    background: white !important;
    box-shadow: var(--shadow-sm) !important;
}

.stExpander summary {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
    color: var(--ink-2) !important;
}

hr {
    border: none !important;
    border-top: 1.5px solid var(--rule) !important;
    margin: 1.5rem 0 !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--paper-3); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--ink-3); }
</style>
""",
    unsafe_allow_html=True,
)

# ─── Session State Init ──────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ─── Helpers ────────────────────────────────────────────────────────────────────
PIPELINE_STEPS = [
    ("audio", "01", "Audio"),
    ("transcript", "02", "Transcribe"),
    ("title", "03", "Title"),
    ("summary", "04", "Summarise"),
    ("extract", "05", "Extract"),
    ("rag", "06", "Index"),
]


def render_pipeline_sidebar():
    for key, num, label in PIPELINE_STEPS:
        state = st.session_state.pipeline_steps.get(key, "pending")
        step_class = f"pipeline-step {state}"
        icon_class = f"step-icon {state}"
        icon_content = "✓" if state == "done" else ("◌" if state == "active" else num)
        st.markdown(
            f"""
<div class="{step_class}">
    <div class="{icon_class}">{icon_content}</div>
    <span>{label}</span>
</div>""",
            unsafe_allow_html=True,
        )


# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Wordmark
    st.markdown(
        """
<div style="padding: 0.5rem 0 0.25rem;">
    <div class="wordmark">L<em>e</em>ns</div>
    <div class="wordmark-sub">AI Video Assistant</div>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="sidebar-rule">', unsafe_allow_html=True)

    # Input section
    st.markdown(
        "<div style=\"font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.18em;text-transform:uppercase;color:rgba(247,245,240,0.35);margin-bottom:0.6rem;\">Source</div>",
        unsafe_allow_html=True,
    )
    source = st.text_input(
        "YouTube URL or File Path",
        placeholder="youtube.com/watch?v=… or /path/to/file",
        label_visibility="collapsed",
    )
    st.markdown(
        "<div style=\"font-family:'DM Mono',monospace;font-size:0.6rem;color:rgba(247,245,240,0.3);margin:-0.3rem 0 0.75rem;padding-left:2px;\">YouTube URL or local file path</div>",
        unsafe_allow_html=True,
    )

    language = st.selectbox(
        "Language",
        ["english", "hinglish"],
        index=0,
        label_visibility="visible",
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    run_btn = st.button("Analyse →", use_container_width=True)

    # Pipeline status
    if st.session_state.pipeline_done or st.session_state.pipeline_steps:
        st.markdown('<hr class="sidebar-rule">', unsafe_allow_html=True)
        st.markdown(
            "<div style=\"font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.18em;text-transform:uppercase;color:rgba(247,245,240,0.35);margin-bottom:0.4rem;\">Pipeline</div>",
            unsafe_allow_html=True,
        )
        render_pipeline_sidebar()


# ─── Main Area ──────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="page-header">
    <div class="page-eyebrow">◈ Meeting Intelligence</div>
    <div class="page-title">AI Video Assistant</div>
    <div class="page-desc">Paste a source below — get a transcript, summary, and a chat interface in seconds.</div>
</div>""",
    unsafe_allow_html=True,
)

# ── Run Pipeline ────────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Enter a YouTube URL or local file path to continue.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}

        progress_placeholder = st.empty()

        def update_step(key, state):
            st.session_state.pipeline_steps[key] = state

        try:
            with progress_placeholder.container():
                st.info("Pipeline running — watch progress in the sidebar.")

            update_step("audio", "active")
            chunks = process_input(source)
            update_step("audio", "done")

            update_step("transcript", "active")
            transcript = transcribe_all(chunks, language)
            update_step("transcript", "done")

            update_step("title", "active")
            title = generate_title(transcript)
            update_step("title", "done")

            update_step("summary", "active")
            summary = summarize(transcript)
            update_step("summary", "done")

            update_step("extract", "active")
            action_items = extract_action_items(transcript)
            decisions = extract_key_decisions(transcript)
            questions = extract_questions(transcript)
            update_step("extract", "done")

            update_step("rag", "active")
            rag_chain = build_rag_chain(transcript)
            update_step("rag", "done")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            progress_placeholder.success("Done — analysis complete.")
            time.sleep(0.6)
            progress_placeholder.empty()
            st.rerun()

        except Exception as e:
            for k in ["audio", "transcript", "title", "summary", "extract", "rag"]:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_placeholder.error(f"Something went wrong: {e}")


# ── Results ──────────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # ── Session banner ────────────────────────────────────────────────────────
    st.markdown(
        f"""
<div class="session-banner">
    <div class="session-banner-icon">◈</div>
    <div>
        <div class="session-banner-eyebrow">Session</div>
        <div class="session-banner-title">{r["title"]}</div>
    </div>
</div>""",
        unsafe_allow_html=True,
    )

    # ── Summary + Transcript ──────────────────────────────────────────────────
    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        st.markdown(
            f"""
<div class="card">
    <div class="card-eyebrow">Summary</div>
    <div class="card-content">{r["summary"]}</div>
</div>""",
            unsafe_allow_html=True,
        )

    with col2:
        with st.expander("Full Transcript", expanded=False):
            st.markdown(
                f'<div class="transcript-scroll">{r["transcript"]}</div>',
                unsafe_allow_html=True,
            )

    # ── Extraction cards ──────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(
            f"""
<div class="card card-amber">
    <div class="card-eyebrow">✓ Action Items</div>
    <div class="card-content">{r["action_items"]}</div>
</div>""",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
<div class="card card-teal">
    <div class="card-eyebrow">◆ Key Decisions</div>
    <div class="card-content">{r["key_decisions"]}</div>
</div>""",
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
<div class="card card-red">
    <div class="card-eyebrow">? Open Questions</div>
    <div class="card-content">{r["open_questions"]}</div>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-heading">Chat with your meeting</div>',
        unsafe_allow_html=True,
    )

    # ── Chat display ─────────────────────────────────────────────────────────
    if st.session_state.chat_history:
        chat_rows = ""
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_rows += f"""
<div class="chat-row chat-row-user">
    <span class="chat-sender chat-sender-user">You</span>
    <div class="chat-bubble bubble-user">{msg["content"]}</div>
</div>"""
            else:
                chat_rows += f"""
<div class="chat-row chat-row-bot">
    <span class="chat-sender chat-sender-bot">Lens</span>
    <div class="chat-bubble bubble-bot">{msg["content"]}</div>
</div>"""

        st.markdown(
            f"""
<div class="chat-wrap">
    <div class="chat-header">
        <span style="color:var(--amber);font-size:0.75rem;">◈</span>
        <span class="chat-header-label">Conversation</span>
    </div>
    <div class="chat-body">{chat_rows}</div>
</div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
<div class="chat-wrap">
    <div class="chat-header">
        <span style="color:var(--amber);font-size:0.75rem;">◈</span>
        <span class="chat-header-label">Conversation</span>
    </div>
    <div class="chat-body" style="padding:2.5rem 1.2rem;text-align:center;">
        <div style="font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--ink-3);margin-bottom:0.4rem;">No messages yet</div>
        <div style="font-size:0.82rem;color:var(--ink-3);font-weight:300;">Ask anything about your meeting — decisions, tasks, who said what.</div>
    </div>
</div>""",
            unsafe_allow_html=True,
        )

    # ── Chat input ────────────────────────────────────────────────────────────
    inp_col, btn_col = st.columns([6, 1], gap="small")
    with inp_col:
        user_input = st.text_input(
            "Ask a question",
            placeholder="What decisions were made about the roadmap?",
            label_visibility="collapsed",
        )
    with btn_col:
        send_btn = st.button("Send", use_container_width=True)

    if send_btn and user_input.strip():
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], user_input.strip())
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input.strip()}
        )
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear conversation", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

else:
    # ── Empty state ───────────────────────────────────────────────────────────
    st.markdown(
        """
<div class="empty-state">
    <div class="empty-glyph">◈</div>
    <div class="empty-headline">Ready when you are</div>
    <div class="empty-body">
        Paste a YouTube URL or local video path in the sidebar,
        pick a language, and hit <strong>Analyse</strong>.
    </div>
    <div class="empty-pills">
        <span class="pill pill-amber">Transcription</span>
        <span class="pill pill-teal">Summarisation</span>
        <span class="pill pill-ink">RAG Chat</span>
    </div>
</div>""",
        unsafe_allow_html=True,
    )
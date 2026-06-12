# 🎬 AI Video Assistant

> **Transcribe · Summarise · Chat with your meetings**

An intelligent meeting analysis tool that takes any YouTube URL or local video/audio file and runs it through a full AI pipeline — producing a transcript, summary, action items, key decisions, open questions, and an interactive RAG-powered chat interface, all in a sleek Streamlit UI.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔊 **Audio Processing** | Downloads YouTube videos or accepts local files via `yt-dlp` + `pydub`, splitting audio into manageable chunks |
| 📝 **Transcription** | Converts speech to text using OpenAI Whisper (with `faster-whisper` backend); supports **English** and **Hinglish** |
| 🏷️ **Title Generation** | Auto-generates a descriptive session title using Mistral AI via LangChain |
| 📋 **Summarisation** | Produces a concise, structured summary of the meeting content |
| 🔍 **Intelligent Extraction** | Automatically identifies **Action Items**, **Key Decisions**, and **Open Questions** |
| 🧠 **RAG Chat Engine** | Indexes the transcript into ChromaDB with sentence-transformer embeddings, then powers a conversational Q&A interface |
| 🌐 **Multi-language** | Choose between English and Hinglish transcription modes |

---

## 🖼️ App Preview

The app features a dark, modern UI with:

- A live **pipeline status sidebar** showing each processing step in real-time
- A **summary card** alongside a collapsible full transcript viewer
- Three-column layout for **Action Items**, **Key Decisions**, and **Open Questions**
- A **chat interface** to ask natural-language questions about your meeting

---

## 🏗️ Architecture

```
Input (YouTube URL / Local File)
        │
        ▼
┌─────────────────────┐
│  utils/audio_       │  yt-dlp + pydub
│  processor.py       │  → chunked audio
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  core/transcriber   │  OpenAI Whisper / faster-whisper
│  .py                │  → raw transcript text
└─────────┬───────────┘
          │
          ├──────────────────────────────────┐
          ▼                                  ▼
┌─────────────────────┐         ┌────────────────────────┐
│  core/summarizer.py │         │  core/extractor.py     │
│  Title + Summary    │         │  Actions / Decisions / │
│  (Mistral via LC)   │         │  Questions (Mistral)   │
└─────────────────────┘         └────────────────────────┘
          │
          ▼
┌─────────────────────┐
│  core/rag_engine.py │  ChromaDB + sentence-transformers
│  + LangChain RAG    │  → conversational Q&A
└─────────────────────┘
          │
          ▼
    Streamlit UI (app.py)
```

---

## 🛠️ Tech Stack

| Layer | Libraries |
|---|---|
| **UI** | Streamlit, streamlit-extras |
| **Audio** | yt-dlp, pydub, ffmpeg-python, imageio-ffmpeg |
| **Transcription** | openai-whisper, faster-whisper, torch, torchaudio |
| **LLM / Chains** | LangChain, langchain-mistralai, MistralAI |
| **Vector Store** | ChromaDB, langchain-chroma |
| **Embeddings** | sentence-transformers, langchain-huggingface, huggingface-hub |
| **Translation** | deep-translator |
| **Document Parsing** | pypdf, python-docx, unstructured |
| **Utilities** | python-dotenv, pydantic, numpy, tqdm, requests, tiktoken |

---

## ⚡ Quick Start

### Prerequisites

- Python **3.11+**
- [FFmpeg](https://ffmpeg.org/download.html) installed and on your `PATH`
- A **Mistral AI API key** (get one at [console.mistral.ai](https://console.mistral.ai))

### 1. Clone the repository

```bash
git clone https://github.com/AarushR1205/AI-video-assistant.git
cd AI-video-assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using uv (recommended — much faster):**
```bash
pip install uv
uv sync
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 🚀 Usage

1. **Paste a source** — enter a YouTube URL (e.g. `https://youtube.com/watch?v=...`) or a local file path (`.mp4`, `.mkv`, `.mp3`, `.wav`, etc.) in the sidebar.
2. **Select language** — choose `english` or `hinglish` from the dropdown.
3. **Click ⚡ Analyse** — watch the pipeline progress in real-time via the sidebar status indicators.
4. **Explore results** — once complete, the main panel shows:
   - Auto-generated session title
   - Meeting summary
   - Full transcript (expandable)
   - Action items, key decisions, open questions
5. **Chat with your meeting** — ask natural-language questions in the chat box at the bottom (powered by RAG).

---

## 📁 Project Structure

```
AI-video-assistant/
├── app.py                  # Streamlit entry point & UI
├── core/
│   ├── transcriber.py      # Whisper-based audio transcription
│   ├── summarizer.py       # LLM summarisation & title generation
│   ├── extractor.py        # Action items / decisions / questions
│   └── rag_engine.py       # ChromaDB vector store + LangChain RAG
├── utils/
│   └── audio_processor.py  # yt-dlp download + pydub chunking
├── pyproject.toml          # Project metadata & dependencies (uv)
├── requirements.txt        # pip-compatible dependency list
├── .env                    # API keys (not committed)
└── README.md
```

---

## 🔧 Configuration

| Variable | Description | Required |
|---|---|---|
| `MISTRAL_API_KEY` | Your Mistral AI API key for LLM calls | ✅ Yes |

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Aarush Rawat

---

## 🙏 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) for optimised inference
- [LangChain](https://www.langchain.com/) for LLM orchestration
- [Mistral AI](https://mistral.ai/) for the language model
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube audio extraction
- [Streamlit](https://streamlit.io/) for the web interface
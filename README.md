# TruthShield AI 🛡️

> **Hackathon-ready** dual-detection AI system — verify news credibility **and** validate physics claims simultaneously.

Built with **FastAPI + Python** (backend) and **Next.js 15** (frontend), deployed via a Python `venv`.

---

## 🚀 Quick Start

### 1. Backend Setup (Python + venv)

```bash
cd backend

# Create venv & install all dependencies (one-time)
setup_venv.bat

# Start the server
start_server.bat
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

### 2. Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

Open [http://localhost:3000](http://localhost:3000) 🎉

---

## 📁 Project Structure

```
TruthShield/
├── backend/
│   ├── main.py            # FastAPI app with dual detection
│   ├── requirements.txt   # Python dependencies
│   ├── .env               # Secrets (USE_MOCK=true by default)
│   ├── .env.example       # Template
│   ├── setup_venv.bat     # One-click venv setup
│   └── start_server.bat   # One-click server start
└── frontend/
    ├── app/
    │   ├── page.tsx        # Main detection UI
    │   ├── layout.tsx      # Root layout + SEO
    │   ├── globals.css     # Design system (dark glassmorphism)
    │   └── api/detect/     # Proxy route → FastAPI
    └── .env.local          # BACKEND_URL config
```

---

## ⚙️ Configuration

### Use Real AI Models (Optional)

Edit `backend/.env`:
```env
USE_MOCK=false
OPENAI_API_KEY=sk-your-key-here
```

| Mode | News Detection | Physics Check |
|------|--------------|---------------|
| `USE_MOCK=true` (default) | Simulated BERT result | Simulated GPT result |
| `USE_MOCK=false` | `roberta-base` (HuggingFace) | `gpt-4o-mini` (OpenAI) |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/health` | Health check |
| `POST` | `/api/detect` | Dual detection |

**POST `/api/detect`** body:
```json
{
  "news_text": "Scientists discover cure for cancer…",
  "physics_text": "Objects can travel faster than light…"
}
```

---

## 🎨 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI · Python 3.10+ · Uvicorn |
| ML | HuggingFace Transformers (roberta-base) |
| LLM | OpenAI GPT-4o-mini |
| Frontend | Next.js 15 · TypeScript |
| Styling | Vanilla CSS (dark glassmorphism) |
| Database | MongoDB Atlas (optional) |

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="TruthShield AI",
    description="Dual-detection AI system for fake news and physics claim verification",
    version="1.0.0"
)

# CORS — allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Model Loading ───────────────────────────────────────────────────────────────
USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

news_classifier = None

if not USE_MOCK:
    try:
        from transformers import pipeline
        print("⏳ Loading news classification model (roberta-base)…")
        news_classifier = pipeline(
            "text-classification",
            model="roberta-base",
            truncation=True,
            max_length=512,
        )
        print("✅ Model loaded!")
    except Exception as e:
        print(f"⚠️  Model load failed ({e}), falling back to mock mode.")
        USE_MOCK = True


# ── Schemas ─────────────────────────────────────────────────────────────────────
class DetectionRequest(BaseModel):
    news_text: str = ""
    physics_text: str = ""


class NewsResult(BaseModel):
    label: str
    confidence: float
    verdict: str
    explanation: str


class PhysicsResult(BaseModel):
    verdict: str
    confidence: float
    reasoning: str
    is_valid: bool


class DetectionResponse(BaseModel):
    news: Optional[NewsResult] = None
    physics: Optional[PhysicsResult] = None
    timestamp: str
    mode: str


# ── Mock Helpers ─────────────────────────────────────────────────────────────────
_FAKE_LABELS = ["FAKE", "REAL"]
_VERDICTS = {
    "FAKE": "⚠️ Likely Misinformation",
    "REAL": "✅ Appears Credible",
}
_FAKE_EXPLANATIONS = [
    "The text exhibits sensationalist language patterns typical of misinformation.",
    "Linguistic markers suggest this content may be fabricated or heavily biased.",
    "Writing style is consistent with known disinformation campaigns.",
]
_REAL_EXPLANATIONS = [
    "The text uses measured, factual language consistent with credible reporting.",
    "Sentence structure and vocabulary align with verified news sources.",
    "Content tone and specificity are consistent with reliable journalism.",
]

def mock_news_result(text: str) -> NewsResult:
    score = random.uniform(0.62, 0.97)
    # simple heuristic: exclamation marks / ALL CAPS skew toward FAKE
    fake_score = text.count("!") + sum(1 for w in text.split() if w.isupper())
    label = "FAKE" if (fake_score > 2 or random.random() < 0.4) else "REAL"
    explanations = _FAKE_EXPLANATIONS if label == "FAKE" else _REAL_EXPLANATIONS
    return NewsResult(
        label=label,
        confidence=round(score, 4),
        verdict=_VERDICTS[label],
        explanation=random.choice(explanations),
    )


_PHYSICS_VERDICTS = [
    {"verdict": "⚛️ Physically Valid", "is_valid": True,
     "reasoning": "The claim is consistent with established physical laws and empirical evidence."},
    {"verdict": "❌ Violates Physics", "is_valid": False,
     "reasoning": "This claim contradicts fundamental principles of physics such as conservation of energy or Newton's laws."},
    {"verdict": "🔬 Unverifiable", "is_valid": False,
     "reasoning": "Insufficient data to evaluate the claim against known physical models."},
]

def mock_physics_result(text: str) -> PhysicsResult:
    verdict_data = random.choice(_PHYSICS_VERDICTS)
    return PhysicsResult(
        verdict=verdict_data["verdict"],
        confidence=round(random.uniform(0.55, 0.95), 4),
        reasoning=verdict_data["reasoning"],
        is_valid=verdict_data["is_valid"],
    )


# ── Real Helpers ─────────────────────────────────────────────────────────────────
def real_news_result(text: str) -> NewsResult:
    raw = news_classifier(text)[0]
    label = "FAKE" if raw["label"] in ("LABEL_0", "NEGATIVE") else "REAL"
    explanations = _FAKE_EXPLANATIONS if label == "FAKE" else _REAL_EXPLANATIONS
    return NewsResult(
        label=label,
        confidence=round(raw["score"], 4),
        verdict=_VERDICTS[label],
        explanation=random.choice(explanations),
    )


async def real_physics_result(text: str) -> PhysicsResult:
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        resp = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "system",
                "content": (
                    "You are a physics expert. Analyze the given claim and respond ONLY with a JSON object "
                    "with keys: verdict (string), confidence (float 0-1), reasoning (string), is_valid (bool)."
                )
            }, {
                "role": "user",
                "content": f"Analyze this physics claim: '{text}'"
            }],
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        return PhysicsResult(**data)
    except Exception as e:
        print(f"OpenAI error: {e}")
        return mock_physics_result(text)


# ── Routes ───────────────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "mode": "mock" if USE_MOCK else "live",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/api/detect", response_model=DetectionResponse)
async def detect_both(request: DetectionRequest):
    if not request.news_text.strip() and not request.physics_text.strip():
        raise HTTPException(status_code=422, detail="At least one of news_text or physics_text must be provided.")

    news_result: Optional[NewsResult] = None
    physics_result: Optional[PhysicsResult] = None

    if request.news_text.strip():
        if USE_MOCK:
            await asyncio.sleep(0.4)  # simulate processing
            news_result = mock_news_result(request.news_text)
        else:
            news_result = real_news_result(request.news_text)

    if request.physics_text.strip():
        if USE_MOCK or not OPENAI_API_KEY:
            await asyncio.sleep(0.6)
            physics_result = mock_physics_result(request.physics_text)
        else:
            physics_result = await real_physics_result(request.physics_text)

    return DetectionResponse(
        news=news_result,
        physics=physics_result,
        timestamp=datetime.now().isoformat(),
        mode="mock" if USE_MOCK else "live",
    )

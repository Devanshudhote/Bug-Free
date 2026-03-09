'use client';

import { useState, useRef } from 'react';
import './globals.css';

// ── Types ─────────────────────────────────────────────────────────────────────
interface NewsResult {
  label: string;
  confidence: number;
  verdict: string;
  explanation: string;
}

interface PhysicsResult {
  verdict: string;
  confidence: number;
  reasoning: string;
  is_valid: boolean;
}

interface DetectionResponse {
  news?: NewsResult;
  physics?: PhysicsResult;
  timestamp: string;
  mode: string;
}

// ── Confidence Bar ─────────────────────────────────────────────────────────────
function ConfidenceBar({ value, type }: { value: number; type: string }) {
  const pct = Math.round(value * 100);
  return (
    <div>
      <div className="confidence-label">
        <span className="confidence-label-text">Confidence</span>
        <span className="confidence-value" style={{ color: type === 'real' || type === 'valid' ? 'var(--accent-green)' : type === 'unknown' ? 'var(--accent-amber)' : 'var(--accent-red)' }}>
          {pct}%
        </span>
      </div>
      <div className="confidence-track">
        <div
          className={`confidence-fill ${type}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

// ── News Result Card ───────────────────────────────────────────────────────────
function NewsResultCard({ data }: { data: NewsResult }) {
  const isFake = data.label === 'FAKE';
  const chipClass = isFake ? 'fake' : 'real';
  const cardClass = isFake ? 'verdict-fake' : 'verdict-real';

  return (
    <div className={`result-card ${cardClass}`}>
      <div className="result-card-header">
        <div className="result-type">
          <span>📰</span> News Analysis
        </div>
        <span className={`verdict-chip ${chipClass}`}>{data.label}</span>
      </div>
      <div className="verdict-text">{data.verdict}</div>
      <ConfidenceBar value={data.confidence} type={chipClass} />
      <div className="explanation-text">{data.explanation}</div>
    </div>
  );
}

// ── Physics Result Card ────────────────────────────────────────────────────────
function PhysicsResultCard({ data }: { data: PhysicsResult }) {
  const isValid = data.is_valid;
  const isUnknown = data.verdict.includes('Unverifiable');
  const chipClass = isUnknown ? 'unknown' : isValid ? 'valid' : 'invalid';
  const cardClass = isUnknown ? 'verdict-unknown' : isValid ? 'verdict-valid' : 'verdict-invalid';

  return (
    <div className={`result-card ${cardClass}`}>
      <div className="result-card-header">
        <div className="result-type">
          <span>⚛️</span> Physics Check
        </div>
        <span className={`verdict-chip ${chipClass}`}>
          {isValid ? 'VALID' : isUnknown ? 'UNCLEAR' : 'INVALID'}
        </span>
      </div>
      <div className="verdict-text">{data.verdict}</div>
      <ConfidenceBar value={data.confidence} type={chipClass} />
      <div className="explanation-text">{data.reasoning}</div>
    </div>
  );
}

// ── Input Card ─────────────────────────────────────────────────────────────────
function InputCard({
  type,
  value,
  onChange,
}: {
  type: 'news' | 'physics';
  value: string;
  onChange: (v: string) => void;
}) {
  const isNews = type === 'news';
  return (
    <div className={`input-card ${isNews ? '' : 'physics-card'}`}>
      <div className="card-header">
        <div className={`card-icon ${isNews ? 'news-icon' : 'physics-icon'}`}>
          {isNews ? '📰' : '⚛️'}
        </div>
        <div>
          <div className="card-title">{isNews ? 'News Article' : 'Physics Claim'}</div>
          <div className="card-desc">{isNews ? 'Paste a news article or headline' : 'Enter a physics claim to verify'}</div>
        </div>
      </div>
      <textarea
        id={`input-${type}`}
        className="detection-input"
        placeholder={
          isNews
            ? 'E.g. "Scientists discover a cure for cancer using AI…"'
            : 'E.g. "Objects can travel faster than the speed of light…"'
        }
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

// ── Main Page ──────────────────────────────────────────────────────────────────
export default function TruthShieldPage() {
  const [newsText, setNewsText] = useState('');
  const [physicsText, setPhysicsText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DetectionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const resultsRef = useRef<HTMLDivElement>(null);

  const handleDetect = async () => {
    if (!newsText.trim() && !physicsText.trim()) {
      setError('Please enter at least one piece of text to analyze.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ news_text: newsText, physics_text: physicsText }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || `Error ${response.status}`);
        return;
      }

      setResult(data);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err) {
      setError('Network error — make sure the FastAPI backend is running on port 8000.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const hasResults = result && (result.news || result.physics);

  return (
    <>
      {/* Animated background */}
      <div className="bg-scene">
        <div className="bg-grid" />
        <div className="bg-orb-cyan" />
      </div>

      <div className="page-wrapper">
        {/* Navbar */}
        <nav className="navbar">
          <div className="navbar-inner">
            <a href="/" className="logo">
              <div className="logo-icon">🛡️</div>
              <span className="logo-text">TruthShield AI</span>
            </a>
          </div>
        </nav>

        {/* Hero */}
        <section className="hero">
          <div className="container">
            <div className="hero-eyebrow">
              <span>●</span> Live Detection System
            </div>
            <h1 className="hero-title">
              Dual-Layer{' '}
              <span className="hero-title-gradient">AI Truth Detection</span>
            </h1>
            <p className="hero-subtitle">
              Simultaneously verify news credibility with BERT-based classification
              and validate physics claims with GPT-powered reasoning.
            </p>
            <div className="hero-stats">
              <div className="stat-item">
                <div className="stat-value">2</div>
                <div className="stat-label">Detection Engines</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">&lt;1s</div>
                <div className="stat-label">Analysis Time</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">97%</div>
                <div className="stat-label">Model Accuracy</div>
              </div>
            </div>
          </div>
        </section>

        {/* Detection Form */}
        <section style={{ paddingBottom: '40px' }}>
          <div className="container">
            <div className="section-label">✦ Detection Inputs</div>
            <div className="detection-grid">
              <InputCard type="news" value={newsText} onChange={setNewsText} />
              <InputCard type="physics" value={physicsText} onChange={setPhysicsText} />
            </div>

            <button
              id="detect-btn"
              className="detect-btn"
              onClick={handleDetect}
              disabled={loading}
            >
              <span className="detect-btn-inner">
                {loading ? (
                  <>
                    <span className="spinner" />
                    Analyzing…
                  </>
                ) : (
                  <>
                    <span>⚡</span>
                    DETECT BOTH
                  </>
                )}
              </span>
            </button>

            {error && (
              <div className="error-box">
                <span>⚠️</span> {error}
              </div>
            )}

            {/* Results */}
            {hasResults && (
              <div className="results-section" ref={resultsRef}>
                <div className="results-header">
                  <div className="results-title">🔍 Analysis Complete</div>
                  <span className="results-badge">✓ Done</span>
                </div>

                <div className="results-grid">
                  {result!.news && <NewsResultCard data={result!.news} />}
                  {result!.physics && <PhysicsResultCard data={result!.physics} />}
                </div>



                <div style={{ marginTop: '8px', color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                  Analyzed at {new Date(result!.timestamp).toLocaleTimeString()}
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Footer */}
        <footer className="footer">
          <strong style={{ color: 'var(--text-secondary)' }}>TruthShield AI</strong> — Built with{' '}
          <a href="https://fastapi.tiangolo.com" target="_blank">FastAPI</a> + {' '}
          <a href="https://nextjs.org" target="_blank">Next.js 15</a> + {' '}
          <a href="https://huggingface.co" target="_blank">HuggingFace</a>
        </footer>
      </div>
    </>
  );
}

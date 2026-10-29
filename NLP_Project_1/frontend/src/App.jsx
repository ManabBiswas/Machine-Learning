import { useState } from "react";

const SAMPLES = [
  "i am fine.",
  "we need to talk.",
  "who is sarah?",
  "you forgot my birthday??",
  "i baked your favorite cookies",
  "take your time, it is okay",
];

const THEME = {
  joy: "#22c55e",
  love: "#ec4899",
  sadness: "#38bdf8",
  anger: "#ef4444",
  fear: "#a78bfa",
  surprise: "#f59e0b",
};

function pct(value) {
  return `${(value * 100).toFixed(1)}%`;
}

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const color = result ? THEME[result.emotion] ?? "#94a3b8" : "#94a3b8";

  async function analyze(value = text) {
    const message = value.trim();
    if (!message) {
      setError("Type something she said first 🫥");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: message }),
      });
      if (!response.ok) {
        throw new Error(`API responded with ${response.status}`);
      }
      setResult(await response.json());
    } catch {
      setResult(null);
      setError("Could not reach the model API — start the backend: uvicorn api:app --port 8000");
    } finally {
      setLoading(false);
    }
  }

  function onChip(sample) {
    setText(sample);
    analyze(sample);
  }

  function onKeyDown(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      analyze();
    }
  }

  return (
    <div className="page">
      <header className="hero">
        <p className="badge">6 emotions · 16k sentences · 89% unseen accuracy</p>
        <h1>
          GF Mood <span>Predictor</span> 💘
        </h1>
        <p className="subtitle">
          Paste what she said. The model reads the text — not her mind. Entertainment only.
        </p>
      </header>

      <main className="card">
        <label htmlFor="said">What did she say? 👇</label>
        <textarea
          id="said"
          rows={3}
          maxLength={2000}
          placeholder='e.g. "i am fine."'
          value={text}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={onKeyDown}
        />

        <div className="chips">
          {SAMPLES.map((sample) => (
            <button key={sample} type="button" className="chip" disabled={loading} onClick={() => onChip(sample)}>
              {sample}
            </button>
          ))}
        </div>

        <button type="button" className="primary" disabled={loading} onClick={() => analyze()}>
          {loading ? "Reading between the lines…" : "Analyze the mood 🔍"}
        </button>

        {error && <p className="error">{error}</p>}

        {result ? (
          <section className="result" aria-live="polite">
            <div className="verdict">
              <span className="verdict-emoji">{result.emoji}</span>
              <div>
                <p className="status" style={{ color }}>
                  {result.status} · {pct(result.confidence)} confident
                </p>
                <h2 style={{ color }}>{result.emotion}</h2>
              </div>
            </div>

            <p className="tip">{result.tip}</p>

            <div className="meter" role="img" aria-label={`confidence ${pct(result.confidence)}`}>
              <div className="meter-fill" style={{ width: pct(result.confidence), background: color }} />
            </div>

            {result.confidence < 0.5 && (
              <p className="uncertain">Vibes unclear — the ancient technique applies: just ask her. 🙃</p>
            )}

            <div className="probabilities">
              {result.probabilities.map(([name, probability]) => (
                <div className="prob-row" key={name}>
                  <span className="prob-name">{name}</span>
                  <div className="prob-track">
                    <div
                      className="prob-fill"
                      style={{
                        width: pct(probability),
                        background: THEME[name] ?? "#94a3b8",
                      }}
                    />
                  </div>
                  <span className="prob-value">{pct(probability)}</span>
                </div>
              ))}
            </div>

            <details>
              <summary>What the model actually saw</summary>
              <code>{result.processed}</code>
            </details>
          </section>
        ) : (
          <p className="hint">No message yet. The mood oracle is listening.</p>
        )}
      </main>

      <footer>
        TF-IDF + Random Forest trained on the Kaggle emotion dataset · real girlfriend &gt; model
      </footer>
    </div>
  );
}

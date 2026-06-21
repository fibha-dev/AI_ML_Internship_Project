import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [featuresText, setFeaturesText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [risk, setRisk] = useState(0);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setResult(null);

      const features = featuresText
        .split(",")
        .map((f) => Number(f.trim()));

      const res = await axios.post("http://127.0.0.1:8000/predict", {
        features,
      });

      // fake probability if backend only returns 0/1
      const prediction = res.data.prediction;
      const probability = prediction === 1 ? 0.85 : 0.12;

      setResult(prediction);
      animateRisk(probability);
    } catch (err) {
      setResult("error");
    } finally {
      setLoading(false);
    }
  };

  const animateRisk = (target) => {
    let start = 0;
    const interval = setInterval(() => {
      start += 0.02;
      if (start >= target) {
        start = target;
        clearInterval(interval);
      }
      setRisk(start);
    }, 20);
  };

  return (
    <div className="bg">
      <div className="dashboard">

        {/* LEFT PANEL */}
        <div className="panel">
          <h1>💳 Fraud Shield</h1>
          <p>Enter transaction vector (comma separated)</p>

          <textarea
            placeholder="0.1, 1.2, 3.4, ..."
            value={featuresText}
            onChange={(e) => setFeaturesText(e.target.value)}
          />

          <button onClick={handleSubmit} disabled={loading}>
            {loading ? "Analyzing..." : "Run Risk Scan"}
          </button>
        </div>

        {/* RIGHT PANEL */}
        <div className="panel glass">

          <h2>Risk Analysis</h2>

          <div className="meter">
            <div
              className={`fill ${risk > 0.6 ? "high" : "low"}`}
              style={{ width: `${risk * 100}%` }}
            />
          </div>

          <div className="percent">
            {(risk * 100).toFixed(1)}%
          </div>

          <div className={`status ${
            result === 1 ? "fraud" : "safe"
          }`}>
            {result === null
              ? "Awaiting scan..."
              : result === "error"
              ? "System error"
              : result === 1
              ? "🚨 High Fraud Risk"
              : "✅ Transaction Safe"}
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
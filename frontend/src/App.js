import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [valueCount, setValueCount] = useState(0);
  const [error, setError] = useState("");

  const [actual, setActual] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [correct, setCorrect] = useState(null);

  const parseInput = (text) => {
    return text
      .trim()
      .replace(/[\n\t]/g, ",")
      .split(",")
      .map((v) => v.trim())
      .filter((v) => v !== "")
      .map((v) => Number(v));
  };

  const handleInputChange = (e) => {
    const text = e.target.value;

    setInput(text);

    const values = parseInput(text);

    setValueCount(values.length);

    setError("");

    if (values.length > 0 && values.some((v) => Number.isNaN(v))) {
      setError("Some values are not valid numbers");
    }
  };

  const loadSample = async () => {
    try {
      setLoading(true);

      const res = await axios.get(
        `${process.env.REACT_APP_API_URL}/random-test`
      );

      const features = res.data.features;

      setInput(features.join(", "));
      setValueCount(features.length);

      setActual(res.data.actual);

      setResult(null);
      setPrediction(null);
      setCorrect(null);
      setError("");
    } catch (err) {
      console.log(err);
      setError("Could not load sample");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);

      setResult(null);
      setError("");

      const values = parseInput(input);

      if (values.length !== 30) {
        setError(
          `Invalid input: Please enter exactly 30 values (you entered ${values.length})`
        );
        return;
      }

      const payload = {
  features: values
};

if (actual !== null) {
  payload.actual = actual;
}

const res = await axios.post(
  `${process.env.REACT_APP_API_URL}/predict`,
  payload
);

      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/predict`,
        {
          features: values,
          actual: actual,
        }
      );
      console.log(res.data);

      const pred = Number(res.data.prediction);

      setPrediction(pred);
      setCorrect(res.data.correct);

      setResult(pred === 1 ? "FRAUD" : "SAFE");
    } catch (err) {
      console.log(err);
      setError("Connection error: Unable to reach server");
      setResult("ERROR");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setInput("");
    setResult(null);
    setError("");
    setValueCount(0);

    setActual(null);
    setPrediction(null);
    setCorrect(null);
  };

  return (
    <div className="page">
      <div className="container">

        <div className="header">
          <div className="icon-header">🔐</div>
          <h1>Credit Card Fraud Detection</h1>
          <p className="subtitle">
            Advanced ML-powered transaction analysis
          </p>
        </div>

        <div className="info-section">
          <div className="info-item">
            <span className="info-label">Features Required:</span>
            <span className="info-value">30 numerical values</span>
          </div>

          <div className="info-item">
            <span className="info-label">Format:</span>
            <span className="info-value">
              Comma, space, or newline separated
            </span>
          </div>
        </div>

        <div className="input-wrapper">
          <label className="input-label">
            Transaction Features
          </label>

          <textarea
            value={input}
            onChange={handleInputChange}
            className="input-textarea"
            disabled={loading}
          />

          <div className="input-info">
            <span
              className={`value-count ${
                valueCount === 30
                  ? "valid"
                  : valueCount > 0
                  ? "warning"
                  : ""
              }`}
            >
              {valueCount}/30 values
            </span>

            {error && (
              <span className="error-message">
                {error}
              </span>
            )}
          </div>
        </div>

        <div className="button-group">

          <button
            className="btn btn-secondary"
            onClick={loadSample}
            disabled={loading}
          >
            📋 Load Test Sample
          </button>

          <button
            className="btn btn-primary"
            onClick={handleSubmit}
            disabled={loading || valueCount !== 30}
          >
            ⚡ {loading ? "Analyzing..." : "Analyze Transaction"}
          </button>

          <button
            className="btn btn-secondary"
            onClick={handleClear}
            disabled={loading}
          >
            ↻ Clear
          </button>

        </div>

        {result && (
          <div className={`result-container result-${result.toLowerCase()}`}>
            <div className="result-icon">
              {result === "FRAUD" && ""}
              {result === "SAFE" && ""}
              {result === "ERROR" && ""}
            </div>

            <div className="result-content">

              <h2 className="result-title">
                {result === "FRAUD" && "Fraud Detected"}
                {result === "SAFE" && "Transaction Safe"}
                {result === "ERROR" && "Analysis Failed"}
              </h2>

              <p className="result-message">
                {result === "FRAUD" &&
                  "This transaction has been flagged as potentially fraudulent."}

                {result === "SAFE" &&
                  "This transaction appears to be legitimate."}

                {result === "ERROR" &&
                  "Please check your input and try again."}
              </p>

            </div>
          </div>
        )}

        {prediction !== null && (
          <div className="details-card">
            <div className="details-header">
              <div className="details-icon">📊</div>
              <div>
                <h3>Model Evaluation</h3>
                <p className="details-subtitle">
                  Comparison between the predicted and actual outcome
                </p>
              </div>
            </div>

            <div className="details-grid">
              <div className="detail-item">
                <span className="detail-label">Predicted</span>
                <span className={`detail-value ${prediction === 1 ? "incorrect" : "correct"}`}>
                  {prediction === 1 ? "Fraud" : "Normal"}
                </span>
              </div>

              <div className="detail-item">
                <span className="detail-label">Actual</span>
                <span className={`detail-value ${actual === 1 ? "incorrect" : "correct"}`}>
                  {actual === 1 ? "Fraud" : "Normal"}
                </span>
              </div>
            </div>

            <div className={`accuracy-badge ${correct ? "accuracy-good" : "accuracy-bad"}`}>
              {correct ? "✓ Correct Prediction" : "✗ Incorrect Prediction"}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;
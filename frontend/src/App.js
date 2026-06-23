import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [valueCount, setValueCount] = useState(0);
  const [error, setError] = useState("");

  const parseInput = (text) => {
    return text
      .trim()
      .replace(/[\n\t]/g, ",")
      .split(",")
      .map(v => v.trim())
      .filter(v => v !== "")
      .map(v => Number(v));
  };

  const handleInputChange = (e) => {
    const text = e.target.value;
    setInput(text);

    const values = parseInput(text);
    setValueCount(values.length);
    setError("");

    if (values.length > 0 && values.some(v => Number.isNaN(v))) {
      setError("Some values are not valid numbers");
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setResult(null);
      setError("");

      const values = parseInput(input);

      if (values.length !== 30) {
        setError(`Invalid input: Please enter exactly 30 values (you entered ${values.length})`);
        return;
      }

      const hasInvalid = values.some(v => Number.isNaN(v));
      if (hasInvalid) {
        setError("Invalid input: Some values are not valid numbers");
        return;
      }

      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/predict`,
        {
          features: values,
        }
      );


      const pred = Number(res.data.prediction);
      setResult(pred === 1 ? "FRAUD" : "SAFE");

    } catch (err) {
      console.log(err);
      setError("Connection error: Unable to reach the server");
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
  };

  return (
    <div className="page">
      <div className="container">
        {/* Header */}
        <div className="header">
          <div className="icon-header">🔐</div>
          <h1>Credit Card Fraud Detection</h1>
          <p className="subtitle">Advanced ML-powered transaction analysis</p>
        </div>

        {/* Info Section */}
        <div className="info-section">
          <div className="info-item">
            <span className="info-label">Features Required:</span>
            <span className="info-value">30 numerical values</span>
          </div>
          <div className="info-item">
            <span className="info-label">Format:</span>
            <span className="info-value">Comma, space, or newline separated</span>
          </div>
        </div>

        {/* Input Section */}
        <div className="input-wrapper">
          <label htmlFor="transaction-input" className="input-label">
            Transaction Features
          </label>
          <textarea
            id="transaction-input"
            placeholder="Enter 30 values&#10;Example: 0.1, 1.2, 3.4, -2.1, 0.5, ...&#10;Values can be separated by commas, spaces, or new lines"
            value={input}
            onChange={handleInputChange}
            className="input-textarea"
            disabled={loading}
          />
          <div className="input-info">
            <span className={`value-count ${valueCount === 30 ? 'valid' : valueCount > 0 ? 'warning' : ''}`}>
              {valueCount}/30 values
            </span>
            {error && <span className="error-message">{error}</span>}
          </div>
        </div>

        {/* Button Group */}
        <div className="button-group">
          <button
            onClick={handleSubmit}
            disabled={loading || valueCount !== 30}
            className="btn btn-primary"
          >
            <span className="btn-icon">⚡</span>
            {loading ? "Analyzing..." : "Analyze Transaction"}
          </button>
          <button
            onClick={handleClear}
            disabled={loading}
            className="btn btn-secondary"
          >
            <span className="btn-icon">↻</span>
            Clear
          </button>
        </div>

        {result && (
          <div className={`result-container result-${result.toLowerCase()}`}>
            <div className="result-icon">
              {result === "FRAUD" && "⚠️"}
              {result === "SAFE" && "✓"}
              {result === "ERROR" && "❌"}
            </div>
            <div className="result-content">
              <h2 className="result-title">
                {result === "FRAUD" && "Fraud Detected"}
                {result === "SAFE" && "Transaction Safe"}
                {result === "ERROR" && "Analysis Failed"}
              </h2>
              <p className="result-message">
                {result === "FRAUD" && "This transaction has been flagged as potentially fraudulent."}
                {result === "SAFE" && "This transaction appears to be legitimate."}
                {result === "ERROR" && "Please check your input and try again."}
              </p>
            </div>
          </div>
        )}
        {/* {table.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Actual</th>
                <th>Predicted</th>
                <th>Correct</th>
              </tr>
            </thead>

            <tbody>
              {table.map((row, i) => (
                <tr key={i}>
                  <td>{row.actual}</td>
                  <td>{row.predicted}</td>
                  <td>{row.correct ? "✔" : "❌"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )} */}
      </div>
    </div>
  );
}

export default App;
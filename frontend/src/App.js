import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const parseInput = (text) => {
    return text
      .replace(/\n/g, ",")
      .split(",")
      .map(v => v.trim())
      .filter(v => v !== "")
      .map(Number)
      .filter(v => !Number.isNaN(v));
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setResult(null);

      const values = parseInput(input);

      if (values.length !== 30) {
        setResult("ERROR");
        return;
      }

      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/predict`,
        {
          features: values,
        }
      );

      setResult(res.data.prediction === 1 ? "FRAUD" : "SAFE");

    } catch (err) {
      console.log(err);
      setResult("ERROR");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1>Fraud Detection System</h1>
      <p>Enter exactly 30 comma-separated values</p>

      <textarea
        placeholder="Example: 0.1, 1.2, 3.4 ... (30 values total)"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Analyzing..." : "Check Transaction"}
      </button>

      {result && (
        <div className={`result ${result}`}>
          {result === "FRAUD" && "Fraud Detected"}
          {result === "SAFE" && "Transaction Safe"}
          {result === "ERROR" && "❌ Enter exactly 30 valid numbers"}
        </div>
      )}
    </div>
  );
}

export default App;
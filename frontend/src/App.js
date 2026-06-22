import { useState } from "react";
import axios from "axios";
import "./App.css";

console.log("API URL:", process.env.REACT_APP_API_URL);

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);


  const handleSubmit = async () => {
    try {
      setLoading(true);
      setResult(null);

      const values = input
        .split(",")
        .map((v) => Number(v.trim()));

      if (values.length !== 30 || values.some(isNaN)) {
        setResult("ERROR");
        return;
      }

      const res = await axios.post("http://127.0.0.1:8000/predict", {
        features: values,
      });

      setResult(res.data.prediction === 1 ? "FRAUD" : "SAFE");

    } catch (err) {
      setResult("ERROR");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
    

      <h1>Fraud Detection System</h1>
      <p>Enter 30 comma-separated values (Amount + Time included)</p>

      <textarea
        placeholder="Example: 0.1, 1.2, 3.4, ... (30 values total)"
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
          {result === "ERROR" && "Enter exactly 30 valid numbers"}
        </div>
      )}

    </div>
  );
}

export default App;
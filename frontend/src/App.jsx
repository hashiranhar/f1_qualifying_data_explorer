import { useState, useEffect } from "react";
import DriverSearch from "./components/DriverSearch";
import ResultsCard from "./components/ResultsCard";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function App() {
  const [drivers, setDrivers] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API}/api/drivers`)
      .then(r => r.json())
      .then(d => setDrivers(d.drivers))
      .catch(() => setError("Failed to load driver list — is the backend running?"));
  }, []);

  async function handleSelect(code) {
    if (!code) { setResult(null); return; }
    setLoading(true);
    setError(null);
    try {
      const r = await fetch(`${API}/api/driver/${code}`);
      if (!r.ok) throw new Error(`Driver not found`);
      setResult(await r.json());
    } catch (e) {
      setError(e.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div style={{ marginBottom: "32px" }}>
        <h1 style={{ fontSize: "20px", fontWeight: "700", marginBottom: "4px" }}>
          F1 Qualifying Explorer
        </h1>
        <p style={{ fontSize: "13px", color: "#888" }}>
          2026 Australian Grand Prix · Qualifying
        </p>
      </div>

      <DriverSearch drivers={drivers} onSelect={handleSelect} />

      {loading && (
        <p style={{ marginTop: "24px", fontSize: "13px", color: "#888" }}>Loading...</p>
      )}
      {error && (
        <p style={{ marginTop: "24px", fontSize: "13px", color: "#c00" }}>{error}</p>
      )}
      <ResultsCard result={result} />
    </div>
  );
}
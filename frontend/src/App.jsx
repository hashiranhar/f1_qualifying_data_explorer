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
      <div style={{
        background: "#111",
        borderRadius: "12px",
        padding: "20px 24px",
        marginBottom: "24px",
        borderLeft: "4px solid #E10600",
      }}>
        <h1 style={{ fontSize: "18px", fontWeight: "700", color: "#fff", letterSpacing: "0.06em" }}>
          F1 QUALIFYING EXPLORER
        </h1>
        <p style={{ fontSize: "12px", color: "#888", marginTop: "4px", letterSpacing: "0.04em" }}>
          2026 AUSTRALIAN GRAND PRIX · QUALIFYING
        </p>
      </div>

      <DriverSearch drivers={drivers} onSelect={handleSelect} />

      {loading && (
        <p style={{ marginTop: "24px", fontSize: "13px", color: "#888" }}>Loading...</p>
      )}
      {error && (
        <p style={{ marginTop: "24px", fontSize: "13px", color: "#E10600" }}>{error}</p>
      )}
      <ResultsCard result={result} />
    </div>
  );
}
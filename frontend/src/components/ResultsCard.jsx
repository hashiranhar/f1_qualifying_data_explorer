export default function ResultsCard({ result }) {
  if (!result) return null;

  return (
    <div style={{
      background: "#fff",
      border: "1.5px solid #ddd",
      borderRadius: "12px",
      padding: "24px",
      marginTop: "24px",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <h2 style={{ fontSize: "26px", fontWeight: "700", letterSpacing: "0.1em" }}>
          {result.driver_code}
        </h2>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: "11px", color: "#888", textTransform: "uppercase", letterSpacing: "0.1em" }}>
            Qualifying Position
          </div>
          <div style={{ fontSize: "32px", fontWeight: "700", color: result.qualifying_position ? "#E10600" : "#bbb" }}>
            {result.qualifying_position ? `P${result.qualifying_position}` : "—"}
          </div>
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        {result.sessions.map(s => (
          <div key={s.session} style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            padding: "14px 16px",
            background: s.participated ? "#fafafa" : "#f4f4f4",
            borderRadius: "8px",
            border: "1px solid #eee",
            borderLeft: s.participated ? "3px solid #E10600" : "3px solid #ddd",
          }}>
            <span style={{
              fontSize: "12px",
              fontWeight: "700",
              letterSpacing: "0.12em",
              color: s.participated ? "#111" : "#aaa",
            }}>
              {s.session}
            </span>
            <span style={{
              fontSize: "15px",
              fontWeight: "600",
              fontFamily: "monospace",
              fontVariantNumeric: "tabular-nums",
              color: s.best_lap_time ? "#111" : "#bbb",
            }}>
              {s.best_lap_time_fmt ?? (s.participated ? "No valid lap" : "Did not participate")}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
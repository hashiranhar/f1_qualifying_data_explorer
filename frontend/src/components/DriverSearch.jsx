import { useState } from "react";

export default function DriverSearch({ drivers, onSelect }) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);

  const filtered = query.length === 0 ? [] : drivers.filter(d =>
    d.toLowerCase().includes(query.toLowerCase())
  );

  function handleSelect(code) {
    setQuery(code);
    setOpen(false);
    onSelect(code);
  }

  return (
    <div style={{ position: "relative" }}>
      <input
        type="text"
        value={query}
        placeholder="Search driver code (e.g. HAM, VER...)"
        onChange={e => { setQuery(e.target.value); setOpen(true); onSelect(null); }}
        onFocus={() => setOpen(true)}
        style={{
          width: "100%",
          padding: "12px 16px",
          fontSize: "15px",
          border: "1.5px solid #ddd",
          borderRadius: "8px",
          outline: "none",
          background: "#fff",
        }}
      />
      {open && filtered.length > 0 && (
        <ul style={{
          position: "absolute",
          top: "calc(100% + 4px)",
          left: 0,
          right: 0,
          background: "#fff",
          border: "1.5px solid #ddd",
          borderRadius: "8px",
          listStyle: "none",
          zIndex: 10,
          overflow: "hidden",
          boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        }}>
          {filtered.map(d => (
            <li
              key={d}
              onClick={() => handleSelect(d)}
              style={{
                padding: "10px 16px",
                cursor: "pointer",
                fontSize: "14px",
                letterSpacing: "0.05em",
              }}
              onMouseEnter={e => e.currentTarget.style.background = "#f5f5f5"}
              onMouseLeave={e => e.currentTarget.style.background = "#fff"}
            >
              {d}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
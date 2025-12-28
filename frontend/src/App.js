import { useState } from "react";
import "./App.css";

function App() {
  const [userId, setUserId] = useState("");
  const [data, setData] = useState(null);

  const fetchRisk = async () => {
    const res = await fetch(`http://127.0.0.1:8000/score/${userId}`);
    const json = await res.json();
    setData(json);
  };

  return (
    <div className="container">
      <h2>Credit Risk Dashboard</h2>

      <input
        placeholder="Enter User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />

      <button onClick={fetchRisk}>Fetch Risk</button>

      {data && (
        <div className="card">
          <h3>User: {data.user_id}</h3>
          <h1 style={{ color: data.risk_score > 0.6 ? "red" : "green" }}>
            Risk Score: {data.risk_score}
          </h1>

          <pre>{JSON.stringify(data.features, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

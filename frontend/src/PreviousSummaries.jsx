import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function PreviousSummaries() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const savedHistory = JSON.parse(
      localStorage.getItem("summaryHistory") || "[]"
    );
    setHistory(savedHistory);
  }, []);

  return (
    <div className="container">
      <h1 className="article-header">Previous Summaries</h1>
      <div className="button-link-wrapper">
        <Link to="/" className="button-link">
          ← Back to Home
        </Link>
      </div>
      {history.length === 0 ? (
        <p style={{ textAlign: "center" }}>No summaries found.</p>
      ) : (
        <ul>
          {history.map(({ url, language, summary, timestamp }, i) => (
            <li
              key={i}
              style={{
                marginBottom: 16,
                borderBottom: "1px solid #ccc",
                paddingBottom: 8,
              }}
            >
              <div>
                <strong>URL:</strong> {url}
              </div>
              <div>
                <strong>Language:</strong> {language}
              </div>
              <div>
                <strong>Time:</strong> {new Date(timestamp).toLocaleString()}
              </div>
              <div>
                <strong>Summary:</strong> {summary}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

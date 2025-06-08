import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function useLinkStatus(linkId) {
  const [status, setStatus] = useState(null);
  const [progress, setProgress] = useState(0);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    if (!linkId) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/result/${linkId}`);
        if (!res.ok) {
          clearInterval(interval);
          return;
        }
        const data = await res.json();
        setStatus(data.status);
        setProgress(data.progress);
        setSummary(data.summary);

        if (data.status === "done" || data.status === "error") {
          clearInterval(interval);
        }
      } catch {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [linkId]);

  return { status, progress, summary };
}

export default function App() {
  const [url, setUrl] = useState("");
  const [language, setLanguage] = useState("English");
  const [linkId, setLinkId] = useState(null);

  const { status, progress, summary } = useLinkStatus(linkId);

  useEffect(() => {
    if (status === "done" && summary) {
      const savedHistory = JSON.parse(
        localStorage.getItem("summaryHistory") || "[]"
      );
      const newEntry = {
        url,
        language,
        summary,
        timestamp: new Date().toISOString(),
      };
      const updatedHistory = [newEntry, ...savedHistory].slice(0, 10);
      localStorage.setItem("summaryHistory", JSON.stringify(updatedHistory));
    }
  }, [status, summary, url, language]);

  function handleCopy() {
    if (summary) {
      navigator.clipboard.writeText(summary);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, language }),
      });
      if (!res.ok) throw new Error("Server Error!");
      const data = await res.json();
      setLinkId(data.id);
    } catch {
      alert("Error: Can't send URL");
    }
  }

  return (
    <div className="container">
      <h1 className="article-header">Article Summarizer</h1>
      <div className="button-link-wrapper">
        <Link to="/history" className="button-link">
          Previous Summaries
        </Link>
      </div>
      <form onSubmit={handleSubmit} noValidate autoComplete="off">
        <p>
          <b>Article URL</b>
        </p>
        <input
          type="url"
          placeholder="Type URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <p>
          <b>Desired Language</b>
        </p>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="English">English</option>
          <option value="Polish">Polish</option>
          <option value="German">German</option>
          <option value="Spanish">Spanish</option>
          <option value="French">French</option>
          <option value="Japanese">Japanese</option>
          <option value="Korean">Korean</option>
          <option value="Chinese">Chinese</option>
          <option value="Czech">Czech</option>
          <option value="Russian">Russian</option>
          <option value="Ukrainian">Ukrainian</option>
          <option value="Norwegian">Norwegian</option>
          <option value="Swedish">Swedish</option>
        </select>

        <button type="submit">Summarize</button>
      </form>

      {linkId && (
        <div className="status-container">
          <div>
            Status: <strong>{status ?? "loading..."}</strong>
          </div>
          <div
            className="progress-bar"
            style={{ backgroundColor: "#ddd", width: "100%", height: 10 }}
          >
            <div
              className="progress-fill"
              style={{
                width: `${progress}%`,
                height: 10,
                backgroundColor: "green",
              }}
            />
          </div>
          <div>Progress: {progress}%</div>

          {status === "done" && (
            <div className="summary">
              <h3>Summary:</h3>
              <p>{summary}</p>
              <button onClick={handleCopy}>Copy</button>
            </div>
          )}

          {status === "error" && (
            <div className="error">Error while trying to summarize</div>
          )}
        </div>
      )}
    </div>
  );
}

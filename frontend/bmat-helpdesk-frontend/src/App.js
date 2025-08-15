import { EventSourcePolyfill } from 'event-source-polyfill';

import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [agent, setAgent] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const askBMAT = () => {
    if (!query.trim()) {
      setResponse("Please enter a question.");
      return;
    }
    setLoading(true);
    setResponse("");
    setAgent("");

    const eventSource = new EventSourcePolyfill("http://localhost:5000/ask-stream", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      payload: JSON.stringify({ query })
    });

    eventSource.onmessage = (event) => {
      if (event.data === "[DONE]") {
        setLoading(false);
        eventSource.close();
        return;
      }
      try {
        const parsed = JSON.parse(event.data);
        if (parsed.agent) setAgent(parsed.agent);
        if (parsed.token) setResponse((prev) => prev + parsed.token);
        if (parsed.response) setResponse(parsed.response);
      } catch (err) {
        console.error("Stream parse error", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("Stream error", err);
      setLoading(false);
      eventSource.close();
    };
  };

  return (
    <div className="App">
      <h1>BMAT Helpdesk</h1>
      <div className="chat-box">
        <input
          type="text"
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && askBMAT()}
        />
        <button onClick={askBMAT} disabled={loading}>
          {loading ? "Typing..." : "Ask"}
        </button>
      </div>
      <div className="output">
        {agent && <p><strong>Agent:</strong> {agent}</p>}
        {response && <p><strong>Response:</strong> {response}</p>}
      </div>
    </div>
  );
}

export default App;

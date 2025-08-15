import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [agent, setAgent] = useState("");
  const [response, setResponse] = useState("");

  const askBMAT = async () => {
    try {
      const res = await axios.post("http://localhost:5000/ask", { query });
      setAgent(res.data.agent);
      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
      setResponse("Error connecting to BMAT API.");
    }
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
        />
        <button onClick={askBMAT}>Ask</button>
      </div>
      <div className="output">
        {agent && <p><strong>Agent:</strong> {agent}</p>}
        {response && <p><strong>Response:</strong> {response}</p>}
      </div>
    </div>
  );
}

export default App;

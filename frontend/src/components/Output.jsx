import React from "react";
import '../App.css'

function Output({ output }) {
  return (
    <div className="output-container">
      <h2 className="output-h2">Output:</h2>
      <pre className="output">{output}</pre>
    </div>
  );
}

export default Output;

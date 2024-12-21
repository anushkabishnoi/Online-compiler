import React from "react";
import '../App.css'

function CodeEditor({ code, setCode }) {
  return (
    <div className="codeEditor-container">
      <textarea
        className="code-editor"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows="10"
        cols="50"
        placeholder="Enter your code here"
      ></textarea>
    </div>
  );
}

export default CodeEditor;

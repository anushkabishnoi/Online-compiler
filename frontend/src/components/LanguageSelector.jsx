import React from "react";
import '../App.css'

function LanguageSelector({ language, setLanguage }) {
  return (
    <select value={language} onChange={(e) => setLanguage(e.target.value)}>
      <option value="python">Python</option>
      <option value="java">Java</option>
      <option value="cpp">C++</option>
    </select>
  );
}

export default LanguageSelector;

import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");

  const compileCode = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/compile/", {
        code,
      });
      setOutput(response.data.output);
    } catch (error) {
      console.error("Error compiling code:", error);
    }
  };
  return (
    <div>
      <textarea value={code} onChange={(e) => setCode(e.target.value)} />
      <button onClick={compileCode}>Compile</button>
      <pre>{output}</pre>
    </div>
  );
}

export default App;

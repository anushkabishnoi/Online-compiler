import { useState } from "react";
import axios from "axios";
import CodeEditor from "./components/CodeEditor";
import LanguageSelector from "./components/LanguageSelector";
import Output from "./components/Output";

function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");

  // const compileCode = async () => {
  //   try {
  //     const response = await axios.post("http://localhost:8000/api/compile/", {
  //       code,
  //     });
  //     setOutput(response.data.output);
  //   } catch (error) {
  //     console.error("Error compiling code:", error);
  //   }
  // };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Sending request with:", { code, language }); // Debugging log
    try {
      // const response = await axios.post("http://localhost:8000/api/compile/", {   code, language,});
      const response = await axios.post(
        "http://localhost:8000/api/compile/",
        { code, language },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log("Response received:", response.data);
      setOutput(response.data.output);
    } catch (error) {
      console.error(
        "Error response:",
        error.response ? error.response.data : error
      );
      setOutput(
        "Error: " + (error.response ? error.response.data.error : error.message)
      );
    }
  };

  return (
    <div className="App">
      <h1>Online Compiler</h1>
      <form onSubmit={handleSubmit}>
        <CodeEditor code={code} setCode={setCode} />
        <LanguageSelector language={language} setLanguage={setLanguage} />
        <button type="submit">Submit</button>
      </form>
      <Output output={output} />
    </div>
  );
}

export default App;

import React, { useState } from 'react';
import { VSCodeButton } from "@vscode/webview-ui-toolkit/react";
import { vscode } from './vscode';

function App() {
  const [input1, setInput1] = useState('');
  const [input2, setInput2] = useState('');
  const [input3, setInput3] = useState('');

  function handleHowdyClick() {
    vscode.postMessage({
      command: "ready",
      text: "Hey there partner! 🤠",
      input1: input1,
      input2: input2,
      input3: input3
    });
  }

  return (
    <main style={styles.main}>
      <div style={styles.container}>
        <h1 style={styles.header}>Code Genie</h1>
        
        <label htmlFor="Name" style={styles.label}>Code base Path:</label>
        <input 
          type="text" 
          id="Name" 
          name="Name" 
          style={styles.input}
          value={input1}
          onChange={(e) => setInput1(e.target.value)}
        />
        
        <label htmlFor="input2" style={styles.label}>Project(Flavor):</label>
        <input 
          type="text" 
          id="input2" 
          style={styles.input}
          value={input2}
          onChange={(e) => setInput2(e.target.value)}
        />

        <label htmlFor="input3" style={styles.label}>Module:</label>
        <input 
          type="text" 
          id="input3" 
          style={styles.input}
          value={input3}
          onChange={(e) => setInput3(e.target.value)}
        />

        <VSCodeButton style={styles.button} onClick={handleHowdyClick}>Click Me!</VSCodeButton>
      </div>
    </main>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  main: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f4f4f4',
  },
  container: {
    backgroundColor: '#fff',
    padding: '40px',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '400px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '20px',
    color: '#333',
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    fontSize: '14px',
    color: '#555',
  },
  input: {
    width: '100%',
    padding: '10px',
    marginBottom: '15px',
    fontSize: '14px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    boxSizing: 'border-box',
  },
  note: {
    marginBottom: '15px',
    fontSize: '12px',
    color: '#777',
  },
  button: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#007ACC',
    color: '#fff',
    fontSize: '16px',
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    textAlign: 'center',
  },
};

export default App;

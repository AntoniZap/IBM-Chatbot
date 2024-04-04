import React, { useState } from 'react';
import { saveAs } from 'file-saver';
import './InsertDocument.css';
import axios from "axios";
import io from "socket.io-client"; // Import CSS file for styling

function InsertDocument() {
  axios.defaults.baseURL = 'http://localhost:5000';
  const [files, setFiles] = useState(["Click 'Refresh Files' to load"]);
  const [selectedFile, setSelectedFile] = useState("");

  const handleInputChange = (event) => {
    setFileName(event.target.value);
  };

  const refresh = async () => {
    try {
      await axios.post('/files')
          .then(response => {
            setFiles(response.data.files);
          })
          .catch(error => {
            console.error('Error fetching data:', error);
            setFiles([]);
          });
    } catch (e) {
      if (e instanceof Error) alert(e);
    }
  };

  const setFile = async (file) => {
    try {
      setSelectedFile(file);
      await axios.post('/setFile', {file: file})
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    } catch (e) {
      if (e instanceof Error) alert(e);
    }
  };

  return (
    <div className="insert-document-container">
      <div className="openai-card">

          <h1 className="header-api">Select Reviews/Feedback File (.CSV)</h1>
          <h5>Add relevant datasets to the 'IBM-Chatbot/' folder and they will appear below.</h5>
          <h6>You may use any relevant comma-seperated values file with FeedBot.</h6>
          <br/>
        {
          files.map((file, index) => (
            [<label key={`enabled-llm.${file}.${index}`}>
              <button name="g2" onClick={(event) => {setFile(file);}}>{file}</button>
            </label>, <br/>]))
        }
        <br/><br/><br/>
        <button className="API-button" onClick={refresh}>
          Refresh Files
        </button>
        {selectedFile !== "" && (
        <h6>Using: "{selectedFile}"</h6>
            )}
      </div>
    </div>
  );
}

export default InsertDocument;

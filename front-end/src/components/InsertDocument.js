import React, { useState } from 'react';
import { saveAs } from 'file-saver';
import './InsertDocument.css'; // Import CSS file for styling

function InsertDocument() {
  const [fileName, setFileName] = useState('');

  const handleInputChange = (event) => {
    setFileName(event.target.value);
  };

  const handleFileSubmit = () => {
    if (fileName.trim() !== '') {
      // Assuming the file exists, perform your action here
      alert(`File "${fileName}.csv" submitted!`);
    } else {
      alert('Please enter a file name.');
    }
  };

  return (
    <div className="insert-document-container">
      <div className="openai-card">
        <header>
          <h1 className="header-api">Insert your .csv file</h1>
          <h3 className="instructions"> Please create a folder on your machine named "IBM-chatbot" and put your .csv file into that folder.</h3>
          <h2 className="h2-api">Enter the file name below</h2>
        </header>
        <input
          type="text"
          placeholder="Enter .csv file name"
          value={fileName}
          onChange={handleInputChange}
          className="input-val"
        />
        <button className="API-button" onClick={handleFileSubmit}>
          Upload CSV
        </button>
      </div>
    </div>
  );
}

export default InsertDocument;

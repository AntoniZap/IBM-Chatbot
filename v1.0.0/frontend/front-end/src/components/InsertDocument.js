import React, { useState } from 'react';
import { saveAs } from 'file-saver';

function FileUpload() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);

    // Save the file locally (in the 'uploads' folder)
    const reader = new FileReader();
    reader.onload = (e) => {
      const fileContent = e.target.result;
      const fileName = 'my-file.csv'; // Set your desired file name
      const blob = new Blob([fileContent], { type: 'text/csv' });
      saveAs(blob, fileName); // Save the file using file-saver
    };
    reader.readAsArrayBuffer(file);
  };

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={() => document.querySelector('input[type="file"]').click()}>
        Upload CSV
      </button>
    </div>
  );
}

export default FileUpload;

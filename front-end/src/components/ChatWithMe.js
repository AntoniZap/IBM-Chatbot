import React, { useState } from 'react';
import axios from 'axios';

function ChatWithMe() {
  axios.defaults.baseURL = 'http://localhost:5000';
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);


  const handleInputChange = (event) => {
    setMessage(event.target.value);
  };

  const handleOptionChange = (event) => {
    const llm = event.target.value;
    
    axios.post('/llm', { llm: llm })
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            console.error('Error with LLM request:', error);
        });
  };

  const handleSendMessage = async () => {
    setChatHistory([...chatHistory, "You: " + message]);
    setMessage('');
    axios.post('/message', {message: message})
      .then(response => {
        setChatHistory([...chatHistory, 'You: ' + message, "AI: " + response.data]);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };
  return (
    <div>
      <div>
        {chatHistory.map((msg, index) => (
          <p key={index}>{msg}</p>
        ))}
      </div>
      <select onChange={handleOptionChange}>
        <option>ChatGPT</option>
        <option>AI21</option>
        <option>LLAMA</option>
      </select>
      <input type="text" value={message} onChange={handleInputChange} />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
}

export default ChatWithMe;

import React, { useState } from 'react';
import axios from 'axios';
import Bot from '../assets/bot.png';
import User from '../assets/user.png';
import './ChatWithMe.css'; // Import the CSS file

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
    setChatHistory([...chatHistory, {sender: 'user', message: message }]);
    setMessage('');
    axios.post('/message', {message: message})
      .then(response => {
        setChatHistory([...chatHistory, { sender: 'user', message: message }, { sender: 'bot', message: response.data[0].answer }]);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };
  return (
    <div>
      <div className="message-bubble">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <text>{msg.message}</text>
            <img src={msg.sender === 'user' ? User : Bot} alt={`${msg.sender} icon`} className="user-icon" />
          </div>
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

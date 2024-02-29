import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Bot from '../assets/bot.png';
import User from '../assets/user.png';
import './ChatWithMe.css'; // Import the CSS file

const mock = [{"answer":"\nAmazon Kindle E-Reader 6\" Wifi (8th Generation, 2016)","llm":"LLaMa"}, {"answer":"\nAmazon Kindle E-Reader 6\" Wifi (8th Generation, 2016)","llm":"AI21"}];


import io from 'socket.io-client';
const socket = io('http://localhost:5000');

function ChatWithMe() {
  axios.defaults.baseURL = 'http://localhost:5000';
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
    const [answers, setAnswers] = useState({});
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        socket.on("socket", (data) => {
            const { llm, answer } = data;
            setAnswers(answers => {
                const last = { ...answers, [llm]: { llm, answer } };
                console.log(last);
                return last;
            });
        });
    }, []);

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
        setLoading(() => true);
        const llm = document.querySelector('input[name="g1"]:checked')?.value;
        if (llm !== undefined) {
            try {
                await axios.post('/selectAnswer', { llm })
            } catch(error) {
                console.error('Error selecting answer:', error);
                return;
            }
            setChatHistory(chatHistory => [...chatHistory, { sender: 'bot', message: answers[llm].answer }]);
            setAnswers(answers => ({}));
        } else {
            alert("Not proceeding without llm chosen");
        }

        await axios.post('/message', {message: message, llms: ["ai21", "llama"]})
            .then(response => {
                setChatHistory(chatHistory => [...chatHistory, { sender: 'user', message: message }]);
                setAnswers(Object.fromEntries(response.data.map(answer => [answer.llm, answer])));
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
        setLoading(() => false);
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
          {   
            answers && (
                <>
                    <h3>Answers</h3>
                    <center className="lmm-container-box">
                    {
                        Object.values(answers).map((msg, index) => (
                            <div key={"..."+index}
                                 className={loading
                                            ? "loading llm-container"
                                            : "llm-container" }>
                                <label>
                                    <h4>{msg.llm}</h4>
                                    <input value={msg.llm} id={"..."+index} type="radio" name="g1"/>
                                    {msg.answer === undefined
                                     ? <span style={{color: "red"}}>No data!</span>
                                     : (msg.answer.trim() || <em>(Nothing was returned 🕳️)</em>)}
                                </label>
                            </div>
                        ))
                    }
                    </center>
                </>
            )
        }
      <select onChange={handleOptionChange}>
        <option>ChatGPT</option>
        <option>AI21</option>
        <option>LLAMA</option>
      </select>
      <input type="text" value={message} onChange={handleInputChange} />
      <button onClick={handleSendMessage} disabled={loading}>Send</button>
    </div>
  );
}

export default ChatWithMe;

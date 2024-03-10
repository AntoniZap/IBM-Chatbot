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


  const handleSendMessage = async () => {
    setLoading(() => true);
    try {
        if (Object.keys(answers).length === 0) {
        // no LLM response to select, proceed.
      } else {
        const llm = document.querySelector('input[name="g1"]:checked')?.value;
        if (llm === undefined) {
          throw Error("Not proceeding without llm chosen");
        } else {
          try {
            await axios.post('/selectAnswer', { llm })
          } catch(error) {
            console.error('Error selecting answer:', error);
            return;
          }
          setChatHistory(chatHistory => [...chatHistory, { sender: 'bot', message: answers[llm].answer }]);
          setAnswers(answers => ({}));
        }
      }

        const llms = [...document.querySelectorAll('[name="g2"]:checked')].map((input) => input.value);

      await axios.post('/message', {message: message, llms })
        .then(response => {
          setChatHistory(chatHistory => [...chatHistory, { sender: 'user', message: message }]);
          setAnswers(Object.fromEntries(response.data.map(answer => [answer.llm, answer])));
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    } catch (e) {
      if (e instanceof Error) alert(e);
    }
    setLoading(() => false);
  };
    
  return (
      <div style={{display: "flex",
                   flexDirection: "column",
                   height: "50%",
                   maxHeight: "50%"}}>
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
                                    <input defaultChecked={index == 0} value={msg.llm} id={"..."+index} type="radio" name="g1"/>
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

          <div style={{color: "black"}}>
          <h2>Enabled LLMs</h2>
          <p>These LLMs will be included in the response</p>
          {["llama", "chatgpt", "ai21"].map((ai, index) => (
              <>
                  <label id={".#."+index}><input value={ai} type="checkbox" name="g2"/> {ai}</label>
                  <br/>
              </>
          ))}
          </div>
      </div>
      <div>
      <input type="text" value={message} onChange={handleInputChange} />
          <button onClick={handleSendMessage} disabled={loading}>Send</button>
          </div>
    </div>
  );
}

export default ChatWithMe;

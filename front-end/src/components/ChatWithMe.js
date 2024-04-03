import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Bot from '../assets/bot.png';
import User from '../assets/user.png';
import Star from '../assets/star.png';
import ExampleQuestions from '../assets/ExampleQuestions.png'; // Import the ExampleQuestions.png image
import RatingLLms from './RatingLLms.js';
import './ChatWithMe.css'; // Import the CSS file
import ReactPaginate from 'react-paginate';

import io from 'socket.io-client'
const socket = io('http://localhost:5000');
const validLLMs = ["llama", "chatgpt", "ai21"];

const AnswerBody = ({ answer, paginationRef }) => {
    if (answer.type == "tabular") {
        const [page, setPage] = useState(0);
        const pageCount = Math.ceil(answer.results.length / 10);
        const pagination = pageCount <= 1
              ?  undefined
              : <ReactPaginate
                    breakLabel="…"
                    previousLabel="◄"
                    nextLabel="►"
                    pageClassName="page-class"
                    onPageChange={async (event) => setPage(event.selected) }
                    marginPagesDisplayed={1}
                    pageRangeDisplayed={1}
                    pageCount={pageCount}
                    containerClassName="page-container-class"
                />;
        
        if (paginationRef !== undefined) {
            paginationRef.current = pagination;
        }

        return <div>
                   <table>
                       <tr>
                           {answer.column_names.map(name => <td><span>{name}</span></td>)}
                       </tr>
                       {answer.results.slice(page, page + 10).map(result => <tr>{result.map(r => <td><span>{r}</span></td>)}</tr>)}
                   </table>
                   {paginationRef === undefined && pagination}
               </div>;
    } else {
        const text = (typeof answer === "string" || answer instanceof String)
              ? answer
              : answer.answer;
        return <text>{text?.trim() ?? <span style={{color: "red"}}>No data! {JSON.stringify(answer)}</span>}</text>;
    }
}

const Bubble = ({ sender, message, className, llm, ...props }) => {
    const paginationRef = useRef(undefined);
    return <div className={`message ${className ?? ""}`} {...props}>
               <div className={`${sender}`}>
                   <img src={sender === 'user' ? User : Bot} alt={`${sender} icon`} className="user-icon"/>
                   <AnswerBody answer={message} paginationRef={paginationRef}/>
               </div>
               <center>{paginationRef.current}</center>
           </div>;
}

function ChatWithMe() {
    axios.defaults.baseURL = 'http://localhost:5000';
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [answers, setAnswers] = useState({});
    const [sources, setSources] = useState([]);
    const [best_llm, setBestLLM] = useState([]);
    const [processingUserMessage, setProcessingUserMessage] = useState(false);
    const [llmRatings, setLlmRatings] = useState({});
    const [showImage, setShowImage] = useState(true); // New state for showing image

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

    const Answer = ({
        index,
        onRatingChange,
        type,
        llm,
        best_llm,
        ...props
    }) => {
        const body = <AnswerBody answer={{...props, type}}/>;
        const isBestLLM = best_llm.includes(llm);
        const sourceBody = type == "tabular"
              ? <>
                    <h4>generated query</h4>
                    <pre style={{whiteSpace: "normal"}}>{props.query}</pre>
                </>
        : (sources.length > 0 && (
            <>
                <h3>Sources</h3>
                { sources.map((source, index) => (
                    <>
                        <p><strong>Product:</strong> {source.productName}<br/>
                        <strong>Rating:</strong> {source.rating ?? "N/A"}</p>
                        <blockquote className="source-quote" key={index}>{source.pageContent}</blockquote>
                    </>)) }
            </>));
        return <div {...props}>
                   <label className="llm-sub-container">
                       <input defaultChecked={index == 0} value={llm} id={"..."+index} type="radio" name="g1"/>
                       <center>
                           <h4>{llm}</h4>
                           {body}
                           <RatingLLms llm={llm} onRatingChange={onRatingChange} />
                           {isBestLLM && <img src={Star} alt="Star Icon" className="star"/>}
                       </center>
                   </label>
                   <label className="llm-sub-container">
                       <input type="checkbox"/>
                       <div className="source-body-source">
                           <p>▼ Hide sources</p>
                           {sourceBody}
                       </div>
                       <span className="source-body-no-source">➤ Show sources</span>
                   </label>
               </div>;
    }

    const handleInputChange = (event) => {
        setMessage(event.target.value);
    }

    const handleSendMessage = async (event) => {
        event.preventDefault();
        setProcessingUserMessage(() => true);
        setShowImage(false); // Hide image when sending message
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
                    setChatHistory(chatHistory => [...chatHistory, { sender: 'bot', message: answers[llm] }]);
                    setAnswers(answers => ({}));
                }
            }

            const llms = [...document.querySelectorAll('[name="g2"]:checked')].map((input) => input.value);
            const sql = document.querySelector('#sql-checkbox')?.checked;

            await axios.post('/message', {message: message, llms, sql })
                .then(response => {
                    setChatHistory(chatHistory => [...chatHistory, { sender: 'user', message: { answer: message } }]);
                    setAnswers(Object.fromEntries(response.data.answers.map(answer => [answer.llm, answer])));
                    setSources(response.data.sources);
                    setBestLLM(response.data.best_llm);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        } catch (e) {
            if (e instanceof Error) alert(e);
        }
        setProcessingUserMessage(() => false);
    };

    const handleRatingChange = (llm, rating) => {
        setLlmRatings(prevState => ({
            ...prevState,
            [llm]: rating
        }));
    };
    
    return (
        <div className="master">
            <div className="options-pane">
                <h2>Enabled LLMs</h2>
                <p>These LLMs will be included in the response</p>
                {validLLMs.map((ai, index) => (
                    [<label key={`enabled-llm.${ai}.${index}`}><input value={ai} type="checkbox" name="g2"/> {ai}</label>, <br/>]
                ))}
                <br/>
                <h2>Enabled Tools</h2>
                <p>These tools will be used in the LLM response</p>
                <div>
                    <label>
                        <input value="sqla" id="sql-checkbox" type="checkbox"/>Table Aggregation Tool - <small>If a question benefits from aggregations over the whole database, the agent will attempt to perform such an aggregation and return a table representing the result.</small>
                    </label>
                    <br/>
                </div>
            </div>
            <div className="messages-pane">
                {showImage && <img src={ExampleQuestions} alt="Example Questions" />} {/* Image shown before message sent */}
                <div style={{flex: "1 1 0", overflow: "scroll"}}>
                    <div className="message-bubble">
                        { chatHistory.map((msg, index) => <Bubble {...msg}/>) }
                        { processingUserMessage && <Bubble className="loading" sender="user" message={message}/> }
                    </div>
                    {
                        (Object.keys(answers).length > 0) && (
                            <>
                                <h3>Answers</h3>
                                <div className="llm-container-box">
                                    {
                                        Object.values(answers).map((msg, index) => 
                                            <Answer
                                                key={`answer.${index}.${msg.llm}`}
                                                className={processingUserMessage ? "processingUserMessage llm-container" : "llm-container" }
                                                index={index}
                                                onRatingChange={handleRatingChange}
                                                {...msg}/>)
                                    }
                                </div>
                            </>
                        )
                    }
                </div>
                <form className="input-form" onSubmit={handleSendMessage} >
                    <textarea placeholder="Ask your question here…" onChange={handleInputChange} />
                    {" "}
                    <input type="submit" disabled={processingUserMessage} value="→"/>
                </form>
            </div>
        </div>
    );
}

export default ChatWithMe;

import React from 'react';
import './InsertApiKey.css';
import {useState} from 'react';
import login from './images/Login1.png'


function InsertApiKey() {
    const [apiKey, setApiKey] = useState("Enter your OpenAI API Key Here")
    const click = () => {
        alert(apiKey)
    }
    const change = () => {
        setApiKey(event.target.value)
    }
    return(
        <div className = "openai-card">
            <div className = "hello"> 
                <header>
                 <h1 className="header-api">Insert your OpenAI Api Key Here</h1>
                 <h2 className="h2-api">Already have an OpenAi Api Key?</h2>
                </header>
                <p className= "phase1-OpenAi">Insert it below to get going, otherwise find and follow our quick and easy tutorial below!</p>
                <input type="text" className = "input-val" onChange = {change} value = {apiKey}/>
                <button className = "API-button" onClick = {click}>Upload Api Key</button>
            </div>
            <div className = "tutorial-OpenAi">
                <header>
                    <h2 className="stepBystep-tutorial">OpenAI API Key Step-by-Step Tutorial:</h2>
                </header>
                <h3 className = "step-1">Step 1: Click on the link below</h3>
                <a href = "https://openai.com/" className = "OpenAi-button">OpenAI</a>
                <h3 className = "step-1">Step 2: Login to your OpenAi Account/Sign Up if you don&apos;t already have an OpenAi Account</h3>
                <p className = "para-1">See the image below, click on the highlighted and boxed login feature.</p>
                <img className = "login-image" src = {login} alt = 'loginButtonImage'></img>
               
            </div>
        </div>
    );
}

export default InsertApiKey;
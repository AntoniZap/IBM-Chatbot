import React from 'react';
import './InsertApiKey.css';
import {useState} from 'react';
import login from './images/Login1.png'
import apiSelect from './images/apiselect.png'

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
                <h3 className = "step-1">Step 1: Click on the button below to access the OpenAI website</h3>
                <a className='OpenAi-href' href = "https://openai.com/">
                    <button className = "OpenAi-button">
                        OpenAI
                    </button>
                </a>
                <h3 className = "step-2">Step 2: Login to your OpenAi Account/Sign Up if you don&apos;t already have an OpenAi Account</h3>
                <p className = "para-1">To login, click on the highlighted and boxed login feature on the OpenAI website (See image below).</p>
                <img className = "login-image" src = {login} alt = 'loginButtonImage'></img>
                <h3 className = "step-2">Step 3: Once you have logged into your OpenAI account select API</h3>
                <p className = "para-1">(See image below).</p>
                <img className = "api-select-image" src = {apiSelect} alt = 'selectAPIImage'></img>

               
            </div>
        </div>
    );
}

export default InsertApiKey;
import React from 'react';
import './InsertApiKey.css';
import {useState} from 'react';
import login from './images/Login1.png'
import apiSelect from './images/apiselect.png'
import apiKeySelect from './images/APIKeyFinder.png'
import openailogo from './images/openailogo.png'
import createSecretApiKey from './images/createapikey.png'


function InsertApiKey() {
    const [apiKey, setApiKey] = useState("Enter your OpenAI API Key Here")
    const click = () => {
        alert(apiKey);
    }
    const change = () => {
        setApiKey(event.target.value)
    }
    return(
        <div>
            <div className = "openai-card"> 
                <header>
                 <h1 className="header-api">How to insert your OpenAI API Key</h1>
                 <h2 className="h2-api">Already have an OpenAi API Key?</h2>
                </header>
                <p className= "phase1-OpenAi">Insert it below to get going, otherwise follow our quick and easy tutorial below!</p>
                <input type="text" className = "input-val" onChange = {change} value = {apiKey}/>
                <button className = "API-button" onClick = {click}>Upload Api Key</button>
            </div>
            <div className = "tutorial-OpenAi">
                <header>
                    <h2 className="stepBystep-tutorial">Step-by-Step Tutorial on obtaining an OpenAI API Key:</h2>
                </header>
                <h3 className = "step-1">Step 1: Navigate to the OpenAI Website</h3>
                <p className = "para-1">Click on the following link to navigate to the OpenAI website: <a className='OpenAi-href' href = "https://openai.com/">OpenAI</a></p>
                <h3 className = "step-2">Step 2: Login to Your OpenAI Account/Sign Up</h3>
                <p className = "para-1">To login, locate the highlighted and boxed login feature on the OpenAI website and click on it (See image below).</p>
                <img className = "login-image" src = {login} alt = 'loginButtonImage'></img>
                <p className = "para-1">If you already have an OpenAI account, proceed to login. If you don&apos;t have an account, sign up for one by following the prompts on the website.</p>
                <h3 className = "step-2">Step 3: Access the API Section</h3>
                <p className = "para-1">Once you have logged into your OpenAI account select API (See image below).</p>
                <img className = "api-select-image" src = {apiSelect} alt = 'selectAPIImage'></img>
                <h3 className = "step-2">Step 4: Access API Keys</h3>
                <p className = "para-1">Hover over the <img className = "openai-logo" src = {openailogo} alt = 'openai-logo'></img> icon in the top left hand corner and select the API keys tab from the dropdown menu (See image below).</p>
                <img className = "api-select-image" src = {apiKeySelect} alt = 'selectAPIKeyTab'></img>
                <h3 className = "step-2">Step 5: Create a New Secret Key</h3>
                <p className = "para-1">Within the API keys section, locate the &quot;create new secret key&quot; button. Click on this button to generate a new API key (See image below).</p>
                <img className = "api-select-image" src = {createSecretApiKey} alt = 'createSecretApiKey'></img>
                <h3 className = "step-2">Step 6: Copy Your API Key</h3>
                <p className = "para-1">After generating the new API key, it will be displayed on the screen. Copy your newly created secret OpenAI API key and return to the top of this page to insert it into the upload box.</p>

            </div>
        </div>
    );
}

export default InsertApiKey;
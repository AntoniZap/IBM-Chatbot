import React from 'react';
import './InsertApiKey.css';
import {useState} from 'react';
import ai21login from './images/loginai21.png'
import apiSelect from './images/apiselectai21.png'
import ai21profilelogo from './images/profileai21.png'


function InsertAI21API() {
    const [aiapiKey, setaiApiKey] = useState("Enter your AI21 API Key Here")
    const click = () => {
        alert(aiapiKey)
    }
    const change = () => {
        setaiApiKey(event.target.value)
    }
    return(
        <div>
            <div className = "openai21-card"> 
                <header>
                 <h1 className="header-api">How to insert your AI21 API Key</h1>
                 <h2 className="h2-api">Already have an AI21 API Key?</h2>
                </header>
                <p className= "phase1-OpenAi">Insert it below to get going, otherwise follow our quick and easy tutorial below!</p>
                <input type="text" className = "input-val" onChange = {change} value = {aiapiKey}/>
                <button className = "API-button" onClick = {click}>Upload Api Key</button>
            </div>
            <div className = "tutorial-OpenAi21">
                <header>
                    <h2 className="stepBystep-tutorial">Step-by-Step Tutorial on obtaining an AI21 API Key:</h2>
                </header>
                <h3 className = "step-3">Step 1: Navigate to the AI21 Website</h3>
                <p className = "para-1">Click on the following link to navigate to the AI21 website: <a className='OpenAi-href' href = "https://www.ai21.com/studio?ad_set_name=AI21_Studio&utm_source=google-search&utm_medium=cpc&utm_campaign=Studio_Search_US_EN_Singup_Branded&utm_term=ai21%20labs&hsa_acc=2867715215&hsa_cam=17786983346&hsa_grp=134207891690&hsa_ad=611028610528&hsa_src=g&hsa_tgt=kwd-1968951467697&hsa_kw=ai21%20labs&hsa_mt=b&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=CjwKCAjw17qvBhBrEiwA1rU9w8i7Z8qwhbP9zIiN4k4kH--NPnNNS7dT_1I1IobtkO9ru5yS2uF7wRoCkzAQAvD_BwE">AI21</a></p>
                <h3 className = "step-3">Step 2: Login to Your OpenAI Account/Sign Up</h3>
                <p className = "para-1">To login, locate the highlighted and boxed login feature on the OpenAI website and click on it (See image below).</p>
                <img className = "login-image" src = {ai21login} alt = 'loginButtonImage'></img>
                <p className = "para-1">If you already have an OpenAI account, proceed to login. If you don&apos;t have an account, sign up for one by following the prompts on the website.</p>
                <h3 className = "step-3">Step 3: Access the API Section</h3>
                <p className = "para-1">Click on the <img className = "openai-logo" src = {ai21profilelogo} alt = 'ai21-profile-logo'></img> icon in the top right hand corner and select the API keys tab from the dropdown menu (See image below).</p>
                <img className = "api-select-image" src = {apiSelect} alt = 'selectAPIKeyTab'></img>
                <h3 className = "step-3">Step 4: Copy Your API Key</h3>
                <p className = "para-1">After selecting the API Key tab from the dropdown menu you will find the new API key, it will be displayed on the screen. </p>
                <p className = "para-1">Copy your newly created secret AI21 API key and return to the top of this page to insert it into the upload box.</p>

            </div>
        </div>
    );
}

export default InsertAI21API;
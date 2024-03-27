import './LandingPage.css'
import ChatwithmePicture from './images/chatwithme.png'
import APIKeyImage from './images/apiKeyhome.png'
import uploadDocImage from './images/uploadDocs.png'
import getChatting from './images/getChatting.png'
import { Link } from "react-router-dom";
import InsertApiKey from './InsertApiKey';
import ChatWithMe from './ChatWithMe';
import InsertDocument from './InsertDocument';

function LandingPage() {
    const workData = [
        {
            image: APIKeyImage,
            title: "1. Insert your API Keys",
            text: "In the first step, securely insert your AI21 and OpenAI API keys into FeedBot. These keys enable FeedBot to access advanced natural language processing capabilities, empowering it to understand and analyze customer reviews effectively.",
            link: "/openai-api-key",
            buttontext: "Insert Your API Key Here"
        },
        {
            image: uploadDocImage,
            title: "2. Upload your Document",
            text: "Next, upload your CSV documents containing customer feedback data directly to FeedBot.",
            link: "/insert-document",
            buttontext: "Upload Your Documents Here"
        },
        {
            image: getChatting,
            title: "3. Get Chatting",
            text: "Once your API keys are integrated, and your data is uploaded, it's time to start chatting with FeedBot! Interact with FeedBot to explore insights, analyze opinions, and extract valuable information from customer reviews.",
            link: "/chat-with-me",
            buttontext: "Start Chatting Here"
        }
    ]

    return (
        <div className = "home-page">
            <div className= "heading-main">
                <h1 className = "landing-page-headline">Discover the Possibilities of AI-powered Conversations with FeedBot</h1>
                <p className = "sub-headline">Group 21 welcome's you to FeedBot! Your Customer Review Assistant.</p>
                <img src = {ChatwithmePicture} alt = "chatwithme" className = "chatwithme-image"></img>
            </div>
            <div className="about-container">
                <h2 className="about-header">About</h2>
                <h2>Discover how FeedBot revolutionizes your customer feedback experience</h2>
                <p className="heading-text">FeedBot allows users to navigate customer feedback reviews seamlessly and effectively. It aims to aid in your choice of product and ensure you are
                        well informed before your purchase. </p>
                <p className="heading-text">It does this by enabling the user to ask questions and unlock insights from customer reviews using AI driven technology. Users benefit from well-crafted responses as FeedBot leverages <a href="https://elastic.co/what-is/large-language-models">Large Language Models</a> such as ChatGPT, AI21, and LLAMA. </p>
            </div>
            <div className="howitworks-section">
                <div className="howitworks-section-top">
                    <h1 className="heading-section2">How FeedBot Works</h1>
                </div>
                <h2 className= "sub-heading">Follow these 3 steps quick and easy steps:</h2>
                <div className="howitworks-section-bottom">
                    {workData.map((data) => (
                     <div className="howitworks-section-info" key={data.title}>
                        <div className="info-boxes-img-container">
                          <img className = "image-info" src={data.image} alt="" />
                        </div>
                        <h2>{data.title}</h2>
                        <p>{data.text}</p>
                        <Link className="link-api-key" to={data.link}><button className = "button-card">{data.buttontext}</button></Link>
                     </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default LandingPage
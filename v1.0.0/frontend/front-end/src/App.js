import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import InsertDocument from './components/InsertDocument';
import ChatWithMe from './components/ChatWithMe';
import AboutUs from './components/AboutUs';
import logo from './logo.svg';
import 'bootstrap/dist/css/bootstrap.css';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <div className="container-fluid d-flex justify-content-center align-items-center vh-100">
          <div className="cover-container">
            <header className="masthead mb-auto">
              <div className="inner">
                <h3 className="masthead-brand">Group 21 AI Chatbot</h3>
                <nav className="nav nav-masthead justify-content-center">
                  <Link className="nav-link" to="/">Home</Link>
                  <Link className="nav-link" to="/insert-document">Insert Document</Link>
                  <Link className="nav-link" to="/chat-with-me">Chat With Me</Link>
                  <Link className="nav-link" to="/about-us">About Us</Link>
                </nav>
              </div>
            </header>

            <main role="main" className="inner cover">
              <Routes>
                <Route path="/" element={
                  <>
                    <h1 className="cover-heading">Welcome to Group 21's AI chatbot</h1>
                    <p className="lead">Welcome to the Chatbot designed by Group 21 as part of our work with IBM and Large Language Models. Just insert your document and ask as many questions as you want!</p>
                    <p className="lead">
                      <a href="https://elastic.co/what-is/large-language-models" className="btn btn-lg btn-secondary">Learn more</a>
                    </p>
                  </>
                } />
                <Route path="/insert-document" element={<InsertDocument />} />
                <Route path="/chat-with-me" element={<ChatWithMe />} />
                <Route path="/about-us" element={<AboutUs />} />
              </Routes>
            </main>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;

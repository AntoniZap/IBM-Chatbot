import React from 'react';
import logo from './logo.svg';
import 'bootstrap/dist/css/bootstrap.css';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="container-fluid d-flex justify-content-center align-items-center vh-100">
        <div className="cover-container">
          <header className="masthead mb-auto">
            <div className="inner">
              <h3 className="masthead-brand">Group 21 AI Chatbot</h3>
              <nav className="nav nav-masthead justify-content-center">
                <a className="nav-link active">Insert Document</a>
                <a className="nav-link">Chat With Me</a>
                <a className="nav-link">Home</a>
              </nav>
            </div>
          </header>

          <main role="main" className="inner cover">
            <h1 className="cover-heading">Welcome to Group 21's AI chatbot</h1>
            <p className="lead">Welcome to the Chatbot designed by Group 21 as part of our work with IBM and Large Language Models. Just insert your document and ask as many questions as you want!</p>
            <p className="lead">
              <a href="https://elastic.co/what-is/large-language-models" className="btn btn-lg btn-secondary">Learn more</a>
            </p>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;

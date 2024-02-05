import streamlit

import os

os.environ["OPENAI_API_KEY"] = ""
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(temperature = 0.6)

title = streamlit.title("Q&A Chatbot")
prompt = streamlit.subheader("Select options in sidebar")

language = streamlit.sidebar.selectbox("Select language / Roghnaigh teanga:", ("English", "Gaeilge"))




if language:
    global language_context
    if language == "English":
        global llm_selection
        language_context = ""
        # print("English selected")
        title.empty()
        title = streamlit.title("IBM Q&A Chatbot")
        prompt.empty()
        prompt = streamlit.subheader("Select options in sidebar.")
        llm_selection = streamlit.sidebar.selectbox("Select LLM:", ("","OpenAI", "Google", "Meta", "IBM"))
    elif language == "Gaeilge":
        language_context = ". Freagair as Gaeilge. Answer in Irish."
        # print("Gaeilge roghnaithe")
        llm_selection = streamlit.sidebar.selectbox("Roghnaigh LLM:", ("","OpenAI", "Google", "Meta", "IBM"))
        title.empty()
        title = streamlit.title("Bota Comhrá C⁊F IBM")
        prompt.empty()
        prompt = streamlit.subheader("Roghnaigh roghanna ar an dtaobhbharra.")

def answer_question(question, key):
    if question:
        print('Question: "' + question + '"')
        open_ai_answer = ""
        with streamlit.spinner('Loading...'):
            open_ai_answer = llm.invoke(question + language_context).content
        streamlit.text_area(llm_selection + ":",
            open_ai_answer,
            disabled = True,
            key = "answer " + str(key)
            )
        if language == "English":
            answer_question(streamlit.text_input("You:", placeholder="Write your question...", key = "response " + str(key)), key + 1)
        elif language == "Gaeilge":
            answer_question(streamlit.text_input("Tusa:", placeholder="Clóscríobh do theachtaireacht...", key = "response " + str(key)), key + 1)

if llm_selection:
    # print(llm_selection + " selected")
    if llm_selection == "OpenAI":
        prompt.empty()
        questions = []
        if language == "English":
            question = streamlit.text_input("You:", placeholder="Write your question...")
            answer_question(question, 1)
        elif language == "Gaeilge":
            question = streamlit.text_input("Tusa:", placeholder="Clóscríobh do theachtaireacht...")
            answer_question(question, 1)
        
    else:
        prompt.empty()
        if language == "English":
            prompt = streamlit.subheader("Unfortunately " + llm_selection + "'s LLM is not available at the moment.")
        elif language == "Gaeilge":
            prompt = streamlit.subheader("Faraor, níl MML " + llm_selection + " ar fáil faoi láthair.")



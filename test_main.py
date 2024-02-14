#UNIT TESTS

#Don't remove these imports
import ChatbotHelper
import config
import os

#TODO CREATE TESTS
def test_get_db():
    ChatbotHelper.get_db()
    assert 2 + 2 == 4

def test_get_llm_ChatOpenAI():                                  # Check that ChatOpenAI is obtained correctly
    os.environ['LLM'] = "CHATGPT"                               # Load 'CHATGPT' as the LLM selection
    from langchain_openai import ChatOpenAI
    llm = ChatbotHelper.get_llm()
    assert isinstance(llm, ChatOpenAI)
    del os.environ['LLM']

#def test_get_llm_LLAMA():                                     # Check that LLAMA is obtained correctly
#    os.environ['LLM'] = "LLAMA"                               # Load 'LLAMA' as the LLM selection
#    llm = ChatbotHelper.get_llm()
#    assert hasattr(llm, 'model_path')
#    assert llm.model_path == os.getenv('LLAMA_MODEL_PATH')
#    del os.environ['LLM'] 

def test_get_llm_AI21():                                     # Check that AI21 is obtained correctly
    os.environ['LLM'] = "AI21"                               # load 'AI21' as the LLM selection
    llm = ChatbotHelper.get_llm()
    from langchain.llms import AI21
    assert isinstance(llm, AI21)
    del os.environ['LLM']                                   

def test_get_memory():                                      # Check that the chat history is loaded correctly
    from langchain.memory import ChatMessageHistory
    assert ChatbotHelper.get_memory() == ChatMessageHistory()        

def test_get_memory_unique():                               # Check that calling the function multiple times does not change the result
    memory1 = ChatbotHelper.get_memory()
    memory2 = ChatbotHelper.get_memory()
    assert memory1 == memory2               
    

def test_get_options():
    assert 2 + 2 == 4


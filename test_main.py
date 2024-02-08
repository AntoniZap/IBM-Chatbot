#UNIT TESTS
import ChatbotConcept
import config


#Need to import function that's used in the tests
#from ChatbotConcept import *


def test_basic_example():
    assert 2 + 2 == 4

def test_get_db():
    import os
    config.config()
    a = os.getenv("LLM")
    b = os.getenv("LLAMA_MODEL_PATH")
    c = os.getenv("OPENAI_API_KEY")
    d = os.getenv("AI21_API_KEY")
    ChatbotConcept.get_db()
    assert 2 + 2 == 4

def test_get_llm():
    assert 2 + 2 == 4

def test_get_memory():
    assert 2 + 2 == 4



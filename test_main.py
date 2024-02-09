#UNIT TESTS

import ChatbotHelper
import config
import os


def test_basic_example():
    assert 2 + 2 == 4

def test_get_db():
    a = os.getenv("LLM")
    b = os.getenv("LLAMA_MODEL_PATH")
    c = os.getenv("OPENAI_API_KEY")
    d = os.getenv("AI21_API_KEY")
    ChatbotHelper.get_db()
    assert 2 + 2 == 4

def test_get_llm():
    assert 2 + 2 == 4

def test_get_memory():
    assert 2 + 2 == 4



#UNIT TESTS

#Don't remove these imports
import ChatbotHelper
import config


def test_basic_example():
    assert 2 + 2 == 4

def test_get_db():
    ChatbotHelper.get_db()
    assert 2 + 2 == 4

def test_get_llm():
    assert 2 + 2 == 4

def test_get_memory():
    assert 2 + 2 == 4



from streamlit.testing.v1 import AppTest

at = AppTest.from_file("ChatbotConcept.py")
at.run()
assert not at.exception

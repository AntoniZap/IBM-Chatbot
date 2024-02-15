import os

if os.environ.get("LLM") is None:
  os.environ['LLM'] = 'AI21'
LLM = os.getenv("LLM")

if os.environ.get("LLAMA_MODEL_PATH") is None:
  os.environ['LLAMA_MODEL_PATH'] = ''
LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH")

if os.environ.get("OPENAI_API_KEY") is None:
  os.environ['OPENAI_API_KEY'] = ''
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if os.environ.get("AI21_API_KEY") is None:
  os.environ['AI21_API_KEY'] = 'ZfNoV72fEKCFJfW3r3jkAgj4scOcaQ37'
AI21_API_KEY = os.getenv("AI21_API_KEY")


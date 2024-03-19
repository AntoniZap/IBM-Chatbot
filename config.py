import os

if os.environ.get("LLM") is None:
  os.environ['LLM'] = 'AI21'
LLM = os.getenv("LLM")

if os.environ.get("LLAMA_MODEL_PATH") is None:
  os.environ['LLAMA_MODEL_PATH'] = ''
LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH")

if os.environ.get("AI21_API_KEY") is None:
  os.environ['AI21_API_KEY'] = 'xGf4pLrLFNdn3mAPWIo6Gd6qhHOZUQxI'
AI21_API_KEY = os.getenv("AI21_API_KEY")


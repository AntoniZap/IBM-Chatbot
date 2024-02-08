import os

if os.environ.get("LLM") is None:
  os.putenv("LLM", "CHATGPT")
LLM = os.getenv("LLM")

if os.environ.get("LLAMA_MODEL_PATH") is None:
  os.putenv("LLAMA_MODEL_PATH", "")
LLM = os.getenv("LLAMA_MODEL_PATH")

if os.environ.get("OPENAI_API_KEY") is None:
  os.putenv("OPENAI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if os.environ.get("AI21_API_KEY") is None:
  os.putenv("AI21_API_KEY", "")
AI21_API_KEY = os.getenv("AI21_API_KEY")


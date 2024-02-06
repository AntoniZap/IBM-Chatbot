Software Engineering Project - Group 21
---------------------------------------------------------------------------------------------------------------------------------------------
<img src="image.png" alt="Alt text" width="15" height="15"/> Customer Review Q+A ChatBot

An Overview of Project 30 - 
--------------------------------------------------------------------------------------------------------------------------------------------  
3️⃣ Third Years
 - Della Doherty (dohertd6@tcd.ie) - ICS
 - Darragh Clifford (dcliffor@tcd.ie) - ICS
 - Antoni Zapedowski (zapedowa@tcd.ie) - ICS
 - Chinaza Uzoukwu (uzoukwuc@tcd.ie) - ICS
 - Sprina Chen (chensp@tcd.ie) - CSB
 - Jaedon Paget (pagetj@tcd.ie) - ICS

2️⃣ Second Years
 - Sean Conway (SECONWAY@tcd.ie) -
 - Emmelia Klefti (kleftie@tcd.ie) -
 - Nicholas Horvat (horvatn@tcd.ie) -
 - Lorca Brannigan (Lbrannig@tcd.ie) -
 - Dylan Martin (martindy@tcd.ie) -

# ibm-sweng

# chinaza/RAG-chromadb

## Setup

Reccomended CPU prerequisite setup.

```
python3 -m venv env
. env/bin/activate
pip3 install torch --index-url https://download.pytorch.org/whl/cpu
pip3 install -r requirements.txt
```

Failing to install torch the way described above may result in your VENV being populated with NVIDIA drivers that you likely do not need.
If you do have an nvidia GPU, feel free to ommit the explicit torch install, as you may be able to run the code faster with CUDA.

Download the "Datafiniti" CSV file from [here](https://data.world/datafiniti/consumer-reviews-of-amazon-products).
Place it in the project root driectory.
The program will for a csv with the name `Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv` in the directory in which it is invoked.

You need to modify `.env.template`.
If you are using LLaMa set the `LLM` environment variable to `LLAMA` and make sure that the `LLAMA_MODEL_PATH` environment variable points to the `gguf` files corresponding to the model that you want to use.
If you are using chatgpt, make sure you set the `LLM` environment variable to `CHATGPT` and set `OPENAI_API_KEY` to your OpenAI API key.

## Running

```
. .env.template
streamlit run ChatbotConcept.py
```

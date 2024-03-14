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

## Setup

Reccomended CPU prerequisite setup.

```
python3 -m venv env
. env/bin/activate
pip3 install torch --index-url https://download.pytorch.org/whl/cpu
pip3 install -r requirements.txt
pip3 install sentence_transformers
pip3 install langchain_openai
```

Failing to install torch the way described above may result in your VENV being populated with NVIDIA drivers that you likely do not need.
If you do have an nvidia GPU, feel free to ommit the explicit torch install, as you may be able to run the code faster with CUDA.

Download the "Datafiniti" CSV file from [here](https://data.world/datafiniti/consumer-reviews-of-amazon-products).
Place it in the project root driectory.
The program will for a csv with the name `Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv` in the directory in which it is invoked.

You need to modify `config.py`.
If you are using LLaMa make sure that the `LLAMA_MODEL_PATH` environment variable points to the `gguf` files corresponding to the model that you want to use.
If you are using chatgpt, set `OPENAI_API_KEY` to your OpenAI API key.
If you are using AI21 llm, set `AI21_API_KEY` to your AI21 API key.

## Running the Backend

Run the app.py file within your IDE, or alternatively within your terminal run:

```
python3 app.py
```

Please run the commands using bash, rather than powershell as it might not work using powershell (windows devices).

## Running the Frontend

Navigate to the `front-end` folder and setup prerequisites via:

```
npm install
```

You can then run the frontend using the command.

```
npm run start
```

Please note that the frontend should be run in a terminal seperate from the backend.

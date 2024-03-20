Software Engineering Project - Group 21
---------------------------------------------------------------------------------------------------------------------------------------------
<img src="LogoText.svg" alt="Alt text" width="15" height="15"/> Customer Review Q+A ChatBot

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
 - Sean Conway (SECONWAY@tcd.ie) - ICS
 - Emmelia Klefti (kleftie@tcd.ie) - ICS
 - Nicholas Horvat (horvatn@tcd.ie) - ICS
 - Lorca Brannigan (Lbrannig@tcd.ie) - CSB
 - Dylan Martin (martindy@tcd.ie) - ICS

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
If you do have an Nvidia GPU, feel free to omit the explicit torch install, as you may be able to run the code faster with CUDA.

To get a sample of data download the "Datafiniti" CSV file from [here](https://data.world/datafiniti/consumer-reviews-of-amazon-products).
Place it in the project root directory.
The program will for a CSV with the name `Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv` in the directory in which it is invoked.

To chat with the bot, the user will need to provide a way to connect with an LLM - either an API key, or path.
API keys for OPENAI GPT and AI21 can be inserted into the program. Instruction on how to find them is available once the application is run. 
Please modify .env.template to put the LLAMA path if you wish to use LLAMA LLM. 

## Running the Backend

You can run the app.py including .env.template which will include the environment variables for LLMs and others (or
you can provide AI21 and GPT keys while the app is running). 

## Running the Frontend

Navigate to the `front-end` folder and setup prerequisites via - this command needs to be executed only once:

```
npm install
```

Once npm is installed you can then run the frontend using the command:

```
npm run start
```

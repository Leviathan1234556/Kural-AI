import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from flask import Flask, request, render_template
from langchain_ollama import OllamaLLM
import requests
import gtts

requests.get('https://api.smith.langchain.com', timeout=10)

# Load environment variables from .env file
load_dotenv()

# Directly assign the API key here
API_KEY = "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"

# Set environment variables for langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Create Flask app
app = Flask(__name__)

# Define chatbot initialization
def initialize_chatbot():
    
    # Initialize OpenAI LLM and output parser
    llm = OllamaLLM(model="tamil-llama2:latest")
    output_parser = StrOutputParser()
    
    # Create chain
    chain = llm 
    return chain

# Initialize chatbot
chain = initialize_chatbot()

# Define route for home page
import logging

logging.basicConfig(level=logging.DEBUG)
def clean_response(response):
    # Remove unwanted step-by-step content
    steps_indicators = ["Step 1", "Step 2", "Step 3"]
    for indicator in steps_indicators:
        if indicator in response:
            response = response.split(indicator, 1)[0].strip()  # Keep only the part before step explanations
    return response

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'input_text' in request.form:  # Check if 'input_text' is present in form data
            input_text = request.form['input_text']
            if input_text:
                logging.debug(f"Input text: {input_text}")
                output = chain.invoke(input_text)
                logging.debug(f"Output: {output}")
                cleaned_output = clean_response(output)
                tts = gtts.gTTS(text=cleaned_output, lang='ta')
                tts.save("kural.mp3")
                os.system("kural.mp3")
                return render_template('index.html', input_text=input_text, output=cleaned_output)
        else:
            logging.debug("input_text not found in form data")
            return render_template('index.html', error="No input text provided.")
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

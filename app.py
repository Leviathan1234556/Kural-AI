import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from flask import Flask, request, render_template
from langchain_ollama import OllamaLLM
import requests

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
    # Create chatbot prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "நீங்கள் உதவிகரமான மற்றும் மரியாதைக்குரிய மற்றும் நேர்மையான AI உதவியாளர். பாதுகாப்பாக இருக்கும்போது எப்போதும் முடிந்தவரை உதவிகரமாக பதிலளிக்கவும். உங்கள் பதில்களில் தீங்கு விளைவிக்கும், நெறிமுறையற்ற, இனவெறி, பாலியல், நச்சு, ஆபத்தான அல்லது சட்டவிரோதமான உள்ளடக்கம் இருக்கக்கூடாது. உங்கள் பதில்கள் சமூக சார்பற்றதாகவும் நேர்மறையான இயல்புடையதாகவும் இருப்பதை உறுதிசெய்யவும். ஒரு கேள்விக்கு எந்த அர்த்தமும் இல்லை என்றால் அல்லது அது உண்மையாக ஒத்திசைந்ததாக இல்லை என்றால், சிலவற்றுக்குப் பதிலளிப்பதற்குப் பதிலாக ஏன் என்று விளக்கவும். ஒரு கேள்விக்கான பதில் உங்களுக்குத் தெரியாவிட்டால், தவறான தகவல்களைப் பகிர வேண்டாம்."),
            ("user", "Question: {question}")
        ]
    )
    
    # Initialize OpenAI LLM and output parser
    llm = OllamaLLM(model="tamil-llama2:latest")
    output_parser = StrOutputParser()
    
    # Create chain
    chain = prompt | llm | output_parser
    return chain

# Initialize chatbot
chain = initialize_chatbot()

# Define route for home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input_text = request.form['input_text']
        if input_text:
            output = chain.invoke({'question': input_text})
            return render_template('index.html', input_text=input_text, output=output)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

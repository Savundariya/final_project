# final_project
Personal UPI Usage and Financial Analyzer using LLMs

This project is an AI-powered financial analysis tool that processes UPI transaction statements from apps like **Paytm, GPay, PhonePe**, etc. It extracts key transaction data from bank statements (PDF), categorizes expenses, analyzes spending patterns, and provides personalized financial advice using **Large Language Models (LLMs)** such as OpenRouter GPT.

##  Features

-  PDF extraction of UPI statements using `PyMuPDF`
-  Monthly and Category-wise spending summary using `pandas`
-  LLM-based personalized financial advice using OpenRouter API
-  Automatic categorization of expenses (e.g., Food Delivery, Travel, Groceries)
-  Interactive dashboard with visualizations using `Streamlit`


##  Project Structure
 Final_Project/
│
├── final_project.ipynb # Notebook version for experimentation
├── streamlit.py # Streamlit web app for deployment
├── categorized_transactions.csv # (Optional) output of parsed data
└── README.md # Project documentation

##  Installation

# 1. Clone the repository
# 2. Create virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # On Windows
# 3. Install dependencies
pip install pymupdf pandas streamlit openai

# How to Use
Run the  final_project.ipynb
Launch the Streamlit App
streamlit run streamlit.py
Upload:
Your UPI transaction PDF (from Paytm/PhonePe/Google Pay)
Wait while transactions are extracted and categorized

Get Financial Tips:
Click "Generate Advice with LLM" to get personalized advice based on your spending

# API Key Setup (OpenRouter)
Sign up at https://openrouter.ai
Go to https://openrouter.ai/keys
Generate an API key
Replace the key in streamlit.py:

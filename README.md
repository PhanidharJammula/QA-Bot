QA-Bot
A FastAPI-based Question-Answering (QA) bot using the LangChain framework and large language models. Supports answering questions based on the content of JSON and PDF documents.

Setup
Clone the Repository:
git clone https://github.com/yourusername/QA-Bot.git
cd QA-Bot

Create and Activate a Virtual Environment:
python3 -m venv venv
source venv/bin/activate

Install Dependencies:
python3 -m pip install -r requirements.txt

Configure Environment Variables:
Create a .env file with your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key_here

Usage
Run the Application:
uvicorn main:app --reload

Access the API:
Visit http://127.0.0.1:8000/docs for interactive API documentation.

Upload Documents and Questions:
Use the /question-answering/ endpoint to upload a document and a file with questions.

Development
Install Development Dependencies: python3 -m pip install -r requirements.txt
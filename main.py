import os
import warnings
import tempfile
from fastapi.responses import JSONResponse
from langchain_community.llms import OpenAI
from fastapi import FastAPI, UploadFile, File
from urllib3.exceptions import NotOpenSSLWarning
from langchain.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFLoader, JSONLoader

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

app = FastAPI()

@app.post("/question-answering/")
async def question_answering(questions_file: UploadFile, document_file: UploadFile):
    questions = await questions_file.read()
    
    # Create a temporary file to store the content of the document file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(await document_file.read())
        tmp_file_path = tmp_file.name

    if document_file.filename.endswith(".pdf"):
        loader = PyPDFLoader(tmp_file_path)
    elif document_file.filename.endswith(".json"):
        # Define a basic jq_schema to load the entire JSON document
        jq_schema = "."
        loader = JSONLoader(file_path=tmp_file_path, jq_schema=jq_schema, text_content=False)
    else:
        return JSONResponse(content={"error": "Unsupported document type"}, status_code=400)

    # Load the document content
    documents = loader.load()
    qa_chain = load_qa_chain(llm=OpenAI(openai_api_key=os.getenv("OPEN_API_KEY")), chain_type="map_reduce")

    answers = {}
    for question in questions.decode("utf-8").splitlines():
        result = qa_chain.run(question=question, input_documents=documents)
        answers[question] = result

    return JSONResponse(content=answers)
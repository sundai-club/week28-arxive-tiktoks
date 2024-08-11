from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.content_generator import process
import os
import tempfile
import requests

#app = FastAPI()
#content_generator = ContentGenerator()

DATA_DIR = "./data"

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)

def process_paper(url):
    content = requests.get(url)
    paper_name = url.split("/")[-1]
    if '.pdf' in paper_name:
        paper_name = paper_name.replace('.pdf', '')
    
    # Use a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", prefix=paper_name, dir=None) as temp_file:
        temp_file.write(content.content)
        temp_file_path = temp_file.name

    return process(temp_file_path)



print(process_paper('https://arxiv.org/pdf/2407.01449'))
#@app.post("/generate_content")
#def generate_content(data: dict):
#    url = data['url']
#    paper_path = download_paper(url)
#    paper_path = os.path.abspath(paper_path)
#    generated_content = content_generator.process(paper_path)
#    return {'generated_content': generated_content}


#if __name__ == "__main__":
#    import uvicorn

#   uvicorn.run("main:app", host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.content_generator import ContentGenerator
import os
import requests

app = FastAPI()
content_generator = ContentGenerator()

DATA_DIR = "./data"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def download_paper(url):
    content = requests.get(url)
    paper_path = url.split("/")[-1]
    paper_name = url.split("/")[-1]
    if '.pdf' in paper_path:
        paper_name = paper_path.replace('.pdf', '')
        paper_path = paper_path.replace('.pdf', '')
    paper_path = os.path.join(DATA_DIR, paper_path)
    if not os.path.exists(paper_path):
        os.makedirs(paper_path)
    paper_path = os.path.join(paper_path, paper_name+'.pdf')
    with open(paper_path, "wb") as f:
        f.write(content.content)

    return paper_path


@app.post("/generate_content")
def generate_content(data: dict):
    url = data['url']
    paper_path = download_paper(url)
    paper_path = os.path.abspath(paper_path)
    generated_content = content_generator.process(paper_path)
    return {'generated_content': generated_content}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)

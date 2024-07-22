from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.content_generator import ContentGenerator



app = FastAPI()
content_generator = ContentGenerator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_content")
def generate_content(data: dict):
    paper_path = data['paper_path']
    generated_content = content_generator.process(paper_path)
    return {'generated_content': generated_content}

# generate_content({'paper_path': "C:/Users/mihir/PycharmProjects/week28-arxive-tiktoks/content_generation/src/2402.09246v4.pdf"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
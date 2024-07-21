from src.pdf_parser import parse_pdf
from src.llm_generation_module import GenerationModule
import dspy

class ContentGenerator:
    def __init__(self, model_name='gpt-4-turbo'):
        self.llm = dspy.OpenAI(model=model_name, max_tokens=4000)
        self.generation_module = GenerationModule(llm=self.llm)

    def parse_pdf(self, pdf_file_path):
        content = parse_pdf(pdf_file_path)
        return content

    def process(self, pdf_file_path):
        print(f"Parsing PDF... ")
        content = self.parse_pdf(pdf_file_path)
        if content is not None:
            generated_content = self.generation_module(content)
            return generated_content
        else:
            print('File could not be processed')
            return None
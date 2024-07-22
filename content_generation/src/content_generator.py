from content_generation.src.pdf_parser import parse_pdf
from content_generation.src.llm_generation_module import GenerationModule
import dspy
from content_generation.src.get_images_for_script import get_final_content


class ContentGenerator:
    def __init__(self, model_name='gpt-4-turbo'):
        self.llm = dspy.OpenAI(model=model_name, max_tokens=4000)
        self.generation_module = GenerationModule(llm=self.llm)

    def parse_pdf(self, pdf_file_path):
        content = parse_pdf(pdf_file_path)
        return content

    def process(self, pdf_file_path):
        print(f"Parsing PDF... ")
        content, images_path = self.parse_pdf(pdf_file_path)
        if content is not None:
            generated_content = self.generation_module(content)
            final_response = get_final_content(generated_content['voice_over_script'], images_path)
            return {'final_response': final_response}
        else:
            print('File could not be processed')
            return None

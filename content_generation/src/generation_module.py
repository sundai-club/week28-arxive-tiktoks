from src.openai_client import OpenAIClient
from src.prompts import script_generation_prompt, image_description_prompt
from tqdm import tqdm
import base64

import os


openai_client = OpenAIClient()


def make_prompt(prompt, content):
    prompt = prompt.format(content=content)
    return prompt


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_descriptions(image_folder):
    image_descriptions = {}

    for img in tqdm(os.listdir(image_folder)):
        encoded_image = encode_image(os.path.join(image_folder, img))
        image_description = openai_client.describe_image(image_description_prompt, encoded_image)
        image_descriptions[img] = image_description
    
    return image_descriptions 


def generate_script(content):
    
    script = openai_client.generate_content(make_prompt(script_generation_prompt, content))

    return script  


def align_img_script(input_prompt):
    return openai_client.generate_content(input_prompt, temperature=0.1)


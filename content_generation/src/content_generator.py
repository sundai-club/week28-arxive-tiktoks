import os
from src.pdf_parser import parse_pdf, get_all_images
from src.generation_module import generate_script, get_descriptions, align_img_script
from src.get_images_for_script import get_final_content
from src.prompts import align_image_to_script_prompt

    



def get_script(content):
    script = generate_script(content)
    return script


def align_image_to_script(script, image_descriptions):
    input_prompt = align_image_to_script_prompt.format(script=script, image_descriptions=image_descriptions)
    align_response = align_img_script(input_prompt)
    return align_response


def process(pdf_file_path):

    parsed_content = parse_pdf(pdf_file_path)
    images_path = get_all_images(pdf_file_path)

    script = get_script(parsed_content)
    print(script)
    image_descriptions = get_descriptions(os.path.join(images_path, 'figures'))
    print(image_descriptions)
    alignment_response = align_image_to_script(script, image_descriptions)
    return alignment_response





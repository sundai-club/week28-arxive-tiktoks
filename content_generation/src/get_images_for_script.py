from openai import OpenAI
import os
import json
import base64

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
You are given a script for a TikTok video which is based on a research paper. The script will be used to voice over through the tik tok video.
You are also given a list of images and tables extracted from the research paper. 

Your task is to create two lists of same size. Chunk the input script into n number of sentences.
For each sentence identify the relevant images and tables and put them in the second list.

The second list can be a lis qt of tuples, such that for each sentence in the first list you will have 1 or more relevant images in the second list as a tuple.

If any image is not highly relevant to the sentence, put None in the second list.

Input Script: {input_script}

Example Output:

list 1 : [sentence 1, sentence 2, sentence 3, ...]
list 2 : [(image 1), (image 2, image 2), (None) ...]
"""


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_base64_encoded_images(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            base64_string = encode_image(os.path.join(folder_path, filename))
            images.append((filename, base64_string))
    return images


def create_messages_with_images(input_script, base64_images, captions):
    input_prompt = prompt.format(input_script=input_script)
    content_list = [{"type": "text", "text": input_prompt}]

    for i, base64_image in enumerate(base64_images):
        content_list.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}})

    for i, caption in enumerate(captions):
        content_list.append({"type": "text", "text": f'image_{i}' + caption})

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that outputs two lists as a json {list_1: [], list_2: []}"
        },
        {
            "role": "user",
            "content": content_list
        }
    ]
    return messages


def get_captions(image_folder_path):
    data = image_folder_path + "/data/" + image_folder_path.split("\\")[-1].replace("_figures", ".json")
    with open(data, 'r') as f:
        data = json.load(f)

    captions = []
    for dict_ in data:
        caption = dict_['caption']
        captions.append(caption)
    return captions


def get_final_content(input_script, image_folder_path):
    images = get_base64_encoded_images(image_folder_path + "/figures")
    captions = get_captions(image_folder_path)
    messages = create_messages_with_images(input_script, images, captions)
    from ipdb import set_trace; set_trace()
    response = openai_client.chat.completions.create(model="gpt-4o", messages=messages, temperature=0.1)
    return response

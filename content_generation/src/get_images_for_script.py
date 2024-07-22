from openai import OpenAI
import os
import json
import re
import base64

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
You are given a script for a TikTok video which is based on a research paper. The script will be used to voice over through the tik tok video.
You are also given a list of captions for images.

Your task is to create two lists of same size.

Identify what image caption is highly relevant to what part of the script and put them sequentially in the lists.

You must create two lists, the first one will contain the part of the script and the second list will contain the tuples of relevant images for each part of the script in the same order.
For each sentence identify the relevant images and tables based on the captions provided from them and put them in the second list.

Try to include as many images as possible in the second list.
If any image is not relevant to the sentence, put None in the second list.
Add the image as the image name for the caption in the second list.

Input Script: {input_script}

Do not repeat the images that are already in the second list.

Example Output:
```json
list 1 : [part 1, part 2, part 3, ...]
list 2 : [(image 1), (image 2, image 2), (None) ...]
```
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

    # for i, base64_image in base64_images:
    #     content_list.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}})

    for file_path, caption in captions:
        content_list.append({"type": "text", "text": f'Caption for {file_path}: ' + caption})

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
        image_path = os.path.split(dict_['renderURL'])[1]
        captions.append((image_path, caption))  # (image_path, caption)
    return captions


def get_image_strings(captions, images, image_folder_path):
    image_strings = []
    for caption, image_path in zip(captions, images):
        if image_path[0] is not None:
            image_path = image_path[0]
            image_strings.append({'caption': caption, 'image': encode_image(os.path.join(image_folder_path, image_path))})
        else:
            image_strings.append({'caption': caption, 'image': None})
    return image_strings
def parse_response(response):
    try:
        response = response.choices[0].message.content
        response = re.search(r'```json\n(.*)```', response, re.DOTALL).group(1)
        print(response)
        response = json.loads(response)
    except:
        response = None
    return response

def get_final_content(input_script, image_folder_path):
    images = get_base64_encoded_images(os.path.join(image_folder_path, "figures"))
    captions = get_captions(image_folder_path)
    messages = create_messages_with_images(input_script, images, captions)
    parsed = False
    while not parsed:
        print('Getting response')
        response = openai_client.chat.completions.create(model="gpt-4o", messages=messages, temperature=0.1)
        parsed_response = parse_response(response)
        if parsed_response is not None:
            parsed = True

    final_response = get_image_strings(parsed_response['list_1'], parsed_response['list_2'], os.path.join(image_folder_path, "figures"))
    return {'final_response': final_response}

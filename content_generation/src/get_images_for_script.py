from openai import OpenAI
import os
import json
import re
import base64
import ast

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
You are given a TikTok video script that is based on a research paper, along with a list of image captions. Your task is to create two lists of the same size by matching each part of the script with the most relevant image captions.

Create Two Lists:

List 1: Contains segments of the script.
List 2: Contains the name of image relevant to the segment of the script
For each segment of the script in List 1, identify the most relevant image captions from the provided list. In List 2, include these image names in the same order as they appear in List 1.

Ensure that no image is repeated in List 2.

Use the image names exactly as they appear in the list of captions.

Provide the output in JSON format, ensuring it is compatible with regex and json.loads.

Be sure to mention only the name of the image as mentioned in the caption.

Here’s the required format for the output:

Do not give any special characters unparsable by regex or json.loads

If a image is not relevant to the part of the script, add '' for the image name in List 2

json

{{
  "list_1": [part 1, part 2, ...],
  "list_2": [image 1, image 2, ...]
}}

Input Script: {input_script}
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
        content_list.append({"type": "text", "text": f'Caption for image name - {file_path}\n: ' + caption})

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
        if image_path != '':
            image_strings.append(
                {'caption': caption, 'image': encode_image(os.path.join(image_folder_path, image_path))})
        else:
            image_strings.append({'caption': caption, 'image': None})
    return image_strings


def parse_response(response):
    try:
        response = response.choices[0].message.content
        print(response)
        if '```json' in response:
            response = re.search(r'```json\n(.*)```', response, re.DOTALL).group(1)
        elif response.startswith('{'):
            response = response
        else:
            return None
        # response = ast.literal_eval(response)
        response = json.loads(response)
    except Exception as e:
        print(e)
        response = None
    return response


def get_recorrect_the_format(response):
    prompt = 'Correct the following response so that it is parsable by regex or json.loads\n'
    response = response.choices[0].message.content
    messages = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": response
        }
    ]
    response = openai_client.chat.completions.create(model="gpt-4", messages=messages)
    return response.choices[0].message.content


def get_final_content(input_script, image_folder_path):
    images = get_base64_encoded_images(os.path.join(image_folder_path, "figures"))
    captions = get_captions(image_folder_path)
    messages = create_messages_with_images(input_script, images, captions)
    parsed = False
    while not parsed:
        print('Getting response')
        response = openai_client.chat.completions.create(model="gpt-4", messages=messages, temperature=0.3)
        parsed_response = parse_response(response)
        if parsed_response is not None:
            parsed = True

    final_response = get_image_strings(parsed_response['list_1'], parsed_response['list_2'],
                                       os.path.join(image_folder_path, "figures"))
    return {'final_response': final_response}

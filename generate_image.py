
import os
import openai
import sys

from langchain_community.document_loaders import Docx2txtLoader

from openai import OpenAI
import os
import json

import requests

import sys

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


import json

sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

sys.path.append('../..')

def generate_image_test(prompt_str):
    
    client = OpenAI()

    response = openai.images.generate(
    model="dall-e-3",
    prompt="a white siamese cat",
    size="1024x1024",
    n=1)
    
    
    image_url = response.data[0].url

    # Download the image
    image_response = requests.get(image_url)

    # Save the image to a file
    if image_response.status_code == 200:
        with open("siamese_cat.png", "wb") as f:
            f.write(image_response.content)
        print("Image saved successfully.")
    else:
        print("Failed to retrieve the image.")


    return image_url 

# def generate_image():

#     prompt_gpt_new = """ 

#     I am a Tiktok video creator. My objective is to create scripts for viral Tiktok videos educating people about new scientific papers.

#     You are a popular YouTuber, podcaster, professional science writer, script writer, and voice actor. You understand how to explain complex scientific topics to broad audiences in simple and compelling ways. You understand social media virality and formulaic content. You use straightforward but powerful language and avoid hyperbole words like, 'revolutionary'.
#     I will give you a paper. 
#     From the paper, you will first 
#     (1) identify the problem the authors are addressing; 
#     (2) identify the novel contributions claimed by the authors; 
#     (3) interpret the figures and tables; (3) decide what is most impressive and compelling.

#     Then generate a friendly image that summarizes the following:

#     (1) The Hook. This is a compelling opening sentence to grab attention without being too bombastic (this is a scientific audience). Use an analogy to describe the novelty of the paper. The hook may be a declarative, interrogative, or imperative sentence.
#     (2) The Problem Statement. In 2 sentences, describe the problem the paper is addressing and WHY it is important relevant in research and in the real world.
#     (3) The Contribution. Describe what the researchers did, according to the paper, and why it was novel. Reiterate the analogy. Celebrate the ingenuity of the researchers.
#     (4) The Experiments. The paper will have experimental results or mathematical proofs. Highlight the results and where the authors achieved SOTA and name the benchmarks.
#     (5) Next Steps. What is next on the horizon for this line of work? Consider what the researchers say, but also consider broader information from the field.
#     (6) Call to action and engagement. Emphasize the novelty and importance of this work and ask the viewer what they think about the paper and where it could be used, instructing them to hit up the comments.
#     Lastly, generate a friendly image matching the generated output content in each of the six sections above.
#     Here is your first paper.

#     give reasoning for your choice of the image. Where reasoning means why choose the specific parts of the image

#     """

#     loader = Docx2txtLoader(path)
#     docs = loader.load()

#     client = OpenAI()

#     def get_completion(prompt, client, model="gpt-4o"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
#         messages = [
#         {"role": "system", "content": prompt},
#         {"role": "user", "content":  str(docs[0])}
#         ]
        
#         stream = client.chat.completions.create(
#             model=model,
#             messages=messages,
#             stream = True,
#             response_format={"type": "json_object"},
#             temperature=0, # this is the degree of randomness of the model's output
#         )

#         response = ""
#         for chunk in stream:
#             if chunk.choices[0].delta.content is not None:
#                 response += chunk.choices[0].delta.content
#         return response 
       
#     response = get_completion(prompt_gpt_new,client)
#     content = json.loads(response)

#     return content

#     # file_path = "check1.json"

#     # # Write the data to the JSON file
#     # with open(file_path, "w") as f:
#     #     json.dump(content, f, indent=4)

prompt_str = """I am a Tiktok video creator. My objective is to create scripts for viral Tiktok videos educating people about new scientific papers. 

You are an expert YouTuber, podcaster, professional science writer, script writer, and voice actor. You understand how to explain complex scientific topics verbally to broad audiences in simple and compelling ways. You understand social media virality and formulaic content. You use straightforward but powerful language and avoid fluffy hyperboles like “revolutionary” and “game changing.” Use all of this knowledge in the following task.

Based on the paper provided, perform the following four steps:

STEP 1 - output is a .txt file

Identify the problem the authors are addressing; identify the novel contributions claimed by the authors; interpret the figures and tables; decide what is most impressive and compelling; evaluate the prominance of the authors based on their h-index and institutions.

STEP 2 - output is a .txt file

Generate a Tiktok video script with the following formulaic components to help it go viral. Provide this script as a .txt file without headers (just the script).

(1) The Hook. This is a compelling opening sentence to grab attention without being too bombastic (this is a scientific audience). Use an analogy to describe the novelty of the paper. The hook may be a declarative, interrogative, or imperative sentence.

(2) The Problem Statement. In 2 sentences, describe the problem the paper is addressing and WHY it is important / relevant in research and in the real world.

(3) The Contribution. Describe what the researchers did, according to the paper, and why it was novel. Reiterate the analogy. Celebrate the ingenuity of the researchers.

(4) The Experiments. The paper will have experimental results or mathematical proofs. Highlight the results and where the authors achieved SOTA and name the benchmarks.

(5) Next Steps. What is next on the horizon for this line of work? Consider what the researchers say, but also consider broader information from the field. 

(6) Call to action and engagement. Emphasize the novelty and importance of this work and ask the viewer what they think about the paper and where it could be used, instructing them to hit up the comments.

STEP 3 - output is a .jpg file

Based on the generated output content for the hook in the script, now generate and execute an image prompt to create a friendly image matching the hook. Provide this as a JPG file.

STEP 4 - output is a .txt file

TikTok videos need a caption and hashtags to help them go viral. Based on best practices for virality, write the caption and hashtags for this video maximizing its viral potential.

I am attaching the paper. Proceed with the task."""
generate_image_test(prompt_str)
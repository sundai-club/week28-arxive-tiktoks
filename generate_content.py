# %%
import requests
import os
import base64
from io import BytesIO
from PIL import Image

NUMBER_OF_VIDEOS = 5


# # Define the endpoint URL
# # endpoint = "https://06da-192-54-222-149.ngrok-free.app/generate_content"
# endpoint = "https://608f-192-54-222-149.ngrok-free.app/generate_content"

# # Create a dummy JSON payload
# payload = {
#     # "url": "https://arxiv.org/pdf/2404.16130"
#     "url": "https://arxiv.org/pdf/2406.13542v3"
# }

# # Send a POST request to the endpoint
# response = requests.post(endpoint, json=payload)

# %%

def decode_and_save_png(encoded_string, output_path):
    """
    Decodes a base64-encoded string and saves it as a PNG image file.

    Args:
        encoded_string (str): The base64-encoded string representing the image data.
        output_path (str): The file path where the PNG image should be saved.
    """
    # Decode the base64 string
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))

    # Create a BytesIO object from the decoded bytes
    image_data = BytesIO(decoded_bytes)

    # Open the image from the BytesIO object
    image = Image.open(image_data)

    # Save the image as a PNG file
    image.save(output_path, 'PNG')
    print(f"Image saved to {output_path}")

# %%
def generate_content(arxiv_link):
    """
    Sends a POST request to the specified endpoint with the provided arXiv link
    and returns the response JSON.

    Args:
        arxiv_link (str): The URL of the arXiv paper.

    Returns:
        dict: The JSON response from the endpoint.
    """
    # endpoint = "https://608f-192-54-222-149.ngrok-free.app/generate_content"
    endpoint = "https://b7c4-192-54-222-149.ngrok-free.app/generate_content/"
    payload = {"url": arxiv_link}

    # try:
    response = requests.post(endpoint, json=payload)
    # response.raise_for_status()  # Raise an exception for non-2xx status codes
    return response.json()
    # except requests.exceptions.RequestException as e:
    #     print(f"Error: {e}")
    #     return None

def saves_images_and_creates_script(response):
    script = []
    final_response = response['generated_content']['final_response']['final_response']
    for i,item in enumerate(final_response):
        image = item['image']
        if image is not None:
            decode_and_save_png(image, f"data/image_{i}.png")
        script.append({ 'text': item['caption'],
                        'foreground_img': os.path.join(os.getcwd(), f"data/image_{i}.png") if image is not None else None})
    return script
# %%
from scrape_arxiv import scrape_arxiv_links
links = scrape_arxiv_links("CL")
# response = generate_content("https://arxiv.org/pdf/2406.13542v3")
# %%
import tiktokgen
for i,link in enumerate(links[1:NUMBER_OF_VIDEOS]):
    link = link.replace('abs', 'pdf')
    response = generate_content(link)
    script = saves_images_and_creates_script(response)
    tiktokgen.pipeline.pipeline(script, f'video_{i}.mp4', style='Internet Videos')

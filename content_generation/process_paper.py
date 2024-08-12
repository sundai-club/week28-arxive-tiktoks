from .src.content_generator import process
import os
import tempfile
import requests



def get_tiktok_script(url):
    content = requests.get(url)
    paper_name = url.split("/")[-1]
    if '.pdf' in paper_name:
        paper_name = paper_name.replace('.pdf', '')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", prefix=paper_name, dir=None) as temp_file:
        temp_file.write(content.content)
        temp_file_path = temp_file.name
    
    tik_tok_input, caption = process(temp_file_path)
    
    caption = f"Paper : {url}\n {caption}"

    return tik_tok_input, caption







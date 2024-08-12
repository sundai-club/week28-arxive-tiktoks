import requests
import dataclasses
import tempfile
from content_generation.src.content_generator import process
import scrape_arxiv
import json
import re

@dataclasses.dataclass
class SceneDesc:
    sentence: str
    image_name: str | None

    def to_dict(self):
        return self.__dict__


json_ptrn = re.compile(r'```json(.*)```', re.DOTALL)
def parse_raw_script(raw_script):
    match = re.search(json_ptrn, raw_script)
    if match is None:
        print('Couldn\'t extract JSON string')
        return []
    json_str = match.group(1).strip()
    data = json.loads(json_str)
    ret = []
    for x in data:
        if 'sentence' in x:
            ret.append(SceneDesc(sentence=x['sentence'], image_name=x['image_name'] if x.get('image_name', None) else None))

    return ret



def process_paper(url: str) -> list[SceneDesc]:
    content = requests.get(url)
    paper_name = url.split("/")[-1]
    if '.pdf' in paper_name:
        paper_name = paper_name.replace('.pdf', '')
    
    # Use a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", prefix=paper_name, dir=None) as temp_file:
        temp_file.write(content.content)
        temp_file_path = temp_file.name

    video_script_raw = process(temp_file_path)
    video_script: list[SceneDesc] = parse_raw_script(video_script_raw)
    return video_script



categories=['CVPR', 'ML', 'CL', 'IT', 'Robotics', 'Crypto', 'AI']
urls_list = scrape_arxiv.scrape_arxiv_links(categories)
for url in urls_list:
    x = process_paper(url)
    print(x)

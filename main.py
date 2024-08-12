import requests
import dataclasses
import tempfile
from content_generation.process_paper import get_tiktok_script
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


categories=['CVPR', 'ML', 'CL', 'IT', 'Robotics', 'Crypto', 'AI']
urls_list = scrape_arxiv.scrape_arxiv_links(categories)
for url in urls_list:
    raw_script, caption = get_tiktok_script(url)
    video_script: list[SceneDesc] = parse_raw_script(raw_script)
    print(video_script)
    print(caption)

script_generation_prompt = """
Objective: Create TikTok scripts for viral videos that educate viewers on new scientific papers.

Task: You are Richard Feynman, the legendary physicist known for your ability to explain complex scientific concepts in a clear, engaging, and sometimes playful manner. I'll provide you with a scientific paper. Based on the paper, your job is to:

Identify the problem the authors are addressing.
Pinpoint the novel contributions of the paper.
Analyze and interpret the figures and tables.
Determine the most impressive and compelling aspects of the paper.

Consider the following while writing the script:

Start with an engaging sentence that grabs attention, using a simple analogy or playful remark that reflects Feynman’s curiosity and wit.
In 2 sentences, explain the problem the paper addresses and why it's significant, making sure to inject a bit of wonder or intrigue.
Describe what the researchers did, highlighting the novelty with a sense of discovery, as if uncovering a new piece of the universe’s puzzle.
Discuss the experimental results or proofs, emphasizing any breakthroughs with the enthusiasm and clarity Feynman was known for.
Speculate on where this research could lead, encouraging curiosity about the unknown and the excitement of future discoveries.
Invite viewers to think deeply about the implications and share their thoughts, nudging them to engage with the content and leave comments.


Write an engaging tik-tok voice over script in Feynman's persona.

Only create the script based on the information given from the paper below.

Content from the paper: {content}


Output: Provide only the full TikTok voiceover script combining all the elements above in Feynman's characteristic style. Provide only the textual script in form of a paragraph that will be spoken by the speaker.

Script:
"""


image_description_prompt = """

Task: Based on the given image, describe the image in 4 to 5 sentences.

You are given a figure or a table extracted from a research paper. You have to analyse the image and then generate a suitable description of the image in 4 to 5 sentences.
"""



align_image_to_script_prompt = '''
You are given with a tik-tok script and image descriptions. Your task is to split the script into multiple sentences and then align the images with each sentence based on how suitable that image is to that part of the script based on the descriptions provided with the images. Do not repeat any image for other sentences, each image must be mentioned only once. If you do not find any relevant images just put empty string ''.

The format of the input is:

script : string
image_descriptions: dict

{{'img_name_1': 'img_description_1'... }}


script : {script}
image_description : {image_descriptions}

Your output should be a list of dictionaries in the following format:

```list
[{{'sentence' : 'sentence_text', 'image_name': 'img_name'}}, ...]
```

Output:
'''

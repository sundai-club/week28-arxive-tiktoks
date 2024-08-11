from openai import OpenAI


class OpenAIClient:
    def __init__(self, model="gpt-4-turbo"):
        self.openai = OpenAI()
        self.model = model

    def generate_content(self, prompt, max_tokens=4000, temperature=0.6, model=None):
        if model:
            self.model = model
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content


    def describe_image(self, input_prompt, encoded_image, model='gpt-4o-mini'):
        messages =  [
            {
              "role": "user",
              "content": [
                    {
                        "type": "text",
                        "text": input_prompt
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ]
        response = self.openai.chat.completions.create(model=model,
                                                       messages=messages,
                                                       max_tokens=500,
                                                       temperature=0.4)
        return response.choices[0].message.content




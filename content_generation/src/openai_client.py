from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key, model="gpt-4-turbo"):
        self.api_key = api_key
        self.openai = OpenAI(api_key=api_key)
        self.model = model

    def generate_content(self, prompt, model=None):
        if model:
            self.model = model
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]


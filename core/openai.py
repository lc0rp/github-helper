import openai

from utils.environment import prompt_for_missing_environment_variables

class OpenAIClient:
    def __init__(self):
        vars = prompt_for_missing_environment_variables()
        global OPENAI_API_KEY, OPENAI_ENGINE
        self.api_key = vars.get("OPENAI_API_KEY")
        self.engine = vars.get("OPENAI_ENGINE", "gpt-3.5-turbo")

    def call_openai_api(self, prompt, max_tokens=50, n=1, stop=None):
        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            max_tokens=max_tokens,
            n=n,
            stop=stop
        )
        return response.choices

    def propose_labels_using_openai_api(self, text, labels, n=1):
        prompt = f"Given the following text:\n{text}\n\nWhich of the following labels best describe the content? Labels: {', '.join(labels)}\n\nLabel:"
        response = self.call_openai_api(prompt, n=n)
        return [choice.text.strip() for choice in response]
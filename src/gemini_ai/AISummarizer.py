"""
LLM agent that works with GitStory to produce a summary
"""

from .llm_client import LLMClient


class AISummarizer:
    def __init__(self, api_key: str, parsed_info: str, model: str = "gemini-2.5-pro"):
        self.api_key = api_key
        self.parsed_info = parsed_info
        self.model = model

    def summarize(self):
        client = LLMClient(api_key=self.api_key, model=self.model)
        response = client.generate(prompt=self.parsed_info)
        # Extract summary from response
        if "candidates" in response and response["candidates"]:
            return response["candidates"][0]["content"]["parts"][0]["text"]
        return response

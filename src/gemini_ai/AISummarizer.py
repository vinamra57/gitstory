"""
LLM agent that works with GitStory to produce a summary
"""


class AISummarizer:
    def __init__(self, api_key: str, parsed_info: str):
        self.api_key = api_key
        self.parsed_info = parsed_info

    def summarize(api_key: str, parsed_info: str):
        return "temporary working state"

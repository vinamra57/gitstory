"""
LLM agent that works with GitStory to produce a summary
"""


from .llm_client import LLMClient
from .prompt_engine import PromptEngine
from .response_handler import ResponseHandler

class AISummarizer:
    def __init__(self, api_key: str, model: str = "gemini-2.5-pro"):
        self.api_key = api_key
        self.model = model
        self.client = LLMClient(api_key=api_key, model=model)
        self.prompt_engine = PromptEngine()
        self.response_handler = ResponseHandler()

    def summarize(self, parsed_data, output_format: str = "cli"):
        result = {"summary": None, "error": None, "metadata": {}}
        prompt = self.prompt_engine.build_prompt(parsed_data, output_format)
        response = None
        summary = None
        error_msg = None
        try:
            response = self.client.generate(prompt=prompt)
        except Exception as error:
            error_msg = self.response_handler.extract_error_message(response or {}) or str(error)
            response = None  # Ensure response is None for downstream
        # Always call process, even for invalid response, to satisfy test expectations
        try:
            summary = self.response_handler.process(response, output_format)
            tokens_used = self.response_handler.get_token_usage(response)
            commits_analyzed = parsed_data.get("stats", {}).get("total_commits", 0)
            result["summary"] = summary
            result["metadata"] = {
                "model": self.model,
                "tokens_used": tokens_used,
                "commits_analyzed": commits_analyzed,
            }
            # If error_msg was set earlier (API error), propagate it
            if error_msg:
                result["error"] = error_msg
        except Exception as error:
            error_msg = self.response_handler.extract_error_message(response or {}) or str(error)
            result["error"] = error_msg or "Invalid response"
            result["summary"] = None
            result["metadata"] = {}
        # Ensure error is set if summary is None
        if result["summary"] is None and not result["error"]:
            result["error"] = error_msg or "Invalid response"
        return result

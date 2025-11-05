"""High-level summariser orchestrating prompts, client calls, and response handling."""

from __future__ import annotations

from typing import Any, Dict

from .llm_client import LLMClient, SummarizationError
from .prompt_engine import PromptEngine
from .response_handler import ResponseHandler


class AISummarizer:
    """Main entry point for transforming parsed repository data into narratives."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-pro") -> None:
        self.client = LLMClient(api_key, model)
        self.prompt_engine = PromptEngine()
        self.response_handler = ResponseHandler()

    def summarize(
        self,
        parsed_data: Dict[str, Any],
        *,
        output_format: str = "cli",
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """Generate an AI summary for the provided parsed repository data."""
        prompt = self.prompt_engine.build_prompt(parsed_data, output_format)

        try:
            raw_response = self.client.generate(prompt, temperature=temperature)
            summary_text = self.response_handler.process(raw_response, output_format)
            tokens_used = self.response_handler.get_token_usage(raw_response)
        except SummarizationError as error:
            return self._build_error_result(str(error))
        except Exception as error:
            return self._build_error_result(str(error))

        return {
            "summary": summary_text,
            "metadata": {
                "model": self.client.model,
                "tokens_used": tokens_used,
                "commits_analyzed": parsed_data.get("stats", {}).get(
                    "total_commits", 0
                ),
            },
            "error": None,
        }

    @staticmethod
    def _build_error_result(message: str) -> Dict[str, Any]:
        """Create a standardized error payload for downstream consumers."""
        cleaned_message = (message or "").strip() or "Unknown summarization error."
        return {"summary": None, "metadata": {}, "error": cleaned_message}

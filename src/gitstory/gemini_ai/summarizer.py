"""High-level summariser orchestrating prompts, client calls, and response handling."""

from __future__ import annotations

import time
from typing import Any, Dict

from .llm_client import LLMClient, SummarizationError
from .prompt_engine import PromptEngine
from .response_handler import ResponseHandler


class AISummarizer:
    """Main entry point for transforming parsed repository data into narratives."""

    MAX_RETRY_ATTEMPTS = 3
    RETRY_DELAY_SECONDS = 5

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
        """Generate an AI summary for the provided parsed repository data with retry logic."""
        prompt = self.prompt_engine.build_prompt(parsed_data, output_format)

        # Retry loop for handling transient failures
        for attempt in range(1, self.MAX_RETRY_ATTEMPTS + 1):
            raw_response = None
            summary_text = None
            tokens_used = 0
            error_msg = None
            api_error = None

            try:
                # Step 1: Call LLM API (with built-in retries for API-level issues)
                raw_response = self.client.generate(prompt, temperature=temperature)

                # Step 2: Process and validate response (checks for end marker, content quality)
                summary_text = self.response_handler.process(
                    raw_response, output_format
                )
                tokens_used = self.response_handler.get_token_usage(raw_response)

                # Success! Return the result
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

            except SummarizationError as error:
                # API-level errors (already retried in llm_client, don't retry again)
                api_error = str(error)
                break  # Exit retry loop, return error below

            except ValueError as error:
                # Content validation errors (empty, incomplete, missing end marker)
                error_msg = str(error)
                error_lower = error_msg.lower()

                # Check if this is a retryable content error
                is_retryable = (
                    "incomplete" in error_lower
                    or "empty" in error_lower
                    or "end marker" in error_lower
                    or "short content" in error_lower
                )

                if is_retryable and attempt < self.MAX_RETRY_ATTEMPTS:
                    # Retry: wait and try again
                    time.sleep(self.RETRY_DELAY_SECONDS)
                    continue
                else:
                    # Not retryable or max attempts reached
                    break

            except Exception as error:
                # Unexpected errors - don't retry
                error_msg = self.response_handler.extract_error_message(
                    raw_response or {}
                ) or str(error)
                break

        # If we get here, all retries failed or encountered a non-retryable error
        final_error = api_error or error_msg or "Unknown error during summarization"

        return {"summary": None, "metadata": {}, "error": final_error}

    @staticmethod
    def _build_error_result(message: str) -> Dict[str, Any]:
        """Create a standardized error payload for downstream consumers."""
        cleaned_message = (message or "").strip() or "Unknown summarization error."
        return {"summary": None, "metadata": {}, "error": cleaned_message}

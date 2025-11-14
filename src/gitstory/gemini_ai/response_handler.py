"""Utilities for cleaning and formatting Gemini responses."""

from __future__ import annotations

import re
from typing import Any, Dict, Optional


class ResponseHandler:
    """Process raw Gemini payloads into clean text responses."""

    def process(self, api_response: Dict[str, Any], output_format: str) -> str:
        """Extract the LLM text and format it for the target output."""
        try:
            candidates = api_response.get("candidates", [])
            if not candidates:
                raise ValueError("No candidates in response")
            content_obj = candidates[0].get("content", {})
            # Try 'parts' first
            if "parts" in content_obj and content_obj["parts"]:
                content = content_obj["parts"][0].get("text", "")
            # Fallback to 'text' directly
            elif "text" in content_obj:
                content = content_obj["text"]
            # Fallback to string representation
            else:
                content = str(content_obj)
        except Exception as error:
            print("[DEBUG] Raw API response in process():", api_response)
            raise ValueError(f"Invalid API response format: {error}") from error

        content = self._clean_content(content)

        # Validate content is not empty or too short
        if not content or len(content.strip()) < 20:
            raise ValueError(
                "Received empty or very short content from API (possible incomplete response)"
            )

        # Validate end marker exists
        if "[END-SUMMARY]" not in content:
            raise ValueError(
                "Incomplete response: missing [END-SUMMARY] marker. The response may have been cut off."
            )

        # Remove the end marker before returning
        content = content.replace("[END-SUMMARY]", "").strip()

        return (
            self._format_for_cli(content)
            if output_format == "cli"
            else self._format_for_dashboard(content)
        )

    def extract_error_message(self, api_response: Dict[str, Any]) -> Optional[str]:
        error = api_response.get("error")
        if not error:
            return None
        if isinstance(error, dict):
            return error.get("message") or str(error)
        return str(error)

    def get_token_usage(self, api_response: Dict[str, Any]) -> int:
        usage = api_response.get("usageMetadata", {})
        if not isinstance(usage, dict):
            return 0
        return int(usage.get("totalTokenCount", 0))

    @staticmethod
    def _clean_content(content: str) -> str:
        content = re.sub(r"```[\w]*\n|```", "", content)
        content = re.sub(r"\n{3,}", "\n\n", content)
        return content.strip()

    @staticmethod
    def _format_for_cli(content: str) -> str:
        content = re.sub(r"\n(#+\s)", r"\n\n\1", content)
        content = re.sub(r"(#+\s[^\n]+)\n([^#\n])", r"\1\n\n\2", content)
        return content.strip()

    @staticmethod
    def _format_for_dashboard(content: str) -> str:
        return content.strip()

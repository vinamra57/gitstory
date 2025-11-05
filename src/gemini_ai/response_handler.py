"""Utilities for cleaning and formatting Gemini responses."""

from __future__ import annotations

import re
from typing import Any, Dict, Optional


class ResponseHandler:
    """Process raw Gemini payloads into clean text responses."""

    def process(self, api_response: Dict[str, Any], output_format: str) -> str:
        """Extract the LLM text and format it for the target output."""
        try:
            content = api_response["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as error:
            raise ValueError(f"Invalid API response format: {error}") from error

        content = self._clean_content(content)
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

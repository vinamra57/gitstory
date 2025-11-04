"""Low-level Google Gemini client with retry and validation support."""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

import requests


# Define exceptions inline since we're in gemini_ai not gitstory
class ConfigurationError(Exception):
    """Configuration related errors."""

    pass


class SummarizationError(Exception):
    """LLM summarization errors."""

    pass


class LLMClient:
    """Handles outbound requests to the Google Gemini API."""

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 60
    TIMEOUT_RETRY_DELAY_SECONDS = 5

    def __init__(self, api_key: str, model: str = "gemini-2.5-pro") -> None:
        if not api_key:
            raise ConfigurationError("Missing Gemini API key.")
        self.api_key = api_key
        self.model = model
        self.endpoint = f"{self.BASE_URL}/{model}:generateContent"

    def generate(self, prompt: str, *, temperature: float = 0.7) -> Dict[str, Any]:
        """Generate content from Gemini, retrying on recoverable failures."""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 2000,
            },
        }

        last_error: Optional[Exception] = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response = requests.post(
                    f"{self.endpoint}?key={self.api_key}",
                    json=payload,
                    timeout=30,
                )
                if response.status_code == 401:
                    raise ConfigurationError(
                        "Invalid API key. Check the GITSTORY_API_KEY environment variable."
                    )
                if response.status_code == 429:
                    if attempt == self.MAX_RETRIES:
                        raise SummarizationError(
                            "Rate limit exceeded after multiple retries."
                        )
                    time.sleep(self.RETRY_DELAY_SECONDS)
                    continue
                if response.status_code >= 400:
                    message = self._extract_error(response)
                    raise SummarizationError(
                        f"Gemini API error (HTTP {response.status_code}): {message}"
                    )

                response.raise_for_status()
                return response.json()
            except requests.exceptions.Timeout as timeout_error:
                last_error = timeout_error
                if attempt == self.MAX_RETRIES:
                    break
                time.sleep(self.TIMEOUT_RETRY_DELAY_SECONDS)
            except requests.exceptions.RequestException as request_error:
                last_error = request_error
                if attempt == self.MAX_RETRIES:
                    break
                time.sleep(self.TIMEOUT_RETRY_DELAY_SECONDS)

        raise SummarizationError(f"Gemini request failed: {last_error}")

    def validate_api_key(self) -> bool:
        """Verify the API key by issuing a trivial request."""
        payload = {
            "contents": [{"parts": [{"text": "ping"}]}],
            "generationConfig": {"maxOutputTokens": 4},
        }
        try:
            response = requests.post(
                f"{self.endpoint}?key={self.api_key}", json=payload, timeout=10
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    @staticmethod
    def _extract_error(response: requests.Response) -> str:
        try:
            payload = response.json()
            if isinstance(payload, dict) and "error" in payload:
                error = payload["error"]
                if isinstance(error, dict):
                    return error.get("message", "Unknown error")
                return str(error)
        except ValueError:
            return response.text or "Unknown error"
        return response.text or "Unknown error"

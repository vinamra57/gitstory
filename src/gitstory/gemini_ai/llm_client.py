"""Low-level Google Gemini client with retry and validation support."""

from __future__ import annotations

import time
from typing import Any, Dict

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

    def generate(self, prompt: str, *, temperature: float = 0.5) -> Dict[str, Any]:
        """Generate content from Gemini, retrying on recoverable failures."""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,  # Lower temperature for more factual, consistent output
                "maxOutputTokens": 4000,  # Increased for dashboard format (800-1200 words)
            },
        }

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response = requests.post(
                    f"{self.endpoint}?key={self.api_key}",
                    json=payload,
                    timeout=60,  # Increased for longer responses
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
                json_data = response.json()

                # Validate response is not empty
                if not json_data:
                    if attempt < self.MAX_RETRIES:
                        time.sleep(self.TIMEOUT_RETRY_DELAY_SECONDS)
                        continue
                    raise SummarizationError(
                        "Received empty JSON response from Gemini API after retries"
                    )

                # Validate required fields exist
                candidates = json_data.get("candidates", [])
                if not candidates or len(candidates) == 0:
                    if attempt < self.MAX_RETRIES:
                        time.sleep(self.TIMEOUT_RETRY_DELAY_SECONDS)
                        continue
                    raise SummarizationError(
                        "Received response with no candidates from Gemini API after retries"
                    )

                # Validate basic structure of first candidate
                if not isinstance(candidates[0], dict):
                    if attempt < self.MAX_RETRIES:
                        time.sleep(self.TIMEOUT_RETRY_DELAY_SECONDS)
                        continue
                    raise SummarizationError(
                        "Received malformed candidate structure from Gemini API after retries"
                    )

                return json_data
            except requests.exceptions.Timeout:
                if attempt == self.MAX_RETRIES:
                    raise SummarizationError(
                        f"Request timed out after {self.MAX_RETRIES} retries"
                    )
                time.sleep(self.TIMEOUT_RETRY_DELAY_SECONDS)
            except requests.exceptions.RequestException as request_error:
                if attempt == self.MAX_RETRIES:
                    raise SummarizationError(
                        f"Gemini request failed: {str(request_error)}"
                    )
                time.sleep(self.TIMEOUT_RETRY_DELAY_SECONDS)

        raise SummarizationError("Gemini request failed after maximum retries")

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
        """Attempt to extract a meaningful error message from a Gemini response."""
        try:
            payload = response.json()
        except Exception:
            return LLMClient._fallback_error_message(response)

        if isinstance(payload, dict):
            error = payload.get("error")
            if isinstance(error, dict):
                message = error.get("message")
                if isinstance(message, str) and message.strip():
                    return message.strip()
                return str(error)
            if error:
                error_str = str(error)
                if error_str.strip():
                    return error_str.strip()
        elif isinstance(payload, str) and payload.strip():
            return payload.strip()

        return LLMClient._fallback_error_message(response)

    @staticmethod
    def _fallback_error_message(response: requests.Response) -> str:
        """Provide a deterministic fallback error string for logging and UX."""
        text = getattr(response, "text", "")
        if isinstance(text, str):
            stripped = text.strip()
            if stripped:
                return stripped
        status_code = getattr(response, "status_code", "unknown")
        return f"HTTP {status_code}"

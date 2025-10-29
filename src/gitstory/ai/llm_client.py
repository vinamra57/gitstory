"""
LLM API client with retry logic and rate limiting.
Handles all direct API communication with Google Gemini API.
"""
import requests
import time
from typing import Dict


class LLMClient:
    """Client for Gemini API interactions."""

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    MAX_RETRIES = 3
    RETRY_DELAY = 60  # seconds for rate limits
    TIMEOUT_RETRY_DELAY = 5  # seconds for timeouts

    def __init__(self, api_key: str, model: str = "gemini-2.5-pro"):
        """
        Initialize LLM client.

        Args:
            api_key: Google AI API key for authentication
            model: Model identifier (default: gemini-2.5-pro)
        """
        self.api_key = api_key
        self.model = model
        self.endpoint = f"{self.BASE_URL}/{model}:generateContent"

    def generate(self, prompt: str, temperature: float = 0.7) -> Dict:
        """
        Generate completion from Gemini LLM.

        Args:
            prompt: Input prompt text
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            API response dictionary

        Raises:
            Exception: If API call fails after retries
        """
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 2000
            }
        }

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.post(
                    f"{self.endpoint}?key={self.api_key}",
                    json=payload,
                    timeout=30
                )

                # Handle rate limiting
                if response.status_code == 429:
                    if attempt < self.MAX_RETRIES - 1:
                        print(f"⏳ Rate limit reached. Retrying in {self.RETRY_DELAY}s...")
                        time.sleep(self.RETRY_DELAY)
                        continue
                    else:
                        raise Exception("Rate limit exceeded. Please try again later.")

                # Handle authentication errors
                if response.status_code == 401:
                    raise Exception(
                        "Invalid API key. Please check your GITSTORY_API_KEY environment variable."
                    )

                # Handle other errors
                if response.status_code >= 400:
                    error_msg = self._extract_error(response)
                    if attempt < self.MAX_RETRIES - 1:
                        print(f"⏳ API error: {error_msg}. Retrying (attempt {attempt + 2}/{self.MAX_RETRIES})...")
                        time.sleep(self.TIMEOUT_RETRY_DELAY)
                        continue
                    else:
                        raise Exception(f"API request failed: {error_msg}")

                # Success
                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout:
                if attempt < self.MAX_RETRIES - 1:
                    print(f"⏳ Request timeout. Retrying (attempt {attempt + 2}/{self.MAX_RETRIES})...")
                    time.sleep(self.TIMEOUT_RETRY_DELAY)
                    continue
                else:
                    raise Exception("API request timed out after multiple retries")

            except requests.exceptions.RequestException as e:
                if attempt < self.MAX_RETRIES - 1:
                    print(f"⏳ Request failed: {str(e)}. Retrying (attempt {attempt + 2}/{self.MAX_RETRIES})...")
                    time.sleep(self.TIMEOUT_RETRY_DELAY)
                    continue
                else:
                    raise Exception(f"API request failed: {str(e)}")

        raise Exception("Maximum retries exceeded")

    def _extract_error(self, response) -> str:
        """Extract error message from failed response."""
        try:
            error_data = response.json()
            if 'error' in error_data:
                if isinstance(error_data['error'], dict):
                    return error_data['error'].get('message', str(error_data['error']))
                return str(error_data['error'])
        except Exception:
            pass
        return f"HTTP {response.status_code}"

    def validate_api_key(self) -> bool:
        """
        Validate API key by making a test request.

        Returns:
            True if key is valid, False otherwise
        """
        try:
            test_payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": "test"}
                        ]
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": 5
                }
            }
            response = requests.post(
                f"{self.endpoint}?key={self.api_key}",
                json=test_payload,
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False

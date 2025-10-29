"""
Processes and formats LLM responses.
Cleans up output and handles errors.
"""
from typing import Dict, Optional
import re


class ResponseHandler:
    """Handles LLM response processing."""

    def process(self, api_response: Dict, output_format: str) -> str:
        """
        Process raw API response from Gemini.

        Args:
            api_response: Raw response from Gemini API
            output_format: "cli" or "dashboard"

        Returns:
            Cleaned, formatted summary text
        """
        # Extract content from Gemini response structure
        try:
            content = api_response['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid API response format: {str(e)}")

        # Clean up common issues
        content = self._clean_content(content)

        # Format for output type
        if output_format == "cli":
            return self._format_for_cli(content)
        else:
            return self._format_for_dashboard(content)

    def _clean_content(self, content: str) -> str:
        """Remove common LLM artifacts."""
        # Remove markdown code blocks if present
        content = re.sub(r'```[\w]*\n|```', '', content)

        # Remove excessive newlines
        content = re.sub(r'\n{3,}', '\n\n', content)

        # Strip whitespace
        content = content.strip()

        return content

    def _format_for_cli(self, content: str) -> str:
        """Format content for terminal display."""
        # Ensure proper spacing around headers
        content = re.sub(r'\n(#+\s)', r'\n\n\1', content)

        # Ensure proper spacing after headers
        content = re.sub(r'(#+\s[^\n]+)\n([^#\n])', r'\1\n\n\2', content)

        return content

    def _format_for_dashboard(self, content: str) -> str:
        """Format content for HTML display (minimal processing)."""
        # Dashboard formatting happens in Ian's module
        # Just ensure basic cleanup here
        return content

    def extract_error_message(self, api_response: Dict) -> Optional[str]:
        """Extract error message from failed API response."""
        if 'error' in api_response:
            error = api_response['error']
            if isinstance(error, dict):
                return error.get('message', str(error))
            return str(error)
        return None

    def get_token_usage(self, api_response: Dict) -> int:
        """
        Extract token usage from Gemini API response.

        Args:
            api_response: Raw response from Gemini API

        Returns:
            Total token count (0 if not available)
        """
        try:
            # Gemini provides token usage in usageMetadata
            return api_response.get('usageMetadata', {}).get('totalTokenCount', 0)
        except (KeyError, AttributeError):
            return 0

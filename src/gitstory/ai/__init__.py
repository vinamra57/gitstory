"""
AI summarization package.
Exports the main AISummarizer class.
"""
from .llm_client import LLMClient
from .prompt_engine import PromptEngine
from .response_handler import ResponseHandler


class AISummarizer:
    """Main interface for AI-powered summarization."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-pro"):
        """
        Initialize AI summarizer.

        Args:
            api_key: Google AI API key for Gemini
            model: Model identifier (default: gemini-2.5-pro)
        """
        self.client = LLMClient(api_key, model)
        self.prompt_engine = PromptEngine()
        self.response_handler = ResponseHandler()

    def summarize(self, parsed_data: dict, output_format: str = "cli") -> dict:
        """
        Generate AI summary from parsed repository data.

        Args:
            parsed_data: Output from RepoParser containing:
                - commits: List of commit dicts
                - summary_text: Pre-formatted text for LLM
                - stats: Repository statistics
                - metadata: Additional metadata
            output_format: "cli" for terminal or "dashboard" for HTML

        Returns:
            {
                'summary': str,  # Generated summary text
                'metadata': {
                    'model': str,
                    'tokens_used': int,
                    'commits_analyzed': int
                },
                'error': None or str  # Error message if failed
            }
        """
        try:
            # Build appropriate prompt
            prompt = self.prompt_engine.build_prompt(
                parsed_data,
                output_format
            )

            # Call LLM API
            raw_response = self.client.generate(prompt)

            # Process response
            processed = self.response_handler.process(
                raw_response,
                output_format
            )

            # Extract token usage
            tokens_used = self.response_handler.get_token_usage(raw_response)

            return {
                'summary': processed,
                'metadata': {
                    'model': self.client.model,
                    'tokens_used': tokens_used,
                    'commits_analyzed': parsed_data['stats']['total_commits']
                },
                'error': None
            }

        except Exception as e:
            return {
                'summary': None,
                'metadata': {},
                'error': str(e)
            }


__all__ = ['AISummarizer']

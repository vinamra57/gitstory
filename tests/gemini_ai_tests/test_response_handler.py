"""
Tests for response handler.
"""

import pytest
from gitstory.gemini_ai.response_handler import ResponseHandler


@pytest.fixture
def response_handler():
    """Create response handler for testing."""
    return ResponseHandler()


@pytest.fixture
def mock_gemini_response():
    """Mock successful Gemini API response."""
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "# Repository Summary\n\nThis is a test summary with proper formatting."
                        }
                    ]
                }
            }
        ],
        "usageMetadata": {"totalTokenCount": 150},
    }


def test_process_success(response_handler, mock_gemini_response):
    """Test successful response processing."""
    result = response_handler.process(mock_gemini_response, "cli")

    assert "# Repository Summary" in result
    assert "test summary" in result


def test_process_invalid_response(response_handler):
    """Test handling of invalid response structure."""
    invalid_response = {"invalid": "structure"}

    with pytest.raises(Exception) as exc_info:
        response_handler.process(invalid_response, "cli")

    assert "Invalid API response format" in str(exc_info.value)


def test_process_missing_candidates(response_handler):
    """Test handling of missing candidates."""
    invalid_response = {"candidates": []}

    with pytest.raises(Exception):
        response_handler.process(invalid_response, "cli")


def test_clean_content_removes_code_blocks(response_handler):
    """Test removal of markdown code blocks."""
    content_with_code = "```python\ncode here\n```\nActual content"
    cleaned = response_handler._clean_content(content_with_code)

    assert "```" not in cleaned
    assert "Actual content" in cleaned


def test_clean_content_removes_excessive_newlines(response_handler):
    """Test removal of excessive newlines."""
    content = "Line 1\n\n\n\nLine 2"
    cleaned = response_handler._clean_content(content)

    assert "\n\n\n" not in cleaned
    assert "Line 1\n\nLine 2" in cleaned


def test_clean_content_strips_whitespace(response_handler):
    """Test whitespace stripping."""
    content = "  \n  Content with whitespace  \n  "
    cleaned = response_handler._clean_content(content)

    assert cleaned == "Content with whitespace"


def test_format_for_cli(response_handler):
    """Test CLI formatting."""
    content = "# Header\nContent immediately after\n## Another Header\nMore content"
    formatted = response_handler._format_for_cli(content)

    # Should add spacing around headers
    assert "\n\n#" in formatted or formatted.startswith("#")


def test_format_for_dashboard(response_handler):
    """Test dashboard formatting (minimal processing)."""
    content = "# Header\nContent"
    formatted = response_handler._format_for_dashboard(content)

    # Dashboard formatting is minimal
    assert formatted == content


def test_extract_error_message_dict(response_handler):
    """Test error extraction from dict."""
    error_response = {"error": {"message": "API error occurred"}}

    error_msg = response_handler.extract_error_message(error_response)
    assert error_msg == "API error occurred"


def test_extract_error_message_string(response_handler):
    """Test error extraction from string."""
    error_response = {"error": "Simple error message"}

    error_msg = response_handler.extract_error_message(error_response)
    assert error_msg == "Simple error message"


def test_extract_error_message_none(response_handler):
    """Test error extraction when no error present."""
    success_response = {"candidates": [{"content": {"parts": [{"text": "Success"}]}}]}

    error_msg = response_handler.extract_error_message(success_response)
    assert error_msg is None


def test_get_token_usage_success(response_handler):
    """Test token usage extraction."""
    response = {"usageMetadata": {"totalTokenCount": 250}}

    tokens = response_handler.get_token_usage(response)
    assert tokens == 250


def test_get_token_usage_missing(response_handler):
    """Test token usage when metadata missing."""
    response = {"candidates": [{"content": {"parts": [{"text": "Test"}]}}]}

    tokens = response_handler.get_token_usage(response)
    assert tokens == 0


def test_get_token_usage_invalid_structure(response_handler):
    """Test token usage with invalid structure."""
    response = {"usageMetadata": "invalid"}

    tokens = response_handler.get_token_usage(response)
    assert tokens == 0


def test_process_cli_format(response_handler, mock_gemini_response):
    """Test processing for CLI output format."""
    result = response_handler.process(mock_gemini_response, "cli")

    assert isinstance(result, str)
    assert len(result) > 0


def test_process_dashboard_format(response_handler, mock_gemini_response):
    """Test processing for dashboard output format."""
    result = response_handler.process(mock_gemini_response, "dashboard")

    assert isinstance(result, str)
    assert len(result) > 0


def test_process_preserves_content(response_handler):
    """Test that processing preserves actual content."""
    response = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Important content that should be preserved"}]
                }
            }
        ]
    }

    result = response_handler.process(response, "cli")
    assert "Important content that should be preserved" in result

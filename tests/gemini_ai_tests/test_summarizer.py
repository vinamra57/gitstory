"""
Integration tests for AISummarizer.
"""

import pytest
from unittest.mock import patch
from gemini_ai import AISummarizer


@pytest.fixture
def summarizer():
    """Create AI summarizer for testing."""
    return AISummarizer(api_key="test-api-key", model="gemini-2.5-pro")


@pytest.fixture
def sample_parsed_data():
    """Sample parsed data from RepoParser."""
    return {
        "commits": [
            {
                "hash": "abc123",
                "author": "Alice",
                "timestamp": "2024-01-01T10:00:00",
                "message": "Add user authentication",
                "type": "feature",
                "files_changed": 5,
                "changes": 150,
            }
        ],
        "summary_text": "## FEATURE COMMITS\n- [abc123] Alice: Add user authentication",
        "stats": {
            "total_commits": 1,
            "by_type": {"feature": 1},
            "by_author": {"Alice": {"count": 1, "types": {"feature": 1}}},
        },
        "metadata": {"total_commits_analyzed": 1, "commit_types_present": ["feature"]},
    }


@pytest.fixture
def mock_api_response():
    """Mock Gemini API response."""
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "# Repository Summary\n\nThis repository added user authentication."
                        }
                    ]
                }
            }
        ],
        "usageMetadata": {"totalTokenCount": 150},
    }


def test_init(summarizer):
    """Test summarizer initialization."""
    assert summarizer.client is not None
    assert summarizer.prompt_engine is not None
    assert summarizer.response_handler is not None
    assert summarizer.client.model == "gemini-2.5-pro"


def test_summarize_success_cli(summarizer, sample_parsed_data, mock_api_response):
    """Test successful summarization for CLI output."""
    with patch.object(summarizer.client, "generate", return_value=mock_api_response):
        result = summarizer.summarize(sample_parsed_data, output_format="cli")

        # Check result structure
        assert "summary" in result
        assert "metadata" in result
        assert "error" in result

        # Check success
        assert result["error"] is None
        assert result["summary"] is not None
        assert "Repository Summary" in result["summary"]

        # Check metadata
        assert result["metadata"]["model"] == "gemini-2.5-pro"
        assert result["metadata"]["tokens_used"] == 150
        assert result["metadata"]["commits_analyzed"] == 1


def test_summarize_success_dashboard(summarizer, sample_parsed_data, mock_api_response):
    """Test successful summarization for dashboard output."""
    with patch.object(summarizer.client, "generate", return_value=mock_api_response):
        result = summarizer.summarize(sample_parsed_data, output_format="dashboard")

        assert result["error"] is None
        assert result["summary"] is not None


def test_summarize_api_error(summarizer, sample_parsed_data):
    """Test handling of API errors."""
    with patch.object(
        summarizer.client, "generate", side_effect=Exception("API Error")
    ):
        result = summarizer.summarize(sample_parsed_data, output_format="cli")

        # Check error handling
        assert result["error"] is not None
        assert "API Error" in result["error"]
        assert result["summary"] is None
        assert result["metadata"] == {}


def test_summarize_invalid_response(summarizer, sample_parsed_data):
    """Test handling of invalid API response."""
    invalid_response = {"invalid": "structure"}

    with patch.object(summarizer.client, "generate", return_value=invalid_response):
        result = summarizer.summarize(sample_parsed_data, output_format="cli")

        assert result["error"] is not None
        assert result["summary"] is None


def test_summarize_calls_prompt_engine(
    summarizer, sample_parsed_data, mock_api_response
):
    """Test that summarizer calls prompt engine correctly."""
    with patch.object(summarizer.client, "generate", return_value=mock_api_response):
        with patch.object(
            summarizer.prompt_engine, "build_prompt", return_value="test prompt"
        ) as mock_build:
            summarizer.summarize(sample_parsed_data, output_format="cli")

            # Verify prompt engine was called with correct arguments
            mock_build.assert_called_once_with(sample_parsed_data, "cli")


def test_summarize_calls_response_handler(
    summarizer, sample_parsed_data, mock_api_response
):
    """Test that summarizer calls response handler correctly."""
    with patch.object(summarizer.client, "generate", return_value=mock_api_response):
        with patch.object(
            summarizer.response_handler, "process", return_value="processed"
        ) as mock_process:
            result = summarizer.summarize(sample_parsed_data, output_format="cli")

            # Verify response handler was called
            mock_process.assert_called_once_with(mock_api_response, "cli")
            assert result["summary"] == "processed"


def test_summarize_extracts_token_usage(
    summarizer, sample_parsed_data, mock_api_response
):
    """Test that token usage is correctly extracted."""
    with patch.object(summarizer.client, "generate", return_value=mock_api_response):
        result = summarizer.summarize(sample_parsed_data, output_format="cli")

        assert result["metadata"]["tokens_used"] == 150


def test_summarize_with_zero_commits(summarizer):
    """Test summarization with empty commit data."""
    empty_data = {
        "commits": [],
        "summary_text": "",
        "stats": {"total_commits": 0, "by_type": {}, "by_author": {}},
        "metadata": {},
    }

    mock_response = {
        "candidates": [{"content": {"parts": [{"text": "No commits found."}]}}],
        "usageMetadata": {"totalTokenCount": 10},
    }

    with patch.object(summarizer.client, "generate", return_value=mock_response):
        result = summarizer.summarize(empty_data, output_format="cli")

        assert result["error"] is None
        assert result["metadata"]["commits_analyzed"] == 0


def test_summarize_default_output_format(
    summarizer, sample_parsed_data, mock_api_response
):
    """Test that CLI is the default output format."""
    with patch.object(summarizer.client, "generate", return_value=mock_api_response):
        with patch.object(
            summarizer.prompt_engine, "build_prompt", return_value="test"
        ) as mock_build:
            summarizer.summarize(sample_parsed_data)

            # Should default to "cli"
            mock_build.assert_called_once_with(sample_parsed_data, "cli")


def test_multiple_summarize_calls(summarizer, sample_parsed_data, mock_api_response):
    """Test multiple successive summarization calls."""
    with patch.object(summarizer.client, "generate", return_value=mock_api_response):
        result1 = summarizer.summarize(sample_parsed_data, output_format="cli")
        result2 = summarizer.summarize(sample_parsed_data, output_format="dashboard")

        # Both should succeed independently
        assert result1["error"] is None
        assert result2["error"] is None
        assert result1["summary"] is not None
        assert result2["summary"] is not None

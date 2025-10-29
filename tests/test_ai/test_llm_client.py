"""
Tests for LLM client (Gemini API integration).
"""
import pytest
from unittest.mock import Mock, patch
from gitstory.ai.llm_client import LLMClient


@pytest.fixture
def llm_client():
    """Create LLM client for testing."""
    return LLMClient(api_key="test-api-key", model="gemini-2.5-pro")


@pytest.fixture
def mock_success_response():
    """Mock successful Gemini API response."""
    return {
        'candidates': [
            {
                'content': {
                    'parts': [
                        {'text': 'This is a test summary.'}
                    ]
                }
            }
        ],
        'usageMetadata': {
            'totalTokenCount': 150
        }
    }


def test_init(llm_client):
    """Test client initialization."""
    assert llm_client.api_key == "test-api-key"
    assert llm_client.model == "gemini-2.5-pro"
    assert "gemini-2.5-pro:generateContent" in llm_client.endpoint


def test_generate_success(llm_client, mock_success_response):
    """Test successful API call."""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_success_response
        mock_post.return_value = mock_response

        result = llm_client.generate("test prompt")

        assert result == mock_success_response
        assert mock_post.called
        assert "key=test-api-key" in mock_post.call_args[0][0]


def test_generate_with_temperature(llm_client, mock_success_response):
    """Test API call with custom temperature."""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_success_response
        mock_post.return_value = mock_response

        llm_client.generate("test prompt", temperature=0.5)

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert payload['generationConfig']['temperature'] == 0.5


def test_generate_invalid_api_key(llm_client):
    """Test handling of invalid API key."""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            llm_client.generate("test prompt")

        assert "Invalid API key" in str(exc_info.value)


def test_generate_rate_limit_retry(llm_client, mock_success_response):
    """Test retry logic for rate limiting."""
    with patch('requests.post') as mock_post, patch('time.sleep'):
        # First call returns 429, second call succeeds
        mock_response_429 = Mock()
        mock_response_429.status_code = 429

        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = mock_success_response

        mock_post.side_effect = [mock_response_429, mock_response_200]

        result = llm_client.generate("test prompt")

        assert result == mock_success_response
        assert mock_post.call_count == 2


def test_generate_rate_limit_max_retries(llm_client):
    """Test rate limit exceeding max retries."""
    with patch('requests.post') as mock_post, patch('time.sleep'):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_post.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            llm_client.generate("test prompt")

        assert "Rate limit exceeded" in str(exc_info.value)
        assert mock_post.call_count == 3


def test_generate_timeout_retry(llm_client, mock_success_response):
    """Test retry logic for timeouts."""
    with patch('requests.post') as mock_post, patch('time.sleep'):
        from requests.exceptions import Timeout

        # First call times out, second call succeeds
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_success_response

        mock_post.side_effect = [Timeout(), mock_response]

        result = llm_client.generate("test prompt")

        assert result == mock_success_response
        assert mock_post.call_count == 2


def test_generate_timeout_max_retries(llm_client):
    """Test timeout exceeding max retries."""
    with patch('requests.post') as mock_post, patch('time.sleep'):
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout()

        with pytest.raises(Exception) as exc_info:
            llm_client.generate("test prompt")

        assert "timed out" in str(exc_info.value)
        assert mock_post.call_count == 3


def test_validate_api_key_success(llm_client):
    """Test API key validation success."""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = llm_client.validate_api_key()

        assert result is True


def test_validate_api_key_failure(llm_client):
    """Test API key validation failure."""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        result = llm_client.validate_api_key()

        assert result is False


def test_extract_error():
    """Test error message extraction."""
    client = LLMClient("test-key")

    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        'error': {
            'message': 'Bad request'
        }
    }

    error_msg = client._extract_error(mock_response)
    assert error_msg == 'Bad request'


def test_extract_error_fallback():
    """Test error extraction fallback."""
    client = LLMClient("test-key")

    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.side_effect = Exception()

    error_msg = client._extract_error(mock_response)
    assert "HTTP 500" in error_msg

"""
Shared pytest fixtures for gitstory test suite.

This module provides common fixtures used across all test files for:
- Mock Git repositories and commits
- Sample commit data
- Mock API responses
- Test file paths and temporary directories
"""

import pytest
from unittest.mock import Mock
from datetime import datetime


@pytest.fixture
def sample_commits():
    """
    Returns realistic commit data for testing.

    Provides a list of commits with various types (feature, bugfix, etc.)
    for testing parsers and groupers.
    """
    return [
        {
            "hash": "abc123",
            "author": "Alice Developer",
            "email": "alice@example.com",
            "timestamp": "2025-01-10T10:00:00",
            "message": "feat: add new authentication module",
            "changed_files": ["src/auth.py", "tests/test_auth.py"],
            "diff": "diff --git a/src/auth.py b/src/auth.py\n+def authenticate(): pass",
        },
        {
            "hash": "def456",
            "author": "Bob Developer",
            "email": "bob@example.com",
            "timestamp": "2025-01-10T11:00:00",
            "message": "fix: resolve login bug",
            "changed_files": ["src/auth.py"],
            "diff": "diff --git a/src/auth.py b/src/auth.py\n-return None\n+return user",
        },
        {
            "hash": "ghi789",
            "author": "Alice Developer",
            "email": "alice@example.com",
            "timestamp": "2025-01-10T12:00:00",
            "message": "refactor: improve code structure",
            "changed_files": ["src/utils.py"],
            "diff": "diff --git a/src/utils.py b/src/utils.py\nrefactoring changes",
        },
        {
            "hash": "jkl012",
            "author": "Charlie Developer",
            "email": "charlie@example.com",
            "timestamp": "2025-01-10T13:00:00",
            "message": "docs: update README",
            "changed_files": ["README.md"],
            "diff": "diff --git a/README.md b/README.md\n+# New Section",
        },
        {
            "hash": "mno345",
            "author": "Bob Developer",
            "email": "bob@example.com",
            "timestamp": "2025-01-10T14:00:00",
            "message": "style: format code",
            "changed_files": ["src/main.py"],
            "diff": "diff --git a/src/main.py b/src/main.py\nformatting changes",
        },
        {
            "hash": "pqr678",
            "author": "Alice Developer",
            "email": "alice@example.com",
            "timestamp": "2025-01-10T15:00:00",
            "message": "test: add integration tests",
            "changed_files": ["tests/test_integration.py"],
            "diff": "diff --git a/tests/test_integration.py b/tests/test_integration.py\n+def test_flow(): pass",
        },
        {
            "hash": "stu901",
            "author": "Charlie Developer",
            "email": "charlie@example.com",
            "timestamp": "2025-01-10T16:00:00",
            "message": "chore: update dependencies",
            "changed_files": ["requirements.txt"],
            "diff": "diff --git a/requirements.txt b/requirements.txt\n+pytest>=8.0",
        },
        {
            "hash": "vwx234",
            "author": "Alice Developer",
            "email": "alice@example.com",
            "timestamp": "2025-01-10T17:00:00",
            "message": "random commit message",
            "changed_files": ["random.txt"],
            "diff": "diff --git a/random.txt b/random.txt\nrandom changes",
        },
    ]


@pytest.fixture
def sample_grouped_commits():
    """
    Returns pre-grouped commit data.

    Simulates the output of CommitGrouper for testing downstream components.
    """
    return {
        "grouped_commits": {
            "feature": [
                {
                    "hash": "abc123",
                    "author": "Alice Developer",
                    "message": "feat: add new authentication module",
                    "timestamp": "2025-01-10T10:00:00",
                }
            ],
            "bugfix": [
                {
                    "hash": "def456",
                    "author": "Bob Developer",
                    "message": "fix: resolve login bug",
                    "timestamp": "2025-01-10T11:00:00",
                }
            ],
            "refactor": [
                {
                    "hash": "ghi789",
                    "author": "Alice Developer",
                    "message": "refactor: improve code structure",
                    "timestamp": "2025-01-10T12:00:00",
                }
            ],
            "docs": [
                {
                    "hash": "jkl012",
                    "author": "Charlie Developer",
                    "message": "docs: update README",
                    "timestamp": "2025-01-10T13:00:00",
                }
            ],
            "style": [
                {
                    "hash": "mno345",
                    "author": "Bob Developer",
                    "message": "style: format code",
                    "timestamp": "2025-01-10T14:00:00",
                }
            ],
            "test": [
                {
                    "hash": "pqr678",
                    "author": "Alice Developer",
                    "message": "test: add integration tests",
                    "timestamp": "2025-01-10T15:00:00",
                }
            ],
            "chore": [
                {
                    "hash": "stu901",
                    "author": "Charlie Developer",
                    "message": "chore: update dependencies",
                    "timestamp": "2025-01-10T16:00:00",
                }
            ],
            "other": [
                {
                    "hash": "vwx234",
                    "author": "Alice Developer",
                    "message": "random commit message",
                    "timestamp": "2025-01-10T17:00:00",
                }
            ],
        },
        "stats": {
            "total_commits": 8,
            "by_type": {
                "feature": 1,
                "bugfix": 1,
                "refactor": 1,
                "docs": 1,
                "style": 1,
                "test": 1,
                "chore": 1,
                "other": 1,
            },
            "by_author": {
                "Alice Developer": {
                    "count": 4,
                    "types": {"feature": 1, "refactor": 1, "test": 1, "other": 1},
                },
                "Bob Developer": {"count": 2, "types": {"bugfix": 1, "style": 1}},
                "Charlie Developer": {"count": 2, "types": {"docs": 1, "chore": 1}},
            },
        },
    }


@pytest.fixture
def mock_git_commit():
    """
    Returns a mock Git commit object.

    Simulates GitPython's Commit object for testing GitExtractor.
    """
    commit = Mock()
    commit.hexsha = "abc123def456"
    commit.author.name = "Test Author"
    commit.author.email = "test@example.com"
    commit.committed_datetime = datetime(2025, 1, 10, 10, 0, 0)
    commit.message = "feat: test commit message"
    commit.parents = [Mock()]  # Has parent (not initial commit)

    # Mock diff
    diff_mock = Mock()
    diff_mock.a_path = "test_file.py"
    diff_mock.diff = b"diff content"
    commit.diff.return_value = [diff_mock]

    return commit


@pytest.fixture
def mock_git_initial_commit():
    """
    Returns a mock Git commit object with no parents (initial commit).
    """
    commit = Mock()
    commit.hexsha = "initial123"
    commit.author.name = "Test Author"
    commit.author.email = "test@example.com"
    commit.committed_datetime = datetime(2025, 1, 1, 10, 0, 0)
    commit.message = "Initial commit"
    commit.parents = []  # No parents (initial commit)

    # Mock tree for file listing
    tree_item = Mock()
    tree_item.path = "README.md"
    commit.tree.traverse.return_value = [tree_item]

    return commit


@pytest.fixture
def mock_git_repo(mock_git_commit):
    """
    Returns a mock Git repository.

    Simulates GitPython's Repo object with configurable commits and branches.
    """
    repo = Mock()
    repo.active_branch.name = "main"

    # Mock branches
    branch1 = Mock()
    branch1.name = "main"
    branch2 = Mock()
    branch2.name = "develop"
    branch3 = Mock()
    branch3.name = "feature/test"

    repo.branches = [branch1, branch2, branch3]

    # Mock commit iteration
    repo.iter_commits.return_value = [mock_git_commit]

    return repo


@pytest.fixture
def mock_gemini_success_response():
    """
    Returns a successful Gemini API response.

    Simulates the JSON response from Google Gemini API for testing AI components.
    """
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "This is a comprehensive summary of the repository changes. "
                            "The team has made significant progress with new features, "
                            "bug fixes, and improvements to code quality."
                        }
                    ]
                }
            }
        ],
        "usageMetadata": {
            "promptTokenCount": 500,
            "candidatesTokenCount": 150,
            "totalTokenCount": 650,
        },
    }


@pytest.fixture
def mock_gemini_error_response():
    """
    Returns a Gemini API error response.
    """
    return {
        "error": {
            "code": 400,
            "message": "Invalid request: missing required field",
            "status": "INVALID_ARGUMENT",
        }
    }


@pytest.fixture
def mock_gemini_empty_json_response():
    """
    Returns an empty JSON response from Gemini API.

    Simulates the case where the API returns an empty dictionary.
    """
    return {}


@pytest.fixture
def mock_gemini_empty_candidates_response():
    """
    Returns a Gemini API response with empty candidates array.

    Simulates the case where the API returns valid JSON structure but no candidates.
    """
    return {"candidates": []}


@pytest.fixture
def mock_gemini_empty_text_response():
    """
    Returns a Gemini API response with empty text content.

    Simulates the case where the API returns valid structure but empty text.
    """
    return {
        "candidates": [{"content": {"parts": [{"text": ""}]}}],
        "usageMetadata": {
            "totalTokenCount": 10,
        },
    }


@pytest.fixture
def mock_gemini_incomplete_response():
    """
    Returns a Gemini API response with incomplete text (no end marker).

    Simulates the case where the response is cut off before completion.
    """
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "This is an incomplete summary that was cut off mid-sentence and doesn't have..."
                        }
                    ]
                }
            }
        ],
        "usageMetadata": {
            "totalTokenCount": 100,
        },
    }


@pytest.fixture
def mock_gemini_complete_response_with_marker():
    """
    Returns a Gemini API response with complete text including end marker.

    Simulates a successful response with the [END-SUMMARY] marker.
    """
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "This is a complete summary of the repository changes. "
                            "The team has made significant progress with new features, "
                            "bug fixes, and improvements to code quality.\n\n[END-SUMMARY]"
                        }
                    ]
                }
            }
        ],
        "usageMetadata": {
            "promptTokenCount": 500,
            "candidatesTokenCount": 150,
            "totalTokenCount": 650,
        },
    }


@pytest.fixture
def temp_output_dir(tmp_path):
    """
    Creates a temporary output directory for testing file operations.

    Args:
        tmp_path: pytest's built-in temporary directory fixture

    Returns:
        Path to temporary output directory
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_cleaned_data():
    """
    Returns sample cleaned data for testing dashboard and AI components.
    """
    return {
        "commits": [
            {
                "hash": "abc123",
                "author": "Alice Developer",
                "message": "feat: add new authentication module",
                "timestamp": "2025-01-10T10:00:00",
                "type": "feature",
            },
            {
                "hash": "def456",
                "author": "Bob Developer",
                "message": "fix: resolve login bug",
                "timestamp": "2025-01-10T11:00:00",
                "type": "bugfix",
            },
        ],
        "summary_text": "## Repository Summary\n\n### Features (1)\n- feat: add new authentication module\n\n### Bug Fixes (1)\n- fix: resolve login bug",
        "stats": {
            "total_commits": 2,
            "by_type": {"feature": 1, "bugfix": 1},
            "by_author": {
                "Alice Developer": {"count": 1, "types": {"feature": 1}},
                "Bob Developer": {"count": 1, "types": {"bugfix": 1}},
            },
        },
        "metadata": {
            "time_range": {"start": "2025-01-10T10:00:00", "end": "2025-01-10T11:00:00"}
        },
    }


@pytest.fixture
def large_commit_message():
    """
    Returns a very long commit message for boundary testing.
    """
    return "This is a test commit message. " * 50  # 1500 characters


@pytest.fixture
def large_diff_text():
    """
    Returns a very large diff for boundary testing.
    """
    return "diff --git a/file.py b/file.py\n" + ("+" + "x" * 100 + "\n") * 100  # ~10KB


@pytest.fixture
def mock_env_with_api_key(monkeypatch):
    """
    Sets GEMINI_API_KEY environment variable for testing.

    Args:
        monkeypatch: pytest's monkeypatch fixture
    """
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key-123")


@pytest.fixture
def mock_env_without_api_key(monkeypatch):
    """
    Removes GEMINI_API_KEY environment variable for testing error handling.

    Args:
        monkeypatch: pytest's monkeypatch fixture
    """
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

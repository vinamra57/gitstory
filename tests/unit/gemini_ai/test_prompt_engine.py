"""
Tests for prompt engine.
"""

import pytest
from gitstory.gemini_ai.prompt_engine import PromptEngine


@pytest.fixture
def prompt_engine():
    """Create prompt engine for testing."""
    return PromptEngine()


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
            },
            {
                "hash": "def456",
                "author": "Bob",
                "timestamp": "2024-01-02T14:30:00",
                "message": "Fix login bug",
                "type": "bugfix",
                "files_changed": 2,
                "changes": 15,
            },
        ],
        "summary_text": "## FEATURE COMMITS\n- [abc123] Alice: Add user authentication\n\n## BUGFIX COMMITS\n- [def456] Bob: Fix login bug",
        "stats": {
            "total_commits": 2,
            "by_type": {"feature": 1, "bugfix": 1},
            "by_author": {
                "Alice": {"count": 1, "types": {"feature": 1}},
                "Bob": {"count": 1, "types": {"bugfix": 1}},
            },
        },
        "metadata": {
            "total_commits_analyzed": 2,
            "commit_types_present": ["feature", "bugfix"],
        },
    }


def test_build_prompt_cli_format(prompt_engine, sample_parsed_data):
    """Test prompt building for CLI output."""
    prompt = prompt_engine.build_prompt(sample_parsed_data, "cli")

    # Check that system prompt is included
    assert "technical code historian" in prompt.lower()
    assert "fact-dense, actionable summary" in prompt.lower()

    # Check that data is included
    assert "Total commits analyzed: 2" in prompt
    assert "Alice" in prompt
    assert "Bob" in prompt
    assert "Add user authentication" in prompt


def test_build_prompt_dashboard_format(prompt_engine, sample_parsed_data):
    """Test prompt building for dashboard output."""
    prompt = prompt_engine.build_prompt(sample_parsed_data, "dashboard")

    # Check that dashboard system prompt is included
    assert "technical project analyst" in prompt.lower()
    assert "comprehensive repository report" in prompt.lower()
    assert "multiple stakeholders" in prompt.lower()

    # Check that data is included
    assert "Total commits analyzed: 2" in prompt
    assert "Alice" in prompt
    assert "Bob" in prompt


def test_format_data(prompt_engine, sample_parsed_data):
    """Test data formatting."""
    formatted = prompt_engine._format_data(sample_parsed_data)

    # Check sections are present
    assert "# REPOSITORY DATA" in formatted
    assert "## Overview Statistics" in formatted
    assert "## Commit Type Distribution" in formatted
    assert "## Top Contributors" in formatted
    assert "## Detailed Commit History" in formatted

    # Check statistics are formatted correctly
    assert "Total commits analyzed: 2" in formatted
    assert "Active contributors: 2" in formatted
    assert "feature: 1 commits (50.0%)" in formatted
    assert "bugfix: 1 commits (50.0%)" in formatted

    # Check summary text is included
    assert "FEATURE COMMITS" in formatted
    assert "BUGFIX COMMITS" in formatted


def test_format_data_with_empty_commits(prompt_engine):
    """Test formatting with no commits."""
    empty_data = {
        "commits": [],
        "summary_text": "",
        "stats": {"total_commits": 0, "by_type": {}, "by_author": {}},
        "metadata": {},
    }

    formatted = prompt_engine._format_data(empty_data)

    assert "Total commits analyzed: 0" in formatted
    assert "Active contributors: 0" in formatted


def test_build_comparison_prompt(prompt_engine, sample_parsed_data):
    """Test branch comparison prompt building."""
    branch1_data = sample_parsed_data
    branch2_data = {
        "commits": [
            {
                "hash": "xyz789",
                "author": "Charlie",
                "timestamp": "2024-01-03T09:00:00",
                "message": "Add new feature",
                "type": "feature",
                "files_changed": 8,
                "changes": 200,
            }
        ],
        "summary_text": "## FEATURE COMMITS\n- [xyz789] Charlie: Add new feature",
        "stats": {
            "total_commits": 1,
            "by_type": {"feature": 1},
            "by_author": {"Charlie": {"count": 1, "types": {"feature": 1}}},
        },
        "metadata": {},
    }

    prompt = prompt_engine.build_comparison_prompt(branch1_data, branch2_data)

    # Check comparison instructions
    assert "Compare these two branches" in prompt
    assert "Unique commits" in prompt
    assert "merge strategy" in prompt

    # Check both branches' data is included
    assert "BRANCH 1 DATA" in prompt
    assert "BRANCH 2 DATA" in prompt
    assert "Alice" in prompt
    assert "Charlie" in prompt


def test_cli_system_prompt_content(prompt_engine):
    """Test CLI system prompt has required content."""
    prompt = prompt_engine.CLI_SYSTEM_PROMPT

    # Check key instructions
    assert "what changed and why" in prompt
    assert "STRICT REQUIREMENTS" in prompt
    assert "bullet points" in prompt
    assert "file paths" in prompt
    assert "commit counts" in prompt

    # Check anti-fluff rules
    assert "FORBIDDEN" in prompt
    assert "significant progress" in prompt
    assert "various improvements" in prompt

    # Check format guidance with examples
    assert "EXAMPLES OF GOOD BULLETS" in prompt
    assert "EXAMPLES OF BAD BULLETS" in prompt
    assert "[FEATURE]" in prompt
    assert "[BUGFIX]" in prompt
    assert "[REFACTOR]" in prompt


def test_dashboard_system_prompt_content(prompt_engine):
    """Test dashboard system prompt has required content."""
    prompt = prompt_engine.DASHBOARD_SYSTEM_PROMPT

    # Check key instructions
    assert "comprehensive repository report" in prompt
    assert "multiple stakeholders" in prompt
    assert "ANALYSIS FRAMEWORK" in prompt
    assert "QUALITY REQUIREMENTS" in prompt

    # Check anti-fluff rules
    assert "FORBIDDEN PHRASES" in prompt
    assert "significant progress" in prompt
    assert "various improvements" in prompt

    # Check format guidance sections
    assert "## Executive Summary" in prompt
    assert "## Development Focus" in prompt
    assert "## Major Technical Changes" in prompt
    assert "## Code Health Signals" in prompt
    assert "## Team Dynamics" in prompt
    assert "## Forward-Looking Assessment" in prompt

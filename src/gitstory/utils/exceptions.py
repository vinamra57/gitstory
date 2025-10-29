"""
Custom exceptions for GitStory.
"""


class GitStoryError(Exception):
    """Base exception for GitStory errors."""
    pass


class ConfigError(GitStoryError):
    """Configuration-related errors."""
    pass


class ParserError(GitStoryError):
    """Repository parsing errors."""
    pass


class AIError(GitStoryError):
    """AI/LLM-related errors."""
    pass


class DashboardError(GitStoryError):
    """Dashboard generation errors."""
    pass

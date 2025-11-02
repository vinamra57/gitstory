"""
Repository parser package.
Exports the main RepoParser class for external use.
"""
from .git_extractor import GitExtractor
from .commit_grouper import CommitGrouper
from .data_cleaner import DataCleaner

class RepoParser:
    """Main interface for repository parsing."""
    def __init__(self, repo_path: str):
        self.extractor = GitExtractor(repo_path)
        self.grouper = CommitGrouper()
        self.cleaner = DataCleaner()

    def parse(self, since: str = None, until: str = None, branch: str = None):
        """
        Parse repository and return structured data.
        """
        raw_commits = self.extractor.get_commits(since, until, branch)
        grouped = self.grouper.group_commits(raw_commits)
        cleaned = self.cleaner.clean_data(grouped)
        return cleaned

__all__ = ['RepoParser']

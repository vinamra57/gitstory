"""
Repository parser package.
Exports the main RepoParser class for external use.
"""

from .git_extractor import GitExtractor
from .commit_grouper import CommitGrouper
from .data_cleaner import DataCleaner
from .branch_comparator import BranchComparator


class RepoParser:
    """Main interface for repository parsing."""

    def __init__(self, repo_path: str):
        self.extractor = GitExtractor(repo_path)
        self.grouper = CommitGrouper()
        self.cleaner = DataCleaner()
        self.comparator = BranchComparator(self.grouper)

    def parse(self, since: str = None, until: str = None, branch: str = None):
        """
        Parse repository and return structured data.
        """
        raw_commits = self.extractor.get_commits(since, until, branch)
        grouped = self.grouper.group_commits(raw_commits)
        cleaned = self.cleaner.clean_data(grouped)
        return cleaned

    def compare(
        self,
        base_branch: str,
        compare_branch: str,
        since: str = None,
        until: str = None,
        context_commits: int = 5,
    ):
        """
        Compare two branches and return structured comparison data.

        Pipeline: Extract → Process → Clean
        """
        # 1. Extract raw comparison data from Git
        raw_comparison = self.extractor.compare_branches(
            base_branch, compare_branch, since, until, context_commits
        )

        # 2. Process comparison (calculate metrics, classify, analyze)
        processed = self.comparator.process_comparison(
            base_commits=raw_comparison["base_only_commits"],
            compare_commits=raw_comparison["compare_only_commits"],
            context_commits=raw_comparison["context_commits"],
            merge_base=raw_comparison["merge_base"],
            base_branch_name=raw_comparison["base_branch"],
            compare_branch_name=raw_comparison["compare_branch"],
        )

        # 3. Clean and optimize for LLM
        cleaned = self.cleaner.clean_comparison_data(processed)

        return cleaned


__all__ = ["RepoParser"]

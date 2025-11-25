"""
Branch comparison logic.
Processes and analyzes differences between two Git branches.
"""

from typing import List, Dict
from datetime import datetime
from .commit_grouper import CommitGrouper


class BranchComparator:
    """Processes and structures branch comparison data."""

    def __init__(self, commit_grouper: CommitGrouper):
        self.grouper = commit_grouper

    def process_comparison(
        self,
        base_commits: List[Dict],
        compare_commits: List[Dict],
        context_commits: List[Dict],
        merge_base: Dict,
        base_branch_name: str,
        compare_branch_name: str,
    ) -> Dict:
        """
        Process comparison data and return structured analysis.

        Returns:
        {
            'base_branch': str,
            'compare_branch': str,
            'merge_base': {...},
            'base_only_commits': List[Dict],
            'compare_only_commits': List[Dict],
            'context_commits': List[Dict],
            'divergence_metrics': {...},
            'base_stats': {...},
            'compare_stats': {...},
            'file_analysis': {...}
        }
        """
        # Group and classify commits for each branch
        base_grouped = self.grouper.group_commits(base_commits)
        compare_grouped = self.grouper.group_commits(compare_commits)

        # Calculate divergence metrics
        divergence_metrics = self._calculate_divergence_metrics(
            base_commits, compare_commits, merge_base
        )

        # Analyze file changes
        file_analysis = self._analyze_file_changes(base_commits, compare_commits)

        return {
            "base_branch": base_branch_name,
            "compare_branch": compare_branch_name,
            "merge_base": merge_base,
            "base_only_commits": base_commits,
            "compare_only_commits": compare_commits,
            "context_commits": context_commits,
            "divergence_metrics": divergence_metrics,
            "base_stats": base_grouped["stats"],
            "compare_stats": compare_grouped["stats"],
            "file_analysis": file_analysis,
        }

    def _calculate_divergence_metrics(
        self, base_commits: List[Dict], compare_commits: List[Dict], merge_base: Dict
    ) -> Dict:
        """Calculate divergence metrics between branches."""
        # Extract unique contributors from each branch
        base_contributors = list(set(c["author"] for c in base_commits))
        compare_contributors = list(set(c["author"] for c in compare_commits))

        # Calculate time since divergence
        merge_base_time = datetime.fromisoformat(merge_base["timestamp"])
        now = datetime.now()
        time_diff = now - merge_base_time

        # Format time difference in human-readable format
        if time_diff.days > 30:
            time_since = f"{time_diff.days // 30} month{'s' if time_diff.days // 30 != 1 else ''} ago"
        elif time_diff.days > 0:
            time_since = f"{time_diff.days} day{'s' if time_diff.days != 1 else ''} ago"
        elif time_diff.seconds >= 3600:
            time_since = f"{time_diff.seconds // 3600} hour{'s' if time_diff.seconds // 3600 != 1 else ''} ago"
        else:
            time_since = "recently"

        return {
            "time_since_divergence": time_since,
            "base_commit_count": len(base_commits),
            "compare_commit_count": len(compare_commits),
            "base_contributors": base_contributors,
            "compare_contributors": compare_contributors,
        }

    def _analyze_file_changes(
        self, base_commits: List[Dict], compare_commits: List[Dict]
    ) -> Dict:
        """Analyze file changes to identify unique and shared files."""
        # Collect all files changed in each branch
        base_files = set()
        for commit in base_commits:
            base_files.update(commit.get("files_changed", []))

        compare_files = set()
        for commit in compare_commits:
            compare_files.update(commit.get("files_changed", []))

        # Identify unique and shared files
        base_only_files = list(base_files - compare_files)
        compare_only_files = list(compare_files - base_files)
        shared_files = list(base_files & compare_files)

        return {
            "base_only_files": sorted(base_only_files),
            "compare_only_files": sorted(compare_only_files),
            "shared_files": sorted(shared_files),  # Conflict risk
        }

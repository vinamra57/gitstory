"""
Git data extraction using GitPython.
Handles all direct Git repository interactions.
"""

from git import Repo, InvalidGitRepositoryError
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import re


class GitExtractor:
    """Extracts commit metadata from Git repositories."""

    def __init__(self, repo_path: str):
        try:
            self.repo = Repo(repo_path)
        except InvalidGitRepositoryError:
            raise InvalidGitRepositoryError(
                f"Not a valid Git repository: {repo_path}\n"
                f"Please run this command in a Git repository or use 'git init'"
            )

    def get_commits(
        self,
        since: Optional[str] = None,
        until: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> List[Dict]:
        if branch is None:
            branch = self.repo.active_branch.name
        since_dt = self._parse_time(since) if since else None
        until_dt = self._parse_time(until) if until else datetime.now()
        commits = []
        for commit in self.repo.iter_commits(branch):
            commit_time = datetime.fromtimestamp(commit.committed_date)
            if since_dt and commit_time < since_dt:
                break
            if commit_time > until_dt:
                continue
            try:
                diff_text = self._get_commit_diff(commit)
            except Exception as e:
                diff_text = f"Error extracting diff: {str(e)}"
            commits.append(
                {
                    "hash": commit.hexsha[:8],
                    "author": commit.author.name,
                    "email": commit.author.email,
                    "timestamp": commit_time.isoformat(),
                    "message": commit.message.strip(),
                    "files_changed": self._get_changed_files(commit),
                    "insertions": commit.stats.total["insertions"],
                    "deletions": commit.stats.total["deletions"],
                    "diff": diff_text,
                }
            )
        return commits

    def _parse_time(self, time_str: str) -> datetime:
        try:
            return datetime.fromisoformat(time_str)
        except ValueError:
            pass
        match = re.match(r"(\d+)([wmd])", time_str)
        if match:
            value, unit = int(match.group(1)), match.group(2)
            if unit == "d":
                delta = timedelta(days=value)
            elif unit == "w":
                delta = timedelta(weeks=value)
            elif unit == "m":
                delta = timedelta(days=value * 30)
            return datetime.now() - delta
        raise ValueError(f"Invalid time format: {time_str}")

    def _get_changed_files(self, commit) -> List[str]:
        if not commit.parents:
            return []
        diff = commit.parents[0].diff(commit)
        return [item.a_path for item in diff]

    def _get_commit_diff(self, commit) -> str:
        """Extracts the full diff text for a commit."""
        if not commit.parents:
            # Initial commit, show all files as added
            return "\n".join([f"A {obj.path}" for obj in commit.tree.traverse()])
        diff = commit.parents[0].diff(commit, create_patch=True)
        return "\n".join(
            [
                d.diff.decode(errors="ignore")
                if hasattr(d.diff, "decode")
                else str(d.diff)
                for d in diff
            ]
        )

    def get_branch_list(self) -> List[str]:
        return [branch.name for branch in self.repo.branches]

    def get_current_branch(self) -> str:
        return self.repo.active_branch.name

    def compare_branches(
        self,
        base_branch: str,
        compare_branch: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        context_commits: int = 5,
    ) -> Dict:
        """
        Compare two branches and return structured commit data.

        Steps:
        1. Validate both branches exist
        2. Find merge base (common ancestor)
        3. Extract commits unique to base branch
        4. Extract commits unique to compare branch
        5. Extract context commits from merge base
        6. Apply time filtering if provided

        Returns: Dict with base_only_commits, compare_only_commits,
                 context_commits, merge_base info, branch names
        """
        # Validate branches exist
        if base_branch not in [b.name for b in self.repo.branches]:
            raise ValueError(f"Base branch not found: {base_branch}")
        if compare_branch not in [b.name for b in self.repo.branches]:
            raise ValueError(f"Compare branch not found: {compare_branch}")

        # Find merge base
        merge_bases = self.repo.merge_base(base_branch, compare_branch)
        if not merge_bases:
            raise ValueError(
                f"No common ancestor found between {base_branch} and {compare_branch}"
            )

        merge_base_commit = merge_bases[0]

        # Extract unique commits for each branch
        base_only_commits = self._extract_commits_in_range(
            f"{compare_branch}..{base_branch}", since, until
        )
        compare_only_commits = self._extract_commits_in_range(
            f"{base_branch}..{compare_branch}", since, until
        )

        # Extract context commits from merge base
        context_commit_list = self._extract_commits_from_point(
            merge_base_commit, context_commits
        )

        return {
            "base_branch": base_branch,
            "compare_branch": compare_branch,
            "merge_base": self._format_commit(merge_base_commit),
            "base_only_commits": base_only_commits,
            "compare_only_commits": compare_only_commits,
            "context_commits": context_commit_list,
        }

    def _extract_commits_in_range(
        self,
        revision_range: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> List[Dict]:
        """Extract commits in a range, with optional time filtering."""
        since_dt = self._parse_time(since) if since else None
        until_dt = self._parse_time(until) if until else datetime.now()

        commits = []
        for commit in self.repo.iter_commits(revision_range):
            commit_time = datetime.fromtimestamp(commit.committed_date)
            if since_dt and commit_time < since_dt:
                continue
            if commit_time > until_dt:
                continue
            commits.append(self._format_commit(commit))
        return commits

    def _extract_commits_from_point(self, start_commit, max_count: int) -> List[Dict]:
        """Extract commits starting from a specific commit."""
        commits = []
        for commit in self.repo.iter_commits(start_commit, max_count=max_count):
            commits.append(self._format_commit(commit))
        return commits

    def _format_commit(self, commit) -> Dict:
        """Format a GitPython commit object into standard dict format."""
        commit_time = datetime.fromtimestamp(commit.committed_date)
        try:
            diff_text = self._get_commit_diff(commit)
        except Exception as e:
            diff_text = f"Error extracting diff: {str(e)}"

        return {
            "hash": commit.hexsha[:8],
            "author": commit.author.name,
            "email": commit.author.email,
            "timestamp": commit_time.isoformat(),
            "message": commit.message.strip(),
            "files_changed": self._get_changed_files(commit),
            "insertions": commit.stats.total.get("insertions", 0),
            "deletions": commit.stats.total.get("deletions", 0),
            "diff": diff_text,
        }

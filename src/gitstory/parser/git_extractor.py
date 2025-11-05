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
    def get_commits(self, since: Optional[str] = None, until: Optional[str] = None, branch: Optional[str] = None) -> List[Dict]:
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
            commits.append({
                'hash': commit.hexsha[:8],
                'author': commit.author.name,
                'email': commit.author.email,
                'timestamp': commit_time.isoformat(),
                'message': commit.message.strip(),
                'files_changed': self._get_changed_files(commit),
                'insertions': commit.stats.total['insertions'],
                'deletions': commit.stats.total['deletions'],
                'diff': diff_text
            })
        return commits
    def _parse_time(self, time_str: str) -> datetime:
        try:
            return datetime.fromisoformat(time_str)
        except ValueError:
            pass
        match = re.match(r'(\d+)([wmd])', time_str)
        if match:
            value, unit = int(match.group(1)), match.group(2)
            if unit == 'd':
                delta = timedelta(days=value)
            elif unit == 'w':
                delta = timedelta(weeks=value)
            elif unit == 'm':
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
            return '\n'.join([f"A {obj.path}" for obj in commit.tree.traverse()])
        diff = commit.parents[0].diff(commit, create_patch=True)
        return '\n'.join([d.diff.decode(errors='ignore') if hasattr(d.diff, 'decode') else str(d.diff) for d in diff])
    def get_branch_list(self) -> List[str]:
        return [branch.name for branch in self.repo.branches]
    def get_current_branch(self) -> str:
        return self.repo.active_branch.name

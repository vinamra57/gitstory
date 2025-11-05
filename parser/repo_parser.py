import git
from typing import List, Dict

class RepoParser:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)

    def get_branches(self) -> List[str]:
        """Return a list of branch names in the repository."""
        return [head.name for head in self.repo.heads]

    def get_recent_commits(self, branch: str = None, count: int = 5) -> List[Dict]:
        """Return a list of recent commits for a branch."""
        if branch:
            commits = list(self.repo.iter_commits(branch, max_count=count))
        else:
            commits = list(self.repo.iter_commits(max_count=count))
        return [
            {
                "hexsha": commit.hexsha,
                "author": commit.author.name,
                "date": commit.committed_datetime.isoformat(),
                "message": commit.message.strip()
            }
            for commit in commits
        ]

    def get_file_changes(self, commit_hexsha: str) -> List[str]:
        """Return a list of changed files for a given commit."""
        commit = self.repo.commit(commit_hexsha)
        return [diff.a_path for diff in commit.diff(None)]

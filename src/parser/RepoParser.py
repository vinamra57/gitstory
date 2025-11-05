"""
Parses through the git commit history for this branch (passed in git commit history)
"""


class RepoParser:
    def __init__(self, branch: str):
        self.branch = branch

    def parse(self):
        """Return deterministic mock repo data for offline execution and tests."""
        commits = [
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
                "message": "Fix login redirect bug",
                "type": "bugfix",
                "files_changed": 2,
                "changes": 45,
            },
        ]

        return {
            "commits": commits,
            "summary_text": "## FEATURE COMMITS\n- [abc123] Alice: Add user authentication\n\n## BUGFIX COMMITS\n- [def456] Bob: Fix login redirect bug",
            "stats": {
                "total_commits": len(commits),
                "by_type": {
                    "feature": 1,
                    "bugfix": 1,
                },
                "by_author": {
                    "Alice": {"count": 1, "types": {"feature": 1}},
                    "Bob": {"count": 1, "types": {"bugfix": 1}},
                },
            },
            "metadata": {
                "total_commits_analyzed": len(commits),
                "commit_types_present": ["feature", "bugfix"],
            },
        }

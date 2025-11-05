"""
Groups commits by type and semantic meaning.
Uses commit message patterns to classify commits.
"""
from typing import List, Dict
import re

class CommitGrouper:
    """Groups commits into semantic categories."""
    PATTERNS = {
        'feature': [
            r'^feat(\(.+\))?:',
            r'^add',
            r'^implement',
            r'new feature',
            r'feature:'
        ],
        'bugfix': [
            r'^fix(\(.+\))?:',
            r'^bug',
            r'hotfix',
            r'patch',
            r'resolve.*issue'
        ],
        'refactor': [
            r'^refactor(\(.+\))?:',
            r'refactor',
            r'restructure',
            r'reorganize'
        ],
        'docs': [
            r'^docs?(\(.+\))?:',
            r'documentation',
            r'readme',
            r'comment'
        ],
        'style': [
            r'^style(\(.+\))?:',
            r'formatting',
            r'whitespace',
            r'lint'
        ],
        'test': [
            r'^test(\(.+\))?:',
            r'add.*test',
            r'test.*coverage'
        ],
        'chore': [
            r'^chore(\(.+\))?:',
            r'dependency',
            r'dependencies',
            r'package',
            r'build'
        ]
    }
    def group_commits(self, commits: List[Dict]) -> Dict:
        grouped = {
            'feature': [],
            'bugfix': [],
            'refactor': [],
            'docs': [],
            'style': [],
            'test': [],
            'chore': [],
            'other': []
        }
        author_stats = {}
        for commit in commits:
            commit_type = self._classify_commit(commit['message'])
            grouped[commit_type].append(commit)
            author = commit['author']
            if author not in author_stats:
                author_stats[author] = {'count': 0, 'types': {}}
            author_stats[author]['count'] += 1
            author_stats[author]['types'][commit_type] = \
                author_stats[author]['types'].get(commit_type, 0) + 1
        return {
            'grouped_commits': grouped,
            'stats': {
                'total_commits': len(commits),
                'by_type': {k: len(v) for k, v in grouped.items() if v},
                'by_author': author_stats
            }
        }
    def _classify_commit(self, message: str) -> str:
        message_lower = message.lower()
        for commit_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return commit_type
        return 'other'

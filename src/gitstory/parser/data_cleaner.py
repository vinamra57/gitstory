"""
Cleans and optimizes commit data for LLM processing.
Reduces token usage and improves summary quality.
"""
from typing import Dict, List

class DataCleaner:
    """Cleans and optimizes data for AI consumption."""
    MAX_MESSAGE_LENGTH = 200
    MAX_COMMITS_PER_GROUP = 50
    MAX_DIFF_CHUNK_SIZE = 2000
    def clean_data(self, grouped_data: Dict) -> Dict:
        cleaned_commits = []
        summary_chunks = []
        for commit_type, commits in grouped_data['grouped_commits'].items():
            if not commits:
                continue
            commits = commits[:self.MAX_COMMITS_PER_GROUP]
            for commit in commits:
                cleaned = self._clean_commit(commit, commit_type)
                cleaned_commits.append(cleaned)
            chunk = self._create_summary_chunk(commit_type, commits)
            summary_chunks.append(chunk)
        return {
            'commits': cleaned_commits,
            'summary_text': '\n\n'.join(summary_chunks),
            'stats': grouped_data['stats'],
            'metadata': {
                'total_commits_analyzed': len(cleaned_commits),
                'commit_types_present': list(grouped_data['stats']['by_type'].keys())
            }
        }
    def _clean_commit(self, commit: Dict, commit_type: str) -> Dict:
        message = commit['message']
        if len(message) > self.MAX_MESSAGE_LENGTH:
            message = message[:self.MAX_MESSAGE_LENGTH] + '...'
        # Chunk diff text
        diff_chunks = self._chunk_diff(commit.get('diff', ''))
        return {
            'hash': commit['hash'],
            'author': commit['author'],
            'timestamp': commit['timestamp'],
            'message': message,
            'type': commit_type,
            'files_changed': len(commit['files_changed']),
            'changes': commit['insertions'] + commit['deletions'],
            'diff_chunks': diff_chunks
        }
    def _chunk_diff(self, diff_text: str) -> List[str]:
        """Chunk large diff text into blocks for LLM token limits."""
        if not diff_text:
            return []
        return [diff_text[i:i+self.MAX_DIFF_CHUNK_SIZE] for i in range(0, len(diff_text), self.MAX_DIFF_CHUNK_SIZE)]
    def _create_summary_chunk(self, commit_type: str, commits: List[Dict]) -> str:
        chunk = [f"## {commit_type.upper()} COMMITS ({len(commits)} total)"]
        for commit in commits[:10]:
            chunk.append(
                f"- [{commit['hash']}] {commit['author']}: "
                f"{commit['message'][:100]}"
            )
        if len(commits) > 10:
            chunk.append(f"... and {len(commits) - 10} more {commit_type} commits")
        return '\n'.join(chunk)

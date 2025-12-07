"""
Validation module for parser pipeline.
Ensures data integrity between stages and handles graceful degradation.
"""
from typing import List, Dict, Any
from datetime import datetime


class ValidationError(Exception):
    """Raised when pipeline validation fails."""
    pass


class ValidationReport:
    """Tracks validation warnings and skipped items."""
    def __init__(self):
        self.warnings: List[str] = []
        self.skipped_commits: int = 0
        self.total_commits_processed: int = 0

    def add_warning(self, message: str):
        self.warnings.append(message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'warnings': self.warnings,
            'skipped_commits': self.skipped_commits,
            'total_commits_processed': self.total_commits_processed
        }


def validate_commit(commit: Dict) -> tuple[bool, str]:
    """
    Validate a single commit object.
    Returns (is_valid, error_message)
    """
    required_fields = ['hash', 'author', 'message', 'timestamp']
    
    for field in required_fields:
        if field not in commit or commit[field] is None:
            return False, f"Missing required field: {field}"
    
    # Validate timestamp format
    try:
        if isinstance(commit['timestamp'], str):
            datetime.fromisoformat(commit['timestamp'])
    except (ValueError, TypeError):
        return False, f"Invalid timestamp format: {commit['timestamp']}"
    
    return True, ""


def sanitize_commit(commit: Dict) -> Dict:
    """
    Sanitize and normalize commit data.
    Sets defaults for missing optional fields.
    """
    sanitized = commit.copy()
    
    # Ensure author is string
    if not isinstance(sanitized.get('author'), str):
        sanitized['author'] = 'Unknown'
    
    # Ensure message is string
    if not isinstance(sanitized.get('message'), str):
        sanitized['message'] = '(No commit message)'
    
    # Set defaults for optional fields
    sanitized.setdefault('files_changed', [])
    sanitized.setdefault('insertions', 0)
    sanitized.setdefault('deletions', 0)
    sanitized.setdefault('diff', '')
    
    # Ensure numeric fields are integers
    try:
        sanitized['insertions'] = int(sanitized['insertions'])
        sanitized['deletions'] = int(sanitized['deletions'])
    except (ValueError, TypeError):
        sanitized['insertions'] = 0
        sanitized['deletions'] = 0
    
    return sanitized


def validate_commits(commits: List[Dict], report: ValidationReport) -> List[Dict]:
    """
    Validate list of commits, skip invalid ones.
    Returns list of valid commits.
    """
    valid_commits = []
    report.total_commits_processed = len(commits)
    
    for commit in commits:
        is_valid, error_msg = validate_commit(commit)
        
        if not is_valid:
            report.skipped_commits += 1
            report.add_warning(f"Skipped commit {commit.get('hash', 'unknown')}: {error_msg}")
            continue
        
        valid_commits.append(sanitize_commit(commit))
    
    return valid_commits


def _check_commit_record_fields(commit: Dict) -> tuple[bool, str]:
    """Ensure a commit record contains required inner fields."""
    required = ['hash', 'author', 'message', 'timestamp']
    for f in required:
        if f not in commit or commit[f] is None:
            return False, f"Missing required commit field: {f}"
    return True, ""


def validate_grouped_data(grouped_data: Dict) -> tuple[bool, str]:
    """
    Validate grouper output structure and inner records.
    Returns (is_valid, error_message)
    """
    required_keys = ['grouped_commits', 'stats']

    for key in required_keys:
        if key not in grouped_data:
            return False, f"Missing required key: {key}"

    if not isinstance(grouped_data['grouped_commits'], dict):
        return False, "grouped_commits must be a dictionary"

    if not isinstance(grouped_data['stats'], dict):
        return False, "stats must be a dictionary"

    # Ensure each group maps to a list of commits and each commit has required fields
    for group_id, commits in grouped_data['grouped_commits'].items():
        if not isinstance(commits, list):
            return False, f"group '{group_id}' must contain a list of commits"
        for c in commits:
            if not isinstance(c, dict):
                return False, f"commit in group '{group_id}' must be a dict"
            ok, msg = _check_commit_record_fields(c)
            if not ok:
                return False, f"In group '{group_id}': {msg}"

    return True, ""


def validate_cleaned_data(cleaned_data: Dict) -> tuple[bool, str]:
    """
    Validate cleaner output structure.
    Returns (is_valid, error_message)
    """
    required_keys = ['commits', 'summary_text', 'stats', 'metadata']
    
    for key in required_keys:
        if key not in cleaned_data:
            return False, f"Missing required key: {key}"
    
    if not isinstance(cleaned_data['commits'], list):
        return False, "commits must be a list"
    
    if not isinstance(cleaned_data['summary_text'], str):
        return False, "summary_text must be a string"
    
    # Validate inner commit records
    for idx, c in enumerate(cleaned_data['commits']):
        if not isinstance(c, dict):
            return False, f"commit at index {idx} must be a dict"
        ok, msg = _check_commit_record_fields(c)
        if not ok:
            return False, f"commit at index {idx}: {msg}"

    return True, ""

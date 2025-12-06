"""
Tests for parser validation module.
Ensures data integrity between pipeline stages.
"""
from gitstory.parser.validation import (
    validate_commit,
    sanitize_commit,
    validate_commits,
    validate_grouped_data,
    validate_cleaned_data,
    ValidationReport,
)


class TestCommitValidation:
    """Test individual commit validation."""

    def test_valid_commit(self):
        commit = {
            'hash': 'abc1234',
            'author': 'John Doe',
            'message': 'Fix bug',
            'timestamp': '2025-01-01T12:00:00'
        }
        is_valid, error_msg = validate_commit(commit)
        assert is_valid
        assert error_msg == ""

    def test_missing_hash(self):
        commit = {
            'author': 'John Doe',
            'message': 'Fix bug',
            'timestamp': '2025-01-01T12:00:00'
        }
        is_valid, error_msg = validate_commit(commit)
        assert not is_valid
        assert 'hash' in error_msg

    def test_missing_author(self):
        commit = {
            'hash': 'abc1234',
            'message': 'Fix bug',
            'timestamp': '2025-01-01T12:00:00'
        }
        is_valid, error_msg = validate_commit(commit)
        assert not is_valid
        assert 'author' in error_msg

    def test_missing_message(self):
        commit = {
            'hash': 'abc1234',
            'author': 'John Doe',
            'timestamp': '2025-01-01T12:00:00'
        }
        is_valid, error_msg = validate_commit(commit)
        assert not is_valid
        assert 'message' in error_msg

    def test_missing_timestamp(self):
        commit = {
            'hash': 'abc1234',
            'author': 'John Doe',
            'message': 'Fix bug'
        }
        is_valid, error_msg = validate_commit(commit)
        assert not is_valid
        assert 'timestamp' in error_msg

    def test_invalid_timestamp_format(self):
        commit = {
            'hash': 'abc1234',
            'author': 'John Doe',
            'message': 'Fix bug',
            'timestamp': 'not-a-date'
        }
        is_valid, error_msg = validate_commit(commit)
        assert not is_valid
        assert 'timestamp' in error_msg.lower()


class TestCommitSanitization:
    """Test commit data sanitization."""

    def test_sanitize_valid_commit(self):
        commit = {
            'hash': 'abc1234',
            'author': 'John Doe',
            'message': 'Fix bug',
            'timestamp': '2025-01-01T12:00:00'
        }
        sanitized = sanitize_commit(commit)
        assert sanitized['hash'] == 'abc1234'
        assert sanitized['author'] == 'John Doe'
        assert sanitized['files_changed'] == []
        assert sanitized['insertions'] == 0

    def test_sanitize_invalid_author(self):
        commit = {
            'hash': 'abc1234',
            'author': None,
            'message': 'Fix bug',
            'timestamp': '2025-01-01T12:00:00'
        }
        sanitized = sanitize_commit(commit)
        assert sanitized['author'] == 'Unknown'

    def test_sanitize_missing_message(self):
        commit = {
            'hash': 'abc1234',
            'author': 'John Doe',
            'timestamp': '2025-01-01T12:00:00'
        }
        sanitized = sanitize_commit(commit)
        assert sanitized['message'] == '(No commit message)'

    def test_sanitize_invalid_numeric_fields(self):
        commit = {
            'hash': 'abc1234',
            'author': 'John Doe',
            'message': 'Fix bug',
            'timestamp': '2025-01-01T12:00:00',
            'insertions': 'not-a-number',
            'deletions': 'also-not-a-number'
        }
        sanitized = sanitize_commit(commit)
        assert sanitized['insertions'] == 0
        assert sanitized['deletions'] == 0


class TestCommitsValidation:
    """Test validation of commit lists."""

    def test_validate_all_valid_commits(self):
        commits = [
            {
                'hash': 'abc1234',
                'author': 'John Doe',
                'message': 'Fix bug',
                'timestamp': '2025-01-01T12:00:00'
            },
            {
                'hash': 'def5678',
                'author': 'Jane Doe',
                'message': 'Add feature',
                'timestamp': '2025-01-02T12:00:00'
            }
        ]
        report = ValidationReport()
        valid_commits = validate_commits(commits, report)
        
        assert len(valid_commits) == 2
        assert report.skipped_commits == 0

    def test_skip_invalid_commits(self):
        commits = [
            {
                'hash': 'abc1234',
                'author': 'John Doe',
                'message': 'Fix bug',
                'timestamp': '2025-01-01T12:00:00'
            },
            {
                'hash': 'def5678',
                # Missing author
                'message': 'Add feature',
                'timestamp': '2025-01-02T12:00:00'
            }
        ]
        report = ValidationReport()
        valid_commits = validate_commits(commits, report)
        
        assert len(valid_commits) == 1
        assert report.skipped_commits == 1
        assert len(report.warnings) > 0


class TestGroupedDataValidation:
    """Test validation of grouper output."""

    def test_valid_grouped_data(self):
        grouped = {
            'grouped_commits': {'feature': [], 'bugfix': []},
            'stats': {'total_commits': 0}
        }
        is_valid, error_msg = validate_grouped_data(grouped)
        assert is_valid

    def test_missing_grouped_commits(self):
        grouped = {
            'stats': {'total_commits': 0}
        }
        is_valid, error_msg = validate_grouped_data(grouped)
        assert not is_valid
        assert 'grouped_commits' in error_msg

    def test_missing_stats(self):
        grouped = {
            'grouped_commits': {'feature': []}
        }
        is_valid, error_msg = validate_grouped_data(grouped)
        assert not is_valid
        assert 'stats' in error_msg


class TestCleanedDataValidation:
    """Test validation of cleaner output."""

    def test_valid_cleaned_data(self):
        cleaned = {
            'commits': [],
            'summary_text': 'Summary',
            'stats': {},
            'metadata': {}
        }
        is_valid, error_msg = validate_cleaned_data(cleaned)
        assert is_valid

    def test_missing_commits(self):
        cleaned = {
            'summary_text': 'Summary',
            'stats': {},
            'metadata': {}
        }
        is_valid, error_msg = validate_cleaned_data(cleaned)
        assert not is_valid
        assert 'commits' in error_msg

    def test_missing_summary_text(self):
        cleaned = {
            'commits': [],
            'stats': {},
            'metadata': {}
        }
        is_valid, error_msg = validate_cleaned_data(cleaned)
        assert not is_valid
        assert 'summary_text' in error_msg

    def test_invalid_commits_type(self):
        cleaned = {
            'commits': 'not-a-list',
            'summary_text': 'Summary',
            'stats': {},
            'metadata': {}
        }
        is_valid, error_msg = validate_cleaned_data(cleaned)
        assert not is_valid
        assert 'list' in error_msg.lower()

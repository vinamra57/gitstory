"""
Integration tests for RepoParser fallback behavior.

This test suite verifies the fallback behavior of the RepoParser pipeline:
- When `on_validation_error='raise'` (default): ValidationError is raised on validation failures.
- When `on_validation_error='fallback'`: parser attempts best-effort recovery.

Test Coverage:
  1. Grouper validation failure with fallback enabled → per-commit grouping fallback
  2. Cleaner validation failure with fallback enabled → partial cleaned output
  3. Raise mode (default) → ValidationError raised with report and stage attached
  4. Validation report is populated and exposed correctly
  5. Compare pipeline validates raw_comparison input
"""

import pytest
from unittest.mock import Mock, patch

from gitstory.parser import RepoParser
from gitstory.parser.validation import ValidationError


class TestFallbackBehavior:
    """Test suite for RepoParser fallback behavior on validation failures."""

    @pytest.fixture
    def valid_commit(self):
        """A valid commit with all required fields."""
        return {
            "hash": "abc123",
            "author": "Alice",
            "message": "feat: add feature",
            "timestamp": "2025-01-10T10:00:00",
            "files_changed": ["file1.py"],
            "insertions": 10,
            "deletions": 5,
            "diff": "sample diff",
        }

    @pytest.fixture
    def valid_grouped_output(self, valid_commit):
        """Valid grouper output."""
        return {
            "grouped_commits": {"feature": [valid_commit]},
            "stats": {
                "total_commits": 1,
                "by_type": {"feature": 1},
                "by_author": {"Alice": {"count": 1, "types": {"feature": 1}}},
            },
        }

    @pytest.fixture
    def valid_cleaned_output(self, valid_commit):
        """Valid cleaner output."""
        return {
            "commits": [
                {
                    "hash": "abc123",
                    "author": "Alice",
                    "message": "feat: add feature",
                    "timestamp": "2025-01-10T10:00:00",
                    "type": "feature",
                    "files_changed": 1,
                    "changes": 15,
                }
            ],
            "summary_text": "## Summary\nFeature commits: 1",
            "stats": {"total_commits": 1},
            "metadata": {"total_commits_analyzed": 1},
        }

    def test_grouper_validation_failure_with_raise_mode(
        self, valid_commit, valid_grouped_output
    ):
        """
        Test: Grouper validation fails, raise mode (default).
        Expected: ValidationError raised with stage='grouper' and report attached.
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            # Setup: valid extractor output
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = [valid_commit]
            mock_extractor_class.return_value = mock_extractor

            # Setup: grouper returns output missing 'stats' (will fail validation)
            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = {
                "grouped_commits": {"feature": [valid_commit]}
                # Missing 'stats' key
            }
            mock_grouper_class.return_value = mock_grouper

            mock_cleaner_class.return_value = Mock()

            # Act & Assert
            parser = RepoParser("/test/repo", on_validation_error="raise")

            with pytest.raises(ValidationError) as exc_info:
                parser.parse()

            error = exc_info.value
            assert error.stage == "grouper"
            assert error.report is not None
            assert "Missing required key: stats" in str(error)

    def test_grouper_validation_failure_with_fallback_mode(
        self, valid_commit, valid_cleaned_output
    ):
        """
        Test: Grouper validation fails, fallback mode enabled.
        Expected: Parser constructs per-commit grouping and continues to cleaner.
        Result should contain all valid commits with fallback grouping.
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            # Setup: valid extractor output with multiple commits
            commits = [
                {
                    "hash": f"hash{i}",
                    "author": f"Author{i}",
                    "message": f"commit {i}",
                    "timestamp": f"2025-01-1{i}T10:00:00",
                }
                for i in range(3)
            ]
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = commits
            mock_extractor_class.return_value = mock_extractor

            # Setup: grouper fails validation (missing 'stats')
            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = {
                "grouped_commits": {commit["hash"]: [commit] for commit in commits}
            }
            mock_grouper_class.return_value = mock_grouper

            # Setup: cleaner accepts fallback grouped data
            expected_cleaned = valid_cleaned_output.copy()
            expected_cleaned["commits"] = commits
            mock_cleaner = Mock()
            mock_cleaner.clean_data.return_value = expected_cleaned
            mock_cleaner_class.return_value = mock_cleaner

            # Act
            parser = RepoParser("/test/repo", on_validation_error="fallback")
            result = parser.parse()

            # Assert
            assert result is not None
            assert result["commits"] == commits
            # Verify cleaner was called with per-commit grouping fallback
            call_args = mock_cleaner.clean_data.call_args[0][0]
            assert "grouped_commits" in call_args
            assert len(call_args["grouped_commits"]) == 3
            # Each commit hashed separately
            for commit in commits:
                assert commit["hash"] in call_args["grouped_commits"]

    def test_cleaner_validation_failure_with_raise_mode(
        self, valid_commit, valid_grouped_output
    ):
        """
        Test: Cleaner validation fails, raise mode (default).
        Expected: ValidationError raised with stage='cleaner' and report attached.
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            # Setup: valid up to cleaner
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = [valid_commit]
            mock_extractor_class.return_value = mock_extractor

            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = valid_grouped_output
            mock_grouper_class.return_value = mock_grouper

            # Setup: cleaner output missing 'commits' (will fail validation)
            mock_cleaner = Mock()
            mock_cleaner.clean_data.return_value = {
                "summary_text": "Summary",
                "stats": {},
                "metadata": {},
                # Missing 'commits'
            }
            mock_cleaner_class.return_value = mock_cleaner

            # Act & Assert
            parser = RepoParser("/test/repo", on_validation_error="raise")

            with pytest.raises(ValidationError) as exc_info:
                parser.parse()

            error = exc_info.value
            assert error.stage == "cleaner"
            assert error.report is not None
            assert "Missing required key: commits" in str(error)

    def test_cleaner_validation_failure_with_fallback_mode(
        self, valid_commit, valid_grouped_output
    ):
        """
        Test: Cleaner validation fails, fallback mode enabled.
        Expected: Parser returns partial cleaned data with validated commits and report.
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            # Setup: valid up to cleaner
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = [valid_commit]
            mock_extractor_class.return_value = mock_extractor

            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = valid_grouped_output
            mock_grouper_class.return_value = mock_grouper

            # Setup: cleaner output fails validation
            mock_cleaner = Mock()
            mock_cleaner.clean_data.return_value = {
                "summary_text": "Summary",
                # Missing 'commits'
            }
            mock_cleaner_class.return_value = mock_cleaner

            # Act
            parser = RepoParser("/test/repo", on_validation_error="fallback")
            result = parser.parse()

            # Assert: partial cleaned output returned
            assert result is not None
            assert result["commits"] == [valid_commit]  # Original validated commits
            assert result["summary_text"] == "Partial summary (cleaner validation failed)"
            assert result["metadata"]["validation_report"] is not None
            # Verify fallback warning was recorded
            report = result["metadata"]["validation_report"]
            assert len(report["warnings"]) > 0, f"Expected warnings but got: {report['warnings']}"
            assert any("Cleaner output validation failed" in w for w in report["warnings"])

    def test_empty_commits_raises_validation_error_in_raise_mode(self):
        """
        Test: No valid commits after extraction/validation.
        Expected: ValidationError raised with stage='commits' in raise mode.
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            # Setup: extractor returns empty or all invalid commits
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = []
            mock_extractor_class.return_value = mock_extractor

            mock_grouper_class.return_value = Mock()
            mock_cleaner_class.return_value = Mock()

            # Act & Assert
            parser = RepoParser("/test/repo", on_validation_error="raise")

            with pytest.raises(ValidationError) as exc_info:
                parser.parse()

            error = exc_info.value
            assert error.stage == "commits"
            assert "No valid commits found" in str(error)

    def test_validation_report_attached_to_error(self, valid_commit):
        """
        Test: ValidationError carries validation_report snapshot with details.
        Expected: report contains skipped_commits count and warnings.
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            # Setup: one valid, one invalid commit
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = [
                valid_commit,
                {
                    "hash": "bad123",
                    "author": "Bob",
                    # Missing 'message' and 'timestamp'
                },
            ]
            mock_extractor_class.return_value = mock_extractor

            # Setup: grouper fails so we can inspect the report
            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = {
                "grouped_commits": {valid_commit["hash"]: [valid_commit]}
                # Missing 'stats'
            }
            mock_grouper_class.return_value = mock_grouper

            mock_cleaner_class.return_value = Mock()

            # Act & Assert
            parser = RepoParser("/test/repo", on_validation_error="raise")

            with pytest.raises(ValidationError) as exc_info:
                parser.parse()

            error = exc_info.value
            report = error.report
            assert report is not None
            assert report["skipped_commits"] == 1  # One invalid commit
            assert len(report["warnings"]) > 0  # Contains warning about bad commit

    def test_default_behavior_is_raise_mode(self, valid_commit, valid_grouped_output):
        """
        Test: When on_validation_error is not specified, default is 'raise'.
        Expected: ValidationError raised on validation failure (not fallback).
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = [valid_commit]
            mock_extractor_class.return_value = mock_extractor

            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = {"grouped_commits": {}}
            # Missing 'stats'
            mock_grouper_class.return_value = mock_grouper

            mock_cleaner_class.return_value = Mock()

            # Act & Assert: default mode should raise
            parser = RepoParser("/test/repo")  # No on_validation_error specified

            with pytest.raises(ValidationError):
                parser.parse()


class TestComparisonValidation:
    """Test suite for RepoParser.compare() input validation."""

    @patch("gitstory.parser.GitExtractor")
    @patch("gitstory.parser.CommitGrouper")
    @patch("gitstory.parser.DataCleaner")
    @patch("gitstory.parser.BranchComparator")
    def test_compare_validates_raw_comparison_keys(
        self, mock_comparator_class, mock_cleaner_class, mock_grouper_class, mock_extractor_class
    ):
        """
        Test: compare() validates raw_comparison has required keys.
        Expected: ValidationError raised if keys are missing.
        """
        # Setup: extractor returns malformed comparison (missing 'merge_base')
        mock_extractor = Mock()
        mock_extractor.compare_branches.return_value = {
            "base_only_commits": [],
            "compare_only_commits": [],
            "context_commits": [],
            # Missing 'merge_base', 'base_branch', 'compare_branch'
        }
        mock_extractor_class.return_value = mock_extractor

        mock_grouper_class.return_value = Mock()
        mock_cleaner_class.return_value = Mock()
        mock_comparator_class.return_value = Mock()

        # Act & Assert
        parser = RepoParser("/test/repo")

        with pytest.raises(ValidationError) as exc_info:
            parser.compare("main", "develop")

        error = exc_info.value
        assert error.stage == "compare"
        assert "compare_branches output missing keys" in str(error)

    @patch("gitstory.parser.GitExtractor")
    @patch("gitstory.parser.CommitGrouper")
    @patch("gitstory.parser.DataCleaner")
    @patch("gitstory.parser.BranchComparator")
    def test_compare_validates_list_types(
        self, mock_comparator_class, mock_cleaner_class, mock_grouper_class, mock_extractor_class
    ):
        """
        Test: compare() validates base/compare commits are lists.
        Expected: ValidationError raised if types are wrong.
        """
        # Setup: extractor returns commits as dicts instead of lists
        mock_extractor = Mock()
        mock_extractor.compare_branches.return_value = {
            "base_only_commits": {},  # Should be list
            "compare_only_commits": {},  # Should be list
            "context_commits": [],
            "merge_base": "abc123",
            "base_branch": "main",
            "compare_branch": "develop",
        }
        mock_extractor_class.return_value = mock_extractor

        mock_grouper_class.return_value = Mock()
        mock_cleaner_class.return_value = Mock()
        mock_comparator_class.return_value = Mock()

        # Act & Assert
        parser = RepoParser("/test/repo")

        with pytest.raises(ValidationError) as exc_info:
            parser.compare("main", "develop")

        error = exc_info.value
        assert error.stage == "compare"
        assert "expected lists" in str(error)

    @patch("gitstory.parser.GitExtractor")
    @patch("gitstory.parser.CommitGrouper")
    @patch("gitstory.parser.DataCleaner")
    @patch("gitstory.parser.BranchComparator")
    def test_compare_with_valid_input_proceeds(
        self, mock_comparator_class, mock_cleaner_class, mock_grouper_class, mock_extractor_class
    ):
        """
        Test: compare() proceeds when raw_comparison is valid.
        Expected: No ValidationError raised, comparator processes data.
        """
        # Setup: valid comparison output
        mock_extractor = Mock()
        mock_extractor.compare_branches.return_value = {
            "base_only_commits": [],
            "compare_only_commits": [
                {
                    "hash": "new123",
                    "author": "Alice",
                    "message": "new feature",
                    "timestamp": "2025-01-10T10:00:00",
                }
            ],
            "context_commits": [],
            "merge_base": "merge123",
            "base_branch": "main",
            "compare_branch": "feature",
        }
        mock_extractor_class.return_value = mock_extractor

        mock_grouper_class.return_value = Mock()
        mock_cleaner_class.return_value = Mock()

        mock_comparator = Mock()
        mock_comparator.process_comparison.return_value = {}
        mock_comparator_class.return_value = mock_comparator

        # Act
        parser = RepoParser("/test/repo")
        # Should not raise
        parser.compare("main", "feature")

        # Assert: comparator was called
        mock_comparator.process_comparison.assert_called_once()


class TestValidationReportExposure:
    """Test suite for ValidationReport exposure and accessibility."""

    def test_validation_report_in_successful_parse_metadata(self, ):
        """
        Test: Successful parse includes validation_report in metadata.
        Expected: metadata['validation_report'] contains skipped_commits and warnings.
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            # Setup: one valid, one invalid (skipped)
            valid_commit = {
                "hash": "abc123",
                "author": "Alice",
                "message": "feat: feature",
                "timestamp": "2025-01-10T10:00:00",
            }
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = [
                valid_commit,
                {"hash": "bad", "author": "Bob"},  # Invalid, will be skipped
            ]
            mock_extractor_class.return_value = mock_extractor

            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = {
                "grouped_commits": {valid_commit["hash"]: [valid_commit]},
                "stats": {"total_commits": 1},
            }
            mock_grouper_class.return_value = mock_grouper

            mock_cleaner = Mock()
            mock_cleaner.clean_data.return_value = {
                "commits": [valid_commit],
                "summary_text": "Summary",
                "stats": {},
                "metadata": {},
            }
            mock_cleaner_class.return_value = mock_cleaner

            # Act
            parser = RepoParser("/test/repo")
            result = parser.parse()

            # Assert
            assert "metadata" in result
            assert "validation_report" in result["metadata"]
            report = result["metadata"]["validation_report"]
            assert report["skipped_commits"] == 1
            assert len(report["warnings"]) > 0
            assert "bad" in str(report["warnings"])


class TestInnerRecordValidation:
    """Test suite for inner-record validation (commit fields in grouped/cleaned data)."""

    def test_grouped_data_inner_commit_validation(self):
        """
        Test: validate_grouped_data checks that commits in groups have required fields.
        Expected: ValidationError if a commit is missing hash/author/message/timestamp.
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            valid_commit = {
                "hash": "abc123",
                "author": "Alice",
                "message": "feat: feature",
                "timestamp": "2025-01-10T10:00:00",
            }
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = [valid_commit]
            mock_extractor_class.return_value = mock_extractor

            # Grouper returns a commit with missing 'timestamp' in a group
            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = {
                "grouped_commits": {
                    "feature": [
                        {
                            "hash": "abc123",
                            "author": "Alice",
                            "message": "feat: feature",
                            # Missing 'timestamp'
                        }
                    ]
                },
                "stats": {"total_commits": 1},
            }
            mock_grouper_class.return_value = mock_grouper

            mock_cleaner_class.return_value = Mock()

            # Act & Assert
            parser = RepoParser("/test/repo", on_validation_error="raise")

            with pytest.raises(ValidationError) as exc_info:
                parser.parse()

            error = exc_info.value
            assert error.stage == "grouper"
            assert "Missing required commit field: timestamp" in str(error)

    def test_cleaned_data_inner_commit_validation(self):
        """
        Test: validate_cleaned_data checks that cleaned commits have required fields.
        Expected: ValidationError if a cleaned commit is missing required fields.
        """
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            valid_commit = {
                "hash": "abc123",
                "author": "Alice",
                "message": "feat: feature",
                "timestamp": "2025-01-10T10:00:00",
            }
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = [valid_commit]
            mock_extractor_class.return_value = mock_extractor

            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = {
                "grouped_commits": {"feature": [valid_commit]},
                "stats": {"total_commits": 1},
            }
            mock_grouper_class.return_value = mock_grouper

            # Cleaner returns cleaned commit with missing 'author'
            mock_cleaner = Mock()
            mock_cleaner.clean_data.return_value = {
                "commits": [
                    {
                        "hash": "abc123",
                        "message": "feat: feature",
                        "timestamp": "2025-01-10T10:00:00",
                        # Missing 'author'
                    }
                ],
                "summary_text": "Summary",
                "stats": {},
                "metadata": {},
            }
            mock_cleaner_class.return_value = mock_cleaner

            # Act & Assert
            parser = RepoParser("/test/repo", on_validation_error="raise")

            with pytest.raises(ValidationError) as exc_info:
                parser.parse()

            error = exc_info.value
            assert error.stage == "cleaner"
            assert "Missing required commit field: author" in str(error)

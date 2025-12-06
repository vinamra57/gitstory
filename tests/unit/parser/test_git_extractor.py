"""
Comprehensive unit tests for GitExtractor.

This test suite implements:
- Black-box testing with boundary value analysis
- White-box testing with MC/DC (Modified Condition/Decision Coverage)
- Systematic edge case testing
- Mock-based isolation testing

Test Count: 28 tests
Coverage Target: 95%+ branch coverage
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from git import InvalidGitRepositoryError

from gitstory.parser.git_extractor import GitExtractor


class TestGitExtractorInitialization:
    """Test suite for GitExtractor initialization."""

    @patch("gitstory.parser.git_extractor.Repo")
    def test_init_with_valid_repo(self, mock_repo_class):
        """Test successful initialization with valid Git repository."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo

        # Act
        extractor = GitExtractor("/valid/repo/path")

        # Assert
        assert extractor.repo is mock_repo
        mock_repo_class.assert_called_once_with("/valid/repo/path")

    @patch("gitstory.parser.git_extractor.Repo")
    def test_init_with_invalid_repo_raises_error(self, mock_repo_class):
        """Test initialization fails with invalid Git repository."""
        # Arrange
        mock_repo_class.side_effect = InvalidGitRepositoryError("Not a git repo")

        # Act & Assert
        with pytest.raises(InvalidGitRepositoryError) as exc_info:
            GitExtractor("/invalid/path")

        assert "Not a valid Git repository" in str(exc_info.value)
        assert "/invalid/path" in str(exc_info.value)

    @patch("gitstory.parser.git_extractor.Repo")
    def test_init_with_nonexistent_path(self, mock_repo_class):
        """Test initialization with non-existent path."""
        # Arrange
        mock_repo_class.side_effect = InvalidGitRepositoryError("Path does not exist")

        # Act & Assert
        with pytest.raises(InvalidGitRepositoryError):
            GitExtractor("/nonexistent/path")


class TestParseTimeMethodMCDC:
    """
    Test suite for _parse_time() method with MC/DC coverage.

    This method has complex conditional logic:
    1. Try ISO format
    2. Try relative format with regex
    3. Check unit type (d/w/m)
    4. Raise ValueError if no match

    MC/DC requires testing each condition independently affects outcome.
    """

    def setup_extractor(self):
        """Helper to create GitExtractor instance."""
        with patch("gitstory.parser.git_extractor.Repo") as mock_repo_class:
            mock_repo = Mock()
            mock_repo_class.return_value = mock_repo
            return GitExtractor("/fake/path")

    @patch("gitstory.parser.git_extractor.Repo")
    def test_parse_time_valid_iso_format(self, mock_repo_class):
        """MC/DC Test 1: Valid ISO format → success (ISO path taken)."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        iso_time = "2025-01-10T10:00:00"
        expected = datetime(2025, 1, 10, 10, 0, 0)

        # Act
        result = extractor._parse_time(iso_time)

        # Assert
        assert result == expected

    @patch("gitstory.parser.git_extractor.Repo")
    def test_parse_time_invalid_iso_valid_relative_days(self, mock_repo_class):
        """MC/DC Test 2: Invalid ISO, valid relative '1d' → success (relative path, days)."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        # Act
        with patch("gitstory.parser.git_extractor.datetime") as mock_datetime:
            mock_datetime.fromisoformat.side_effect = ValueError("Invalid ISO")
            mock_now = datetime(2025, 1, 10, 10, 0, 0)
            mock_datetime.now.return_value = mock_now
            result = extractor._parse_time("1d")

        # Assert
        expected = mock_now - timedelta(days=1)
        assert result == expected

    @patch("gitstory.parser.git_extractor.Repo")
    def test_parse_time_invalid_iso_valid_relative_weeks(self, mock_repo_class):
        """MC/DC Test 3: Invalid ISO, valid relative '2w' → success (relative path, weeks)."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        # Act
        with patch("gitstory.parser.git_extractor.datetime") as mock_datetime:
            mock_datetime.fromisoformat.side_effect = ValueError("Invalid ISO")
            mock_now = datetime(2025, 1, 10, 10, 0, 0)
            mock_datetime.now.return_value = mock_now
            result = extractor._parse_time("2w")

        # Assert
        expected = mock_now - timedelta(weeks=2)
        assert result == expected

    @patch("gitstory.parser.git_extractor.Repo")
    def test_parse_time_invalid_iso_valid_relative_months(self, mock_repo_class):
        """MC/DC Test 4: Invalid ISO, valid relative '3m' → success (relative path, months)."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        # Act
        with patch("gitstory.parser.git_extractor.datetime") as mock_datetime:
            mock_datetime.fromisoformat.side_effect = ValueError("Invalid ISO")
            mock_now = datetime(2025, 1, 10, 10, 0, 0)
            mock_datetime.now.return_value = mock_now
            result = extractor._parse_time("3m")

        # Assert
        expected = mock_now - timedelta(days=90)  # 3 * 30
        assert result == expected

    @patch("gitstory.parser.git_extractor.Repo")
    def test_parse_time_invalid_iso_valid_relative_years(self, mock_repo_class):
        """MC/DC Test 5: Invalid ISO, valid relative '2y' → success (relative path, years)."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        # Act
        with patch("gitstory.parser.git_extractor.datetime") as mock_datetime:
            mock_datetime.fromisoformat.side_effect = ValueError("Invalid ISO")
            mock_now = datetime(2025, 1, 10, 10, 0, 0)
            mock_datetime.now.return_value = mock_now
            result = extractor._parse_time("2y")

        # Assert
        expected = mock_now - timedelta(days=730)  # 2 * 365
        assert result == expected

    @patch("gitstory.parser.git_extractor.Repo")
    def test_parse_time_invalid_iso_invalid_relative(self, mock_repo_class):
        """MC/DC Test 6: Invalid ISO, invalid relative → ValueError."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            extractor._parse_time("invalid_format")

        assert "Invalid time format" in str(exc_info.value)

    @patch("gitstory.parser.git_extractor.Repo")
    def test_parse_time_invalid_unit(self, mock_repo_class):
        """MC/DC Test 7: Invalid ISO, invalid unit '1x' → ValueError."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            extractor._parse_time("1x")

        assert "Invalid time format" in str(exc_info.value)

    @patch("gitstory.parser.git_extractor.Repo")
    def test_parse_time_boundary_zero_days(self, mock_repo_class):
        """Boundary Test: Zero days '0d' → current time."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        # Act
        with patch("gitstory.parser.git_extractor.datetime") as mock_datetime:
            mock_datetime.fromisoformat.side_effect = ValueError("Invalid ISO")
            mock_now = datetime(2025, 1, 10, 10, 0, 0)
            mock_datetime.now.return_value = mock_now
            result = extractor._parse_time("0d")

        # Assert
        assert result == mock_now

    @patch("gitstory.parser.git_extractor.Repo")
    def test_parse_time_large_value(self, mock_repo_class):
        """Boundary Test: Large value '365d' → 1 year ago."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        # Act
        with patch("gitstory.parser.git_extractor.datetime") as mock_datetime:
            mock_datetime.fromisoformat.side_effect = ValueError("Invalid ISO")
            mock_now = datetime(2025, 1, 10, 10, 0, 0)
            mock_datetime.now.return_value = mock_now
            result = extractor._parse_time("365d")

        # Assert
        expected = mock_now - timedelta(days=365)
        assert result == expected


class TestGetCommitsFiltering:
    """Test suite for get_commits() method with filtering logic."""

    def create_mock_commit(self, hexsha, message, commit_date):
        """Helper to create mock commit."""
        commit = Mock()
        commit.hexsha = hexsha
        commit.author.name = "Test Author"
        commit.author.email = "test@example.com"
        commit.committed_date = commit_date.timestamp()
        commit.message = message
        commit.parents = [Mock()]  # Has parents
        commit.stats.total = {"insertions": 10, "deletions": 5}

        # Mock diff
        diff_item = Mock()
        diff_item.a_path = "test.py"
        diff_item.diff = b"diff content"
        commit.parents[0].diff.return_value = [diff_item]

        return commit

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commits_no_filters(self, mock_repo_class):
        """Test get_commits() with no filters returns all commits."""
        # Arrange
        mock_repo = Mock()
        mock_repo.active_branch.name = "main"

        commit1 = self.create_mock_commit(
            "abc123", "feat: test", datetime(2025, 1, 10, 10, 0)
        )
        commit2 = self.create_mock_commit(
            "def456", "fix: bug", datetime(2025, 1, 9, 10, 0)
        )

        mock_repo.iter_commits.return_value = [commit1, commit2]
        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act
        result = extractor.get_commits()

        # Assert
        assert len(result) == 2
        assert result[0]["hash"] == "abc123"[:8]
        assert result[1]["hash"] == "def456"[:8]

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commits_with_since_excludes_older(self, mock_repo_class):
        """Test get_commits() with since parameter excludes older commits."""
        # Arrange
        mock_repo = Mock()
        mock_repo.active_branch.name = "main"

        commit1 = self.create_mock_commit(
            "abc123", "feat: new", datetime(2025, 1, 10, 10, 0)
        )
        commit2 = self.create_mock_commit(
            "def456", "fix: old", datetime(2025, 1, 5, 10, 0)
        )

        mock_repo.iter_commits.return_value = [commit1, commit2]
        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act
        result = extractor.get_commits(since="2025-01-08T00:00:00")

        # Assert
        assert len(result) == 1
        assert result[0]["hash"] == "abc123"[:8]

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commits_with_until_excludes_newer(self, mock_repo_class):
        """Test get_commits() with until parameter excludes newer commits."""
        # Arrange
        mock_repo = Mock()
        mock_repo.active_branch.name = "main"

        commit1 = self.create_mock_commit(
            "abc123", "feat: new", datetime(2025, 1, 10, 10, 0)
        )
        commit2 = self.create_mock_commit(
            "def456", "fix: old", datetime(2025, 1, 5, 10, 0)
        )

        mock_repo.iter_commits.return_value = [commit1, commit2]
        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act
        result = extractor.get_commits(until="2025-01-08T00:00:00")

        # Assert
        assert len(result) == 1
        assert result[0]["hash"] == "def456"[:8]

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commits_with_both_since_and_until(self, mock_repo_class):
        """Test get_commits() with both since and until filters."""
        # Arrange
        mock_repo = Mock()
        mock_repo.active_branch.name = "main"

        commit1 = self.create_mock_commit(
            "abc123", "feat: new", datetime(2025, 1, 15, 10, 0)
        )
        commit2 = self.create_mock_commit(
            "def456", "fix: mid", datetime(2025, 1, 10, 10, 0)
        )
        commit3 = self.create_mock_commit(
            "ghi789", "chore: old", datetime(2025, 1, 5, 10, 0)
        )

        mock_repo.iter_commits.return_value = [commit1, commit2, commit3]
        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act
        result = extractor.get_commits(
            since="2025-01-08T00:00:00", until="2025-01-12T00:00:00"
        )

        # Assert
        assert len(result) == 1
        assert result[0]["hash"] == "def456"[:8]

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commits_specific_branch(self, mock_repo_class):
        """Test get_commits() with specific branch parameter."""
        # Arrange
        mock_repo = Mock()
        mock_repo.active_branch.name = "main"
        
        # Mock branches to include the requested branch
        mock_branch1 = Mock()
        mock_branch1.name = "main"
        mock_branch2 = Mock()
        mock_branch2.name = "feature-branch"
        mock_repo.branches = [mock_branch1, mock_branch2]

        commit1 = self.create_mock_commit(
            "abc123", "feat: test", datetime(2025, 1, 10, 10, 0)
        )

        mock_repo.iter_commits.return_value = [commit1]
        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act
        result = extractor.get_commits(branch="feature-branch")

        # Assert
        mock_repo.iter_commits.assert_called_once_with("feature-branch")
        assert len(result) == 1

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commits_none_branch_uses_active(self, mock_repo_class):
        """Test get_commits() with None branch uses active branch."""
        # Arrange
        mock_repo = Mock()
        mock_repo.active_branch.name = "main"
        
        # Mock branches
        mock_branch = Mock()
        mock_branch.name = "main"
        mock_repo.branches = [mock_branch]

        commit1 = self.create_mock_commit(
            "abc123", "feat: test", datetime(2025, 1, 10, 10, 0)
        )

        mock_repo.iter_commits.return_value = [commit1]
        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act
        extractor.get_commits(branch=None)

        # Assert
        mock_repo.iter_commits.assert_called_once_with("main")

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commits_nonexistent_branch_raises_error(self, mock_repo_class):
        """Test get_commits() with nonexistent branch raises ValueError."""
        # Arrange
        mock_repo = Mock()
        mock_repo.active_branch.name = "main"
        
        # Mock branches - only main exists
        mock_branch = Mock()
        mock_branch.name = "main"
        mock_repo.branches = [mock_branch]

        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act & Assert
        with pytest.raises(ValueError, match="Branch not found: nonexistent"):
            extractor.get_commits(branch="nonexistent")


class TestGetChangedFiles:
    """Test suite for _get_changed_files() method."""

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_changed_files_initial_commit(self, mock_repo_class):
        """Test _get_changed_files() with initial commit (no parents) returns empty list."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        commit = Mock()
        commit.parents = []  # No parents

        # Act
        result = extractor._get_changed_files(commit)

        # Assert
        assert result == []

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_changed_files_normal_commit(self, mock_repo_class):
        """Test _get_changed_files() with normal commit returns file list."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        commit = Mock()
        parent = Mock()
        commit.parents = [parent]

        diff_item1 = Mock()
        diff_item1.a_path = "file1.py"
        diff_item2 = Mock()
        diff_item2.a_path = "file2.py"

        parent.diff.return_value = [diff_item1, diff_item2]

        # Act
        result = extractor._get_changed_files(commit)

        # Assert
        assert result == ["file1.py", "file2.py"]

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_changed_files_empty_diff(self, mock_repo_class):
        """Test _get_changed_files() with empty diff returns empty list."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        commit = Mock()
        parent = Mock()
        commit.parents = [parent]
        parent.diff.return_value = []

        # Act
        result = extractor._get_changed_files(commit)

        # Assert
        assert result == []


class TestGetCommitDiff:
    """Test suite for _get_commit_diff() method."""

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commit_diff_initial_commit(self, mock_repo_class):
        """Test _get_commit_diff() with initial commit shows added files."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        commit = Mock()
        commit.parents = []

        tree_item1 = Mock()
        tree_item1.path = "README.md"
        tree_item2 = Mock()
        tree_item2.path = "main.py"

        commit.tree.traverse.return_value = [tree_item1, tree_item2]

        # Act
        result = extractor._get_commit_diff(commit)

        # Assert
        assert "A README.md" in result
        assert "A main.py" in result

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commit_diff_normal_commit(self, mock_repo_class):
        """Test _get_commit_diff() with normal commit returns diff text."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        commit = Mock()
        parent = Mock()
        commit.parents = [parent]

        diff_item = Mock()
        diff_item.diff = b"diff --git a/file.py b/file.py\n+new line"

        parent.diff.return_value = [diff_item]

        # Act
        result = extractor._get_commit_diff(commit)

        # Assert
        assert "diff --git a/file.py b/file.py" in result
        assert "+new line" in result

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commit_diff_encoding_error(self, mock_repo_class):
        """Test _get_commit_diff() handles encoding errors gracefully."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        commit = Mock()
        parent = Mock()
        commit.parents = [parent]

        diff_item = Mock()
        # Binary data with invalid UTF-8
        diff_item.diff = b"\xff\xfe invalid utf-8"

        parent.diff.return_value = [diff_item]

        # Act
        result = extractor._get_commit_diff(commit)

        # Assert
        # Should not raise exception, uses errors='ignore'
        assert isinstance(result, str)

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commit_diff_non_bytes_diff(self, mock_repo_class):
        """Test _get_commit_diff() handles non-bytes diff."""
        # Arrange
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        extractor = GitExtractor("/fake/path")

        commit = Mock()
        parent = Mock()
        commit.parents = [parent]

        diff_item = Mock()
        diff_item.diff = "string diff"  # Not bytes

        parent.diff.return_value = [diff_item]

        # Act
        result = extractor._get_commit_diff(commit)

        # Assert
        assert "string diff" in result


class TestBranchMethods:
    """Test suite for branch-related methods."""

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_branch_list(self, mock_repo_class):
        """Test get_branch_list() returns all branch names."""
        # Arrange
        mock_repo = Mock()

        branch1 = Mock()
        branch1.name = "main"
        branch2 = Mock()
        branch2.name = "develop"
        branch3 = Mock()
        branch3.name = "feature/test"

        mock_repo.branches = [branch1, branch2, branch3]
        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act
        result = extractor.get_branch_list()

        # Assert
        assert result == ["main", "develop", "feature/test"]

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_current_branch(self, mock_repo_class):
        """Test get_current_branch() returns active branch name."""
        # Arrange
        mock_repo = Mock()
        mock_repo.active_branch.name = "main"
        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act
        result = extractor.get_current_branch()

        # Assert
        assert result == "main"


class TestGetCommitsDiffErrorHandling:
    """Test suite for diff error handling in get_commits()."""

    @patch("gitstory.parser.git_extractor.Repo")
    def test_get_commits_handles_diff_extraction_error(self, mock_repo_class):
        """Test get_commits() handles diff extraction errors gracefully."""
        # Arrange
        mock_repo = Mock()
        mock_repo.active_branch.name = "main"

        commit = Mock()
        commit.hexsha = "abc123"
        commit.author.name = "Test Author"
        commit.author.email = "test@example.com"
        commit.committed_date = datetime(2025, 1, 10, 10, 0).timestamp()
        commit.message = "test"
        commit.parents = [Mock()]
        commit.stats.total = {"insertions": 0, "deletions": 0}

        # Mock diff to work for _get_changed_files but raise exception for _get_commit_diff
        def diff_side_effect(*args, **kwargs):
            if "create_patch" in kwargs:
                raise Exception("Diff error")
            else:
                # For _get_changed_files, return empty list
                return []

        commit.parents[0].diff.side_effect = diff_side_effect

        mock_repo.iter_commits.return_value = [commit]
        mock_repo_class.return_value = mock_repo

        extractor = GitExtractor("/fake/path")

        # Act
        result = extractor.get_commits()

        # Assert
        assert len(result) == 1
        assert "Error extracting diff" in result[0]["diff"]

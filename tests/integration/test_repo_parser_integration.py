"""
Integration tests for RepoParser (full parser pipeline).

This test suite tests the integration between:
- GitExtractor → CommitGrouper → DataCleaner

Test Count: 10+ tests
Coverage Target: 100% for parser/__init__.py
"""

import pytest
from unittest.mock import Mock, patch

from gitstory.parser import RepoParser


class TestRepoParserInitialization:
    """Test suite for RepoParser initialization."""

    @patch("gitstory.parser.GitExtractor")
    def test_init_creates_extractor(self, mock_extractor_class):
        """Test RepoParser initialization creates GitExtractor."""
        # Arrange
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor

        # Act
        parser = RepoParser("/test/repo")

        # Assert
        mock_extractor_class.assert_called_once_with("/test/repo")
        assert parser.extractor is mock_extractor

    @patch("gitstory.parser.GitExtractor")
    @patch("gitstory.parser.CommitGrouper")
    def test_init_creates_grouper(self, mock_grouper_class, mock_extractor_class):
        """Test RepoParser initialization creates CommitGrouper."""
        # Arrange
        mock_grouper = Mock()
        mock_grouper_class.return_value = mock_grouper

        # Act
        parser = RepoParser("/test/repo")

        # Assert
        mock_grouper_class.assert_called_once()
        assert parser.grouper is mock_grouper

    @patch("gitstory.parser.GitExtractor")
    @patch("gitstory.parser.CommitGrouper")
    @patch("gitstory.parser.DataCleaner")
    def test_init_creates_cleaner(
        self, mock_cleaner_class, mock_grouper_class, mock_extractor_class
    ):
        """Test RepoParser initialization creates DataCleaner."""
        # Arrange
        mock_cleaner = Mock()
        mock_cleaner_class.return_value = mock_cleaner

        # Act
        parser = RepoParser("/test/repo")

        # Assert
        mock_cleaner_class.assert_called_once()
        assert parser.cleaner is mock_cleaner


class TestRepoParserPipeline:
    """Test suite for RepoParser full pipeline integration."""

    @pytest.fixture
    def mock_components(self):
        """Create mock components for testing."""
        with (
            patch("gitstory.parser.GitExtractor") as mock_extractor_class,
            patch("gitstory.parser.CommitGrouper") as mock_grouper_class,
            patch("gitstory.parser.DataCleaner") as mock_cleaner_class,
        ):
            # Setup mock extractor
            mock_extractor = Mock()
            mock_extractor.get_commits.return_value = [
                {
                    "hash": "abc123",
                    "author": "Alice",
                    "timestamp": "2025-01-10T10:00:00",
                    "message": "feat: add feature",
                    "files_changed": ["file1.py"],
                    "insertions": 10,
                    "deletions": 5,
                    "diff": "sample diff",
                }
            ]
            mock_extractor_class.return_value = mock_extractor

            # Setup mock grouper
            mock_grouper = Mock()
            mock_grouper.group_commits.return_value = {
                "grouped_commits": {
                    "feature": [
                        {
                            "hash": "abc123",
                            "author": "Alice",
                            "timestamp": "2025-01-10T10:00:00",
                            "message": "feat: add feature",
                            "files_changed": ["file1.py"],
                            "insertions": 10,
                            "deletions": 5,
                            "diff": "sample diff",
                        }
                    ]
                },
                "stats": {
                    "total_commits": 1,
                    "by_type": {"feature": 1},
                    "by_author": {"Alice": {"count": 1, "types": {"feature": 1}}},
                },
            }
            mock_grouper_class.return_value = mock_grouper

            # Setup mock cleaner
            mock_cleaner = Mock()
            mock_cleaner.clean_data.return_value = {
                "commits": [
                    {
                        "hash": "abc123",
                        "author": "Alice",
                        "timestamp": "2025-01-10T10:00:00",
                        "message": "feat: add feature",
                        "type": "feature",
                        "files_changed": 1,
                        "changes": 15,
                        "diff_chunks": ["sample diff"],
                    }
                ],
                "summary_text": "## FEATURE COMMITS (1 total)\n- [abc123] Alice: feat: add feature",
                "stats": {
                    "total_commits": 1,
                    "by_type": {"feature": 1},
                    "by_author": {"Alice": {"count": 1, "types": {"feature": 1}}},
                },
                "metadata": {
                    "total_commits_analyzed": 1,
                    "commit_types_present": ["feature"],
                },
            }
            mock_cleaner_class.return_value = mock_cleaner

            yield {
                "extractor": mock_extractor,
                "grouper": mock_grouper,
                "cleaner": mock_cleaner,
            }

    def test_parse_calls_extractor(self, mock_components):
        """Test parse() calls GitExtractor.get_commits()."""
        # Arrange
        parser = RepoParser("/test/repo")

        # Act
        parser.parse(since="2025-01-01", until="2025-01-31", branch="main")

        # Assert
        mock_components["extractor"].get_commits.assert_called_once_with(
            "2025-01-01", "2025-01-31", "main"
        )

    def test_parse_calls_grouper(self, mock_components):
        """Test parse() calls CommitGrouper.group_commits() with extractor output."""
        # Arrange
        parser = RepoParser("/test/repo")
        raw_commits = mock_components["extractor"].get_commits.return_value

        # Act
        parser.parse()

        # Assert
        mock_components["grouper"].group_commits.assert_called_once_with(raw_commits)

    def test_parse_calls_cleaner(self, mock_components):
        """Test parse() calls DataCleaner.clean_data() with grouper output."""
        # Arrange
        parser = RepoParser("/test/repo")
        grouped_data = mock_components["grouper"].group_commits.return_value

        # Act
        parser.parse()

        # Assert
        mock_components["cleaner"].clean_data.assert_called_once_with(grouped_data)

    def test_parse_returns_cleaned_data(self, mock_components):
        """Test parse() returns DataCleaner output."""
        # Arrange
        parser = RepoParser("/test/repo")
        expected_result = mock_components["cleaner"].clean_data.return_value

        # Act
        result = parser.parse()

        # Assert
        assert result == expected_result
        assert result["commits"][0]["hash"] == "abc123"
        assert result["metadata"]["total_commits_analyzed"] == 1

    def test_parse_pipeline_flow(self, mock_components):
        """Test complete pipeline flow: extractor → grouper → cleaner."""
        # Arrange
        parser = RepoParser("/test/repo")

        # Act
        parser.parse(since="2025-01-01")

        # Assert - verify call order
        assert mock_components["extractor"].get_commits.called
        assert mock_components["grouper"].group_commits.called
        assert mock_components["cleaner"].clean_data.called

        # Verify data flows correctly
        # Extractor output → Grouper input
        extractor_output = mock_components["extractor"].get_commits.return_value
        grouper_input = mock_components["grouper"].group_commits.call_args[0][0]
        assert grouper_input == extractor_output

        # Grouper output → Cleaner input
        grouper_output = mock_components["grouper"].group_commits.return_value
        cleaner_input = mock_components["cleaner"].clean_data.call_args[0][0]
        assert cleaner_input == grouper_output

    def test_parse_with_no_parameters(self, mock_components):
        """Test parse() with no parameters (defaults)."""
        # Arrange
        parser = RepoParser("/test/repo")

        # Act
        result = parser.parse()

        # Assert
        mock_components["extractor"].get_commits.assert_called_once_with(
            None, None, None
        )
        assert result is not None

    def test_parse_with_only_since(self, mock_components):
        """Test parse() with only since parameter."""
        # Arrange
        parser = RepoParser("/test/repo")

        # Act
        parser.parse(since="2025-01-01")

        # Assert
        mock_components["extractor"].get_commits.assert_called_once_with(
            "2025-01-01", None, None
        )

    def test_parse_with_only_branch(self, mock_components):
        """Test parse() with only branch parameter."""
        # Arrange
        parser = RepoParser("/test/repo")

        # Act
        parser.parse(branch="develop")

        # Assert
        mock_components["extractor"].get_commits.assert_called_once_with(
            None, None, "develop"
        )

    def test_parse_with_all_parameters(self, mock_components):
        """Test parse() with all parameters specified."""
        # Arrange
        parser = RepoParser("/test/repo")

        # Act
        parser.parse(since="2025-01-01", until="2025-01-31", branch="main")

        # Assert
        mock_components["extractor"].get_commits.assert_called_once_with(
            "2025-01-01", "2025-01-31", "main"
        )


class TestRepoParserErrorPropagation:
    """Test suite for error propagation through the pipeline."""

    @patch("gitstory.parser.GitExtractor")
    @patch("gitstory.parser.CommitGrouper")
    @patch("gitstory.parser.DataCleaner")
    def test_extractor_error_propagates(
        self, mock_cleaner_class, mock_grouper_class, mock_extractor_class
    ):
        """Test errors from GitExtractor propagate correctly."""
        # Arrange
        mock_extractor = Mock()
        mock_extractor.get_commits.side_effect = ValueError("Invalid time format")
        mock_extractor_class.return_value = mock_extractor

        parser = RepoParser("/test/repo")

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid time format"):
            parser.parse()

    @patch("gitstory.parser.GitExtractor")
    @patch("gitstory.parser.CommitGrouper")
    @patch("gitstory.parser.DataCleaner")
    def test_grouper_error_propagates(
        self, mock_cleaner_class, mock_grouper_class, mock_extractor_class
    ):
        """Test errors from CommitGrouper propagate correctly."""
        # Arrange
        mock_extractor = Mock()
        mock_extractor.get_commits.return_value = [
            {
                "hash": "abc123",
                "author": "Test Author",
                "message": "test commit",
                "timestamp": "2025-01-01T00:00:00",
            }
        ]
        mock_extractor_class.return_value = mock_extractor

        mock_grouper = Mock()
        mock_grouper.group_commits.side_effect = KeyError("Missing 'author' field")
        mock_grouper_class.return_value = mock_grouper

        parser = RepoParser("/test/repo")

        # Act & Assert
        with pytest.raises(KeyError, match="Missing 'author' field"):
            parser.parse()

    @patch("gitstory.parser.GitExtractor")
    @patch("gitstory.parser.CommitGrouper")
    @patch("gitstory.parser.DataCleaner")
    def test_cleaner_error_propagates(
        self, mock_cleaner_class, mock_grouper_class, mock_extractor_class
    ):
        """Test errors from DataCleaner propagate correctly."""
        # Arrange
        mock_extractor = Mock()
        mock_extractor.get_commits.return_value = [
            {
                "hash": "abc123",
                "author": "Test Author",
                "message": "test commit",
                "timestamp": "2025-01-01T00:00:00",
            }
        ]
        mock_extractor_class.return_value = mock_extractor

        mock_grouper = Mock()
        mock_grouper.group_commits.return_value = {
            "grouped_commits": {},
            "stats": {"by_author": {}, "by_type": {}, "total_commits": 0},
        }
        mock_grouper_class.return_value = mock_grouper

        mock_cleaner = Mock()
        mock_cleaner.clean_data.side_effect = TypeError("Invalid data type")
        mock_cleaner_class.return_value = mock_cleaner

        parser = RepoParser("/test/repo")

        # Act & Assert
        with pytest.raises(TypeError, match="Invalid data type"):
            parser.parse()

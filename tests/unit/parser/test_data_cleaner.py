"""
Comprehensive unit tests for DataCleaner.

This test suite implements:
- Boundary value analysis for all truncation/limiting logic
- Message length boundaries (199, 200, 201 chars)
- Commit count boundaries (49, 50, 51 commits)
- Diff chunk size boundaries (1999, 2000, 2001, 4000 chars)
- Data transformation validation
- Edge case testing

Test Count: 35+ tests
Coverage Target: 100% for this module
"""

import pytest
from gitstory.parser.data_cleaner import DataCleaner


class TestMessageTruncation:
    """Test suite for message truncation boundary conditions."""

    @pytest.fixture
    def cleaner(self):
        return DataCleaner()

    @pytest.fixture
    def sample_commit(self):
        """Sample commit with all required fields."""
        return {
            "hash": "abc123",
            "author": "Alice",
            "timestamp": "2025-01-10T10:00:00",
            "message": "test message",
            "files_changed": ["file1.py", "file2.py"],
            "insertions": 10,
            "deletions": 5,
            "diff": "sample diff",
        }

    def test_message_shorter_than_max(self, cleaner, sample_commit):
        """Test message < 200 chars remains unchanged."""
        # Arrange: 50 char message
        sample_commit["message"] = "a" * 50

        # Act
        result = cleaner._clean_commit(sample_commit, "feature")

        # Assert
        assert result["message"] == "a" * 50
        assert not result["message"].endswith("...")

    def test_message_boundary_199_chars(self, cleaner, sample_commit):
        """Boundary Test: Message == 199 chars remains unchanged."""
        # Arrange
        sample_commit["message"] = "a" * 199

        # Act
        result = cleaner._clean_commit(sample_commit, "feature")

        # Assert
        assert len(result["message"]) == 199
        assert result["message"] == "a" * 199
        assert not result["message"].endswith("...")

    def test_message_boundary_200_chars(self, cleaner, sample_commit):
        """Boundary Test: Message == 200 chars remains unchanged (at limit)."""
        # Arrange
        sample_commit["message"] = "a" * 200

        # Act
        result = cleaner._clean_commit(sample_commit, "feature")

        # Assert
        assert len(result["message"]) == 200
        assert result["message"] == "a" * 200
        assert not result["message"].endswith("...")

    def test_message_boundary_201_chars(self, cleaner, sample_commit):
        """Boundary Test: Message == 201 chars → truncated to 200 + '...'."""
        # Arrange
        sample_commit["message"] = "a" * 201

        # Act
        result = cleaner._clean_commit(sample_commit, "feature")

        # Assert
        assert result["message"] == ("a" * 200) + "..."
        assert len(result["message"]) == 203  # 200 + '...'

    def test_message_much_longer_than_max(self, cleaner, sample_commit):
        """Test message >> 200 chars → truncated to 200 + '...'."""
        # Arrange: 1000 char message
        sample_commit["message"] = "b" * 1000

        # Act
        result = cleaner._clean_commit(sample_commit, "feature")

        # Assert
        assert result["message"] == ("b" * 200) + "..."
        assert len(result["message"]) == 203

    def test_empty_message(self, cleaner, sample_commit):
        """Edge Case: Empty message remains empty."""
        # Arrange
        sample_commit["message"] = ""

        # Act
        result = cleaner._clean_commit(sample_commit, "feature")

        # Assert
        assert result["message"] == ""


class TestDiffChunking:
    """Test suite for diff chunking boundary conditions."""

    @pytest.fixture
    def cleaner(self):
        return DataCleaner()

    def test_empty_diff(self, cleaner):
        """Test empty diff → empty list."""
        assert cleaner._chunk_diff("") == []

    def test_diff_shorter_than_chunk_size(self, cleaner):
        """Test diff < 2000 chars → single chunk."""
        # Arrange: 500 char diff
        diff = "a" * 500

        # Act
        result = cleaner._chunk_diff(diff)

        # Assert
        assert len(result) == 1
        assert result[0] == diff

    def test_diff_boundary_1999_chars(self, cleaner):
        """Boundary Test: Diff == 1999 chars → single chunk."""
        # Arrange
        diff = "a" * 1999

        # Act
        result = cleaner._chunk_diff(diff)

        # Assert
        assert len(result) == 1
        assert result[0] == diff
        assert len(result[0]) == 1999

    def test_diff_boundary_2000_chars(self, cleaner):
        """Boundary Test: Diff == 2000 chars → single chunk (exactly at limit)."""
        # Arrange
        diff = "b" * 2000

        # Act
        result = cleaner._chunk_diff(diff)

        # Assert
        assert len(result) == 1
        assert result[0] == diff
        assert len(result[0]) == 2000

    def test_diff_boundary_2001_chars(self, cleaner):
        """Boundary Test: Diff == 2001 chars → 2 chunks (2000 + 1)."""
        # Arrange
        diff = "c" * 2001

        # Act
        result = cleaner._chunk_diff(diff)

        # Assert
        assert len(result) == 2
        assert result[0] == "c" * 2000
        assert result[1] == "c" * 1
        assert len(result[0]) == 2000
        assert len(result[1]) == 1

    def test_diff_boundary_4000_chars(self, cleaner):
        """Boundary Test: Diff == 4000 chars → 2 chunks (2000 + 2000)."""
        # Arrange
        diff = "d" * 4000

        # Act
        result = cleaner._chunk_diff(diff)

        # Assert
        assert len(result) == 2
        assert result[0] == "d" * 2000
        assert result[1] == "d" * 2000
        assert all(len(chunk) == 2000 for chunk in result)

    def test_diff_boundary_4001_chars(self, cleaner):
        """Boundary Test: Diff == 4001 chars → 3 chunks (2000 + 2000 + 1)."""
        # Arrange
        diff = "e" * 4001

        # Act
        result = cleaner._chunk_diff(diff)

        # Assert
        assert len(result) == 3
        assert result[0] == "e" * 2000
        assert result[1] == "e" * 2000
        assert result[2] == "e" * 1
        assert len(result[2]) == 1

    def test_very_large_diff(self, cleaner):
        """Test very large diff (10KB) → multiple chunks."""
        # Arrange: 10000 char diff
        diff = "f" * 10000

        # Act
        result = cleaner._chunk_diff(diff)

        # Assert
        assert len(result) == 5  # 10000 / 2000 = 5
        assert all(len(chunk) == 2000 for chunk in result)


class TestCommitLimiting:
    """Test suite for commit limiting per group."""

    @pytest.fixture
    def cleaner(self):
        return DataCleaner()

    def create_grouped_data(self, num_commits):
        """Helper to create grouped data with N commits."""
        commits = [
            {
                "hash": f"hash{i}",
                "author": f"Author{i}",
                "timestamp": "2025-01-10T10:00:00",
                "message": f"commit {i}",
                "files_changed": ["file.py"],
                "insertions": 5,
                "deletions": 3,
                "diff": "diff",
            }
            for i in range(num_commits)
        ]
        return {
            "grouped_commits": {"feature": commits},
            "stats": {
                "total_commits": num_commits,
                "by_type": {"feature": num_commits},
                "by_author": {},
            },
        }

    def test_commits_less_than_max(self, cleaner):
        """Test < 50 commits → all included."""
        # Arrange: 20 commits
        data = self.create_grouped_data(20)

        # Act
        result = cleaner.clean_data(data)

        # Assert
        assert len(result["commits"]) == 20

    def test_commits_boundary_49(self, cleaner):
        """Boundary Test: 49 commits → all included."""
        # Arrange
        data = self.create_grouped_data(49)

        # Act
        result = cleaner.clean_data(data)

        # Assert
        assert len(result["commits"]) == 49

    def test_commits_boundary_50(self, cleaner):
        """Boundary Test: 50 commits → all included (at limit)."""
        # Arrange
        data = self.create_grouped_data(50)

        # Act
        result = cleaner.clean_data(data)

        # Assert
        assert len(result["commits"]) == 50

    def test_commits_boundary_51(self, cleaner):
        """Boundary Test: 51 commits → first 50 only."""
        # Arrange
        data = self.create_grouped_data(51)

        # Act
        result = cleaner.clean_data(data)

        # Assert
        assert len(result["commits"]) == 50
        # Verify it's the first 50 (hash0 to hash49)
        assert result["commits"][0]["hash"] == "hash0"
        assert result["commits"][49]["hash"] == "hash49"

    def test_commits_much_more_than_max(self, cleaner):
        """Test >> 50 commits (e.g., 100) → first 50 only."""
        # Arrange
        data = self.create_grouped_data(100)

        # Act
        result = cleaner.clean_data(data)

        # Assert
        assert len(result["commits"]) == 50
        assert result["commits"][0]["hash"] == "hash0"
        assert result["commits"][49]["hash"] == "hash49"


class TestSummaryChunkCreation:
    """Test suite for summary chunk creation."""

    @pytest.fixture
    def cleaner(self):
        return DataCleaner()

    def create_commits_list(self, num_commits):
        """Helper to create list of N commits."""
        return [
            {
                "hash": f"hash{i}",
                "author": f"Author{i}",
                "message": f"commit message {i}" * 10,  # Make it longer
            }
            for i in range(num_commits)
        ]

    def test_summary_less_than_10_commits(self, cleaner):
        """Test < 10 commits → all shown, no '... and X more'."""
        # Arrange
        commits = self.create_commits_list(5)

        # Act
        result = cleaner._create_summary_chunk("feature", commits)

        # Assert
        assert "FEATURE COMMITS (5 total)" in result
        assert "... and" not in result
        # Verify all 5 are shown
        for i in range(5):
            assert f"hash{i}" in result

    def test_summary_boundary_9_commits(self, cleaner):
        """Boundary Test: 9 commits → all shown."""
        # Arrange
        commits = self.create_commits_list(9)

        # Act
        result = cleaner._create_summary_chunk("bugfix", commits)

        # Assert
        assert "BUGFIX COMMITS (9 total)" in result
        assert "... and" not in result
        assert result.count("[hash") == 9

    def test_summary_boundary_10_commits(self, cleaner):
        """Boundary Test: 10 commits → all shown, no '... and X more'."""
        # Arrange
        commits = self.create_commits_list(10)

        # Act
        result = cleaner._create_summary_chunk("refactor", commits)

        # Assert
        assert "REFACTOR COMMITS (10 total)" in result
        assert "... and" not in result
        assert result.count("[hash") == 10

    def test_summary_boundary_11_commits(self, cleaner):
        """Boundary Test: 11 commits → first 10 + '... and 1 more'."""
        # Arrange
        commits = self.create_commits_list(11)

        # Act
        result = cleaner._create_summary_chunk("docs", commits)

        # Assert
        assert "DOCS COMMITS (11 total)" in result
        assert "... and 1 more docs commits" in result
        assert result.count("[hash") == 10  # Only first 10 shown

    def test_summary_much_more_than_10_commits(self, cleaner):
        """Test >> 10 commits (e.g., 50) → first 10 + '... and 40 more'."""
        # Arrange
        commits = self.create_commits_list(50)

        # Act
        result = cleaner._create_summary_chunk("test", commits)

        # Assert
        assert "TEST COMMITS (50 total)" in result
        assert "... and 40 more test commits" in result
        assert result.count("[hash") == 10

    def test_summary_message_truncated_to_100_chars(self, cleaner):
        """Test commit messages in summary truncated to 100 chars."""
        # Arrange
        commits = [
            {
                "hash": "abc123",
                "author": "Alice",
                "message": "a" * 200,  # Long message
            }
        ]

        # Act
        result = cleaner._create_summary_chunk("feature", commits)

        # Assert
        # Message should be truncated to 100 chars in summary
        assert ("a" * 100) in result
        assert ("a" * 101) not in result


class TestDataTransformation:
    """Test suite for data transformation and preservation."""

    @pytest.fixture
    def cleaner(self):
        return DataCleaner()

    @pytest.fixture
    def sample_grouped_data(self):
        return {
            "grouped_commits": {
                "feature": [
                    {
                        "hash": "abc123",
                        "author": "Alice",
                        "timestamp": "2025-01-10T10:00:00",
                        "message": "feat: add feature",
                        "files_changed": ["file1.py", "file2.py", "file3.py"],
                        "insertions": 15,
                        "deletions": 7,
                        "diff": "sample diff content",
                    }
                ],
                "bugfix": [],  # Empty group
            },
            "stats": {
                "total_commits": 1,
                "by_type": {"feature": 1},
                "by_author": {"Alice": {"count": 1, "types": {"feature": 1}}},
            },
        }

    def test_preserves_hash(self, cleaner, sample_grouped_data):
        """Test hash is preserved."""
        result = cleaner.clean_data(sample_grouped_data)
        assert result["commits"][0]["hash"] == "abc123"

    def test_preserves_author(self, cleaner, sample_grouped_data):
        """Test author is preserved."""
        result = cleaner.clean_data(sample_grouped_data)
        assert result["commits"][0]["author"] == "Alice"

    def test_preserves_timestamp(self, cleaner, sample_grouped_data):
        """Test timestamp is preserved."""
        result = cleaner.clean_data(sample_grouped_data)
        assert result["commits"][0]["timestamp"] == "2025-01-10T10:00:00"

    def test_adds_commit_type(self, cleaner, sample_grouped_data):
        """Test commit type is added to cleaned data."""
        result = cleaner.clean_data(sample_grouped_data)
        assert result["commits"][0]["type"] == "feature"

    def test_calculates_files_changed_count(self, cleaner, sample_grouped_data):
        """Test files_changed is converted to count."""
        result = cleaner.clean_data(sample_grouped_data)
        assert result["commits"][0]["files_changed"] == 3  # Count, not list

    def test_calculates_total_changes(self, cleaner, sample_grouped_data):
        """Test changes = insertions + deletions."""
        result = cleaner.clean_data(sample_grouped_data)
        assert result["commits"][0]["changes"] == 22  # 15 + 7

    def test_creates_diff_chunks(self, cleaner, sample_grouped_data):
        """Test diff_chunks is created from diff."""
        result = cleaner.clean_data(sample_grouped_data)
        assert "diff_chunks" in result["commits"][0]
        assert result["commits"][0]["diff_chunks"] == ["sample diff content"]

    def test_handles_missing_diff(self, cleaner):
        """Test handles commits without diff field."""
        data = {
            "grouped_commits": {
                "feature": [
                    {
                        "hash": "abc",
                        "author": "Bob",
                        "timestamp": "2025-01-10T10:00:00",
                        "message": "test",
                        "files_changed": [],
                        "insertions": 0,
                        "deletions": 0,
                        # No 'diff' field
                    }
                ]
            },
            "stats": {"total_commits": 1, "by_type": {"feature": 1}, "by_author": {}},
        }

        result = cleaner.clean_data(data)
        assert result["commits"][0]["diff_chunks"] == []

    def test_skips_empty_commit_groups(self, cleaner, sample_grouped_data):
        """Test empty commit groups are skipped."""
        result = cleaner.clean_data(sample_grouped_data)

        # Only feature commits should be processed (bugfix is empty)
        assert len(result["commits"]) == 1
        # Summary should not include bugfix
        assert "BUGFIX" not in result["summary_text"]

    def test_preserves_stats(self, cleaner, sample_grouped_data):
        """Test stats are preserved in output."""
        result = cleaner.clean_data(sample_grouped_data)
        assert result["stats"] == sample_grouped_data["stats"]

    def test_creates_metadata(self, cleaner, sample_grouped_data):
        """Test metadata is created correctly."""
        result = cleaner.clean_data(sample_grouped_data)

        assert result["metadata"]["total_commits_analyzed"] == 1
        assert result["metadata"]["commit_types_present"] == ["feature"]

    def test_combines_summary_chunks(self, cleaner):
        """Test summary chunks are combined with double newlines."""
        data = {
            "grouped_commits": {
                "feature": [
                    {
                        "hash": "a",
                        "author": "Alice",
                        "timestamp": "2025-01-10T10:00:00",
                        "message": "feat",
                        "files_changed": [],
                        "insertions": 0,
                        "deletions": 0,
                    }
                ],
                "bugfix": [
                    {
                        "hash": "b",
                        "author": "Bob",
                        "timestamp": "2025-01-10T11:00:00",
                        "message": "fix",
                        "files_changed": [],
                        "insertions": 0,
                        "deletions": 0,
                    }
                ],
            },
            "stats": {
                "total_commits": 2,
                "by_type": {"feature": 1, "bugfix": 1},
                "by_author": {},
            },
        }

        result = cleaner.clean_data(data)

        # Summary should have both groups separated by \n\n
        assert "FEATURE COMMITS" in result["summary_text"]
        assert "BUGFIX COMMITS" in result["summary_text"]
        assert "\n\n" in result["summary_text"]


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    @pytest.fixture
    def cleaner(self):
        return DataCleaner()

    def test_clean_data_with_all_empty_groups(self, cleaner):
        """Test clean_data with all commit groups empty."""
        data = {
            "grouped_commits": {"feature": [], "bugfix": [], "refactor": []},
            "stats": {"total_commits": 0, "by_type": {}, "by_author": {}},
        }

        result = cleaner.clean_data(data)

        assert result["commits"] == []
        assert result["summary_text"] == ""
        assert result["metadata"]["total_commits_analyzed"] == 0
        assert result["metadata"]["commit_types_present"] == []

    def test_commit_with_zero_changes(self, cleaner):
        """Test commit with 0 insertions and 0 deletions."""
        commit = {
            "hash": "abc",
            "author": "Alice",
            "timestamp": "2025-01-10T10:00:00",
            "message": "empty commit",
            "files_changed": [],
            "insertions": 0,
            "deletions": 0,
            "diff": "",
        }

        result = cleaner._clean_commit(commit, "chore")

        assert result["changes"] == 0
        assert result["files_changed"] == 0
        assert result["diff_chunks"] == []

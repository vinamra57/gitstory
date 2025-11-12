"""
Comprehensive unit tests for CommitGrouper.

This test suite implements:
- Pattern matching tests for all 7 commit types
- Edge case testing (empty, special characters, unicode)
- Aggregation and statistics validation
- Boundary value analysis

Test Count: 30+ tests
Coverage Target: 100% for this simple module
"""

import pytest
from gitstory.parser.commit_grouper import CommitGrouper


class TestCommitClassification:
    """Test suite for _classify_commit() pattern matching."""

    @pytest.fixture
    def grouper(self):
        """Create CommitGrouper instance for testing."""
        return CommitGrouper()

    # Feature classification tests
    def test_classify_conventional_feat(self, grouper):
        """Test 'feat:' conventional commit format → feature."""
        assert grouper._classify_commit("feat: add new feature") == "feature"

    def test_classify_conventional_feat_with_scope(self, grouper):
        """Test 'feat(scope):' format → feature."""
        assert grouper._classify_commit("feat(auth): add login") == "feature"

    def test_classify_add_prefix(self, grouper):
        """Test 'add' prefix → feature."""
        assert grouper._classify_commit("add user authentication") == "feature"

    def test_classify_implement_keyword(self, grouper):
        """Test 'implement' keyword → feature."""
        assert grouper._classify_commit("implement new API endpoint") == "feature"

    def test_classify_new_feature_phrase(self, grouper):
        """Test 'new feature' phrase → feature."""
        assert grouper._classify_commit("new feature for dashboard") == "feature"

    def test_classify_feature_colon(self, grouper):
        """Test 'feature:' prefix → feature."""
        assert grouper._classify_commit("feature: user profile page") == "feature"

    # Bugfix classification tests
    def test_classify_conventional_fix(self, grouper):
        """Test 'fix:' conventional commit format → bugfix."""
        assert grouper._classify_commit("fix: resolve login bug") == "bugfix"

    def test_classify_conventional_fix_with_scope(self, grouper):
        """Test 'fix(scope):' format → bugfix."""
        assert grouper._classify_commit("fix(api): null pointer") == "bugfix"

    def test_classify_bug_keyword(self, grouper):
        """Test 'bug' keyword → bugfix."""
        assert grouper._classify_commit("bug in payment processing") == "bugfix"

    def test_classify_hotfix_keyword(self, grouper):
        """Test 'hotfix' keyword → bugfix."""
        assert grouper._classify_commit("hotfix for production error") == "bugfix"

    def test_classify_patch_keyword(self, grouper):
        """Test 'patch' keyword → bugfix."""
        assert grouper._classify_commit("patch security vulnerability") == "bugfix"

    def test_classify_resolve_issue_phrase(self, grouper):
        """Test 'resolve issue' phrase → bugfix."""
        assert grouper._classify_commit("resolve issue with database") == "bugfix"

    # Refactor classification tests
    def test_classify_conventional_refactor(self, grouper):
        """Test 'refactor:' conventional commit format → refactor."""
        assert grouper._classify_commit("refactor: clean up code") == "refactor"

    def test_classify_refactor_keyword(self, grouper):
        """Test 'refactor' keyword → refactor."""
        assert grouper._classify_commit("refactor authentication module") == "refactor"

    def test_classify_restructure_keyword(self, grouper):
        """Test 'restructure' keyword → refactor."""
        assert grouper._classify_commit("restructure project layout") == "refactor"

    def test_classify_reorganize_keyword(self, grouper):
        """Test 'reorganize' keyword → refactor."""
        assert grouper._classify_commit("reorganize components") == "refactor"

    # Docs classification tests
    def test_classify_conventional_docs(self, grouper):
        """Test 'docs:' conventional commit format → docs."""
        assert grouper._classify_commit("docs: update README") == "docs"

    def test_classify_doc_singular(self, grouper):
        """Test 'doc:' singular format → docs."""
        assert grouper._classify_commit("doc: add API documentation") == "docs"

    def test_classify_documentation_keyword(self, grouper):
        """Test 'documentation' keyword → docs."""
        assert grouper._classify_commit("update documentation") == "docs"

    def test_classify_readme_keyword(self, grouper):
        """Test 'readme' keyword → docs."""
        assert grouper._classify_commit("update readme file") == "docs"

    def test_classify_comment_keyword(self, grouper):
        """Test 'comment' keyword → docs."""
        # Note: "add comments" matches 'feature' first due to 'add' pattern
        # Using "update comments" to specifically match docs
        assert grouper._classify_commit("update comments in code") == "docs"

    # Style classification tests
    def test_classify_conventional_style(self, grouper):
        """Test 'style:' conventional commit format → style."""
        assert grouper._classify_commit("style: format code") == "style"

    def test_classify_formatting_keyword(self, grouper):
        """Test 'formatting' keyword → style."""
        assert grouper._classify_commit("code formatting improvements") == "style"

    def test_classify_whitespace_keyword(self, grouper):
        """Test 'whitespace' keyword → style."""
        assert grouper._classify_commit("fix whitespace issues") == "style"

    def test_classify_lint_keyword(self, grouper):
        """Test 'lint' keyword → style."""
        assert grouper._classify_commit("fix lint errors") == "style"

    # Test classification tests
    def test_classify_conventional_test(self, grouper):
        """Test 'test:' conventional commit format → test."""
        assert grouper._classify_commit("test: add unit tests") == "test"

    def test_classify_add_test_phrase(self, grouper):
        """Test 'add test' phrase → feature (due to 'add' matching first)."""
        # "add test" matches 'feature' first because 'add' pattern is checked before 'add test'
        assert grouper._classify_commit("add test for login") == "feature"

    def test_classify_test_coverage_phrase(self, grouper):
        """Test 'test coverage' phrase → test."""
        assert grouper._classify_commit("improve test coverage") == "test"

    # Chore classification tests
    def test_classify_conventional_chore(self, grouper):
        """Test 'chore:' conventional commit format → chore."""
        assert grouper._classify_commit("chore: update dependencies") == "chore"

    def test_classify_dependency_keyword(self, grouper):
        """Test 'dependency' keyword → chore."""
        assert grouper._classify_commit("update dependency versions") == "chore"

    def test_classify_dependencies_keyword(self, grouper):
        """Test 'dependencies' keyword → chore."""
        assert grouper._classify_commit("upgrade dependencies") == "chore"

    def test_classify_package_keyword(self, grouper):
        """Test 'package' keyword → chore."""
        assert grouper._classify_commit("update package.json") == "chore"

    def test_classify_build_keyword(self, grouper):
        """Test 'build' keyword → chore."""
        assert grouper._classify_commit("fix build configuration") == "chore"

    # Other/fallback classification tests
    def test_classify_unmatched_message(self, grouper):
        """Test unmatched message → other."""
        assert grouper._classify_commit("random commit message") == "other"

    def test_classify_empty_message(self, grouper):
        """Test empty message → other."""
        assert grouper._classify_commit("") == "other"

    def test_classify_special_characters(self, grouper):
        """Test message with special characters → other."""
        assert grouper._classify_commit("!@#$%^&*()") == "other"

    def test_classify_numeric_message(self, grouper):
        """Test numeric-only message → other."""
        assert grouper._classify_commit("12345") == "other"


class TestPatternMatchingEdgeCases:
    """Test suite for pattern matching edge cases."""

    @pytest.fixture
    def grouper(self):
        return CommitGrouper()

    def test_case_insensitivity_uppercase(self, grouper):
        """Test pattern matching is case-insensitive (uppercase)."""
        assert grouper._classify_commit("FEAT: NEW FEATURE") == "feature"
        assert grouper._classify_commit("FIX: BUG") == "bugfix"

    def test_case_insensitivity_mixed(self, grouper):
        """Test pattern matching is case-insensitive (mixed case)."""
        assert grouper._classify_commit("FeAt: New Feature") == "feature"
        assert grouper._classify_commit("FiX: Bug Fix") == "bugfix"

    def test_first_match_wins(self, grouper):
        """Test first matching pattern wins (not greedy)."""
        # "add test" could match both 'feature' (add) and 'test' (add test)
        # 'feature' should win as it's checked first in PATTERNS
        result = grouper._classify_commit("add test for login")
        # This should match 'feature' due to 'add' pattern being checked first
        assert result == "feature"

    def test_multiline_message(self, grouper):
        """Test multiline commit message (uses first line)."""
        message = "feat: add new feature\n\nThis is a detailed description\nwith multiple lines"
        assert grouper._classify_commit(message) == "feature"

    def test_message_with_newlines(self, grouper):
        """Test message with embedded newlines."""
        assert grouper._classify_commit("fix:\nresolve bug") == "bugfix"

    def test_unicode_characters(self, grouper):
        """Test message with unicode characters."""
        assert grouper._classify_commit("feat: add café feature ☕") == "feature"

    def test_emoji_in_message(self, grouper):
        """Test message with emojis."""
        # Emojis before pattern prevent '^' anchor from matching
        # These should be classified as 'other' due to regex anchors
        assert grouper._classify_commit("✨ feat: add sparkles") == "other"
        # Emojis after pattern should work
        assert grouper._classify_commit("feat: add sparkles ✨") == "feature"

    def test_very_long_message(self, grouper):
        """Test very long commit message."""
        long_message = "feat: " + "a" * 10000
        assert grouper._classify_commit(long_message) == "feature"

    def test_whitespace_only_message(self, grouper):
        """Test whitespace-only message → other."""
        assert grouper._classify_commit("   \t\n   ") == "other"

    def test_message_with_leading_whitespace(self, grouper):
        """Test message with leading whitespace doesn't match '^' anchored patterns."""
        # Leading whitespace prevents '^' anchor from matching
        assert grouper._classify_commit("  feat: feature") == "other"
        # Non-anchored patterns still work (e.g., "new feature")
        assert grouper._classify_commit("  new feature here") == "feature"


class TestGroupCommitsAggregation:
    """Test suite for group_commits() aggregation logic."""

    @pytest.fixture
    def grouper(self):
        return CommitGrouper()

    def test_group_commits_empty_list(self, grouper):
        """Test group_commits() with empty list returns empty groups."""
        result = grouper.group_commits([])

        assert result["stats"]["total_commits"] == 0
        assert result["stats"]["by_type"] == {}
        assert result["stats"]["by_author"] == {}
        assert all(len(v) == 0 for v in result["grouped_commits"].values())

    def test_group_commits_single_commit(self, grouper):
        """Test group_commits() with single commit."""
        commits = [
            {"hash": "abc123", "author": "Alice", "message": "feat: new feature"}
        ]

        result = grouper.group_commits(commits)

        assert result["stats"]["total_commits"] == 1
        assert result["stats"]["by_type"]["feature"] == 1
        assert result["stats"]["by_author"]["Alice"]["count"] == 1
        assert result["stats"]["by_author"]["Alice"]["types"]["feature"] == 1
        assert len(result["grouped_commits"]["feature"]) == 1

    def test_group_commits_multiple_same_type(self, grouper):
        """Test group_commits() with multiple commits of same type."""
        commits = [
            {"hash": "abc123", "author": "Alice", "message": "feat: feature 1"},
            {"hash": "def456", "author": "Bob", "message": "feat: feature 2"},
            {"hash": "ghi789", "author": "Alice", "message": "feat: feature 3"},
        ]

        result = grouper.group_commits(commits)

        assert result["stats"]["total_commits"] == 3
        assert result["stats"]["by_type"]["feature"] == 3
        assert len(result["grouped_commits"]["feature"]) == 3
        assert result["stats"]["by_author"]["Alice"]["count"] == 2
        assert result["stats"]["by_author"]["Bob"]["count"] == 1

    def test_group_commits_multiple_different_types(self, grouper):
        """Test group_commits() with multiple different commit types."""
        commits = [
            {"hash": "abc123", "author": "Alice", "message": "feat: feature"},
            {"hash": "def456", "author": "Bob", "message": "fix: bug"},
            {"hash": "ghi789", "author": "Charlie", "message": "docs: update"},
            {"hash": "jkl012", "author": "Alice", "message": "test: add test"},
        ]

        result = grouper.group_commits(commits)

        assert result["stats"]["total_commits"] == 4
        assert result["stats"]["by_type"]["feature"] == 1
        assert result["stats"]["by_type"]["bugfix"] == 1
        assert result["stats"]["by_type"]["docs"] == 1
        assert result["stats"]["by_type"]["test"] == 1
        assert len(result["grouped_commits"]["feature"]) == 1
        assert len(result["grouped_commits"]["bugfix"]) == 1

    def test_group_commits_all_commit_types(self, grouper):
        """Test group_commits() with all 8 commit types."""
        commits = [
            {"hash": "1", "author": "Alice", "message": "feat: feature"},
            {"hash": "2", "author": "Alice", "message": "fix: bug"},
            {"hash": "3", "author": "Alice", "message": "refactor: code"},
            {"hash": "4", "author": "Alice", "message": "docs: readme"},
            {"hash": "5", "author": "Alice", "message": "style: format"},
            {"hash": "6", "author": "Alice", "message": "test: add test"},
            {"hash": "7", "author": "Alice", "message": "chore: deps"},
            {"hash": "8", "author": "Alice", "message": "random message"},
        ]

        result = grouper.group_commits(commits)

        assert result["stats"]["total_commits"] == 8
        assert result["stats"]["by_type"]["feature"] == 1
        assert result["stats"]["by_type"]["bugfix"] == 1
        assert result["stats"]["by_type"]["refactor"] == 1
        assert result["stats"]["by_type"]["docs"] == 1
        assert result["stats"]["by_type"]["style"] == 1
        assert result["stats"]["by_type"]["test"] == 1
        assert result["stats"]["by_type"]["chore"] == 1
        assert result["stats"]["by_type"]["other"] == 1

    def test_group_commits_author_statistics(self, grouper):
        """Test group_commits() author statistics accuracy."""
        commits = [
            {"hash": "1", "author": "Alice", "message": "feat: feature 1"},
            {"hash": "2", "author": "Alice", "message": "feat: feature 2"},
            {"hash": "3", "author": "Alice", "message": "fix: bug"},
            {"hash": "4", "author": "Bob", "message": "docs: readme"},
            {"hash": "5", "author": "Bob", "message": "fix: bug 2"},
        ]

        result = grouper.group_commits(commits)

        # Alice: 3 commits (2 feature, 1 bugfix)
        assert result["stats"]["by_author"]["Alice"]["count"] == 3
        assert result["stats"]["by_author"]["Alice"]["types"]["feature"] == 2
        assert result["stats"]["by_author"]["Alice"]["types"]["bugfix"] == 1

        # Bob: 2 commits (1 docs, 1 bugfix)
        assert result["stats"]["by_author"]["Bob"]["count"] == 2
        assert result["stats"]["by_author"]["Bob"]["types"]["docs"] == 1
        assert result["stats"]["by_author"]["Bob"]["types"]["bugfix"] == 1

    def test_group_commits_preserves_commit_data(self, grouper):
        """Test group_commits() preserves original commit data."""
        commits = [
            {
                "hash": "abc123",
                "author": "Alice",
                "email": "alice@example.com",
                "message": "feat: new feature",
                "timestamp": "2025-01-10T10:00:00",
                "files": ["file1.py", "file2.py"],
            }
        ]

        result = grouper.group_commits(commits)

        grouped_commit = result["grouped_commits"]["feature"][0]
        assert grouped_commit["hash"] == "abc123"
        assert grouped_commit["author"] == "Alice"
        assert grouped_commit["email"] == "alice@example.com"
        assert grouped_commit["timestamp"] == "2025-01-10T10:00:00"
        assert grouped_commit["files"] == ["file1.py", "file2.py"]

    def test_group_commits_only_returns_nonempty_types(self, grouper):
        """Test by_type stats only includes types with commits."""
        commits = [
            {"hash": "1", "author": "Alice", "message": "feat: feature"},
            {"hash": "2", "author": "Alice", "message": "fix: bug"},
        ]

        result = grouper.group_commits(commits)

        # Only feature and bugfix should be in by_type
        assert "feature" in result["stats"]["by_type"]
        assert "bugfix" in result["stats"]["by_type"]
        assert "refactor" not in result["stats"]["by_type"]
        assert "docs" not in result["stats"]["by_type"]
        assert "style" not in result["stats"]["by_type"]
        assert "test" not in result["stats"]["by_type"]
        assert "chore" not in result["stats"]["by_type"]
        assert "other" not in result["stats"]["by_type"]

    def test_group_commits_multiple_authors_same_type(self, grouper):
        """Test multiple authors contributing to same commit type."""
        commits = [
            {"hash": "1", "author": "Alice", "message": "feat: feature 1"},
            {"hash": "2", "author": "Bob", "message": "feat: feature 2"},
            {"hash": "3", "author": "Charlie", "message": "feat: feature 3"},
        ]

        result = grouper.group_commits(commits)

        assert result["stats"]["total_commits"] == 3
        assert result["stats"]["by_type"]["feature"] == 3
        assert len(result["stats"]["by_author"]) == 3
        assert all(
            author_stats["types"]["feature"] == 1
            for author_stats in result["stats"]["by_author"].values()
        )


class TestBoundaryAndEdgeCases:
    """Test suite for boundary values and edge cases."""

    @pytest.fixture
    def grouper(self):
        return CommitGrouper()

    def test_commit_with_only_hash(self, grouper):
        """Test commit with minimal data (only required fields)."""
        commits = [{"author": "Alice", "message": "feat: test"}]
        result = grouper.group_commits(commits)

        assert result["stats"]["total_commits"] == 1
        assert result["stats"]["by_type"]["feature"] == 1

    def test_commit_message_with_null_bytes(self, grouper):
        """Test commit message with null bytes."""
        commits = [{"author": "Alice", "message": "feat: test\x00message"}]
        result = grouper.group_commits(commits)

        # Should still classify correctly
        assert result["stats"]["by_type"]["feature"] == 1

    def test_author_name_with_special_characters(self, grouper):
        """Test author name with special characters."""
        commits = [
            {"author": "Alice O'Brien", "message": "feat: test"},
            {"author": 'Bob "The Builder"', "message": "fix: bug"},
        ]
        result = grouper.group_commits(commits)

        assert "Alice O'Brien" in result["stats"]["by_author"]
        assert 'Bob "The Builder"' in result["stats"]["by_author"]

    def test_very_large_commit_list(self, grouper):
        """Test grouping very large number of commits (performance)."""
        commits = [
            {"author": f"Author{i % 10}", "message": "feat: feature"}
            for i in range(1000)
        ]

        result = grouper.group_commits(commits)

        assert result["stats"]["total_commits"] == 1000
        assert result["stats"]["by_type"]["feature"] == 1000
        assert len(result["stats"]["by_author"]) == 10

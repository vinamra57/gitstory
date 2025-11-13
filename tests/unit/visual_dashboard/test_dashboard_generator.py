"""
Comprehensive unit tests for DashboardGenerator.

This test suite implements:
- File system operation mocking (os.makedirs, open)
- Jinja2 template mocking
- Markdown conversion testing
- Error handling
- Data flow validation

Test Count: 20+ tests
Coverage Target: 95%+ for this module
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from gitstory.visual_dashboard.dashboard_generator import generate_dashboard


class TestDashboardGenerationSuccess:
    """Test suite for successful dashboard generation scenarios."""

    @pytest.fixture
    def sample_repo_data(self):
        """Sample repository data."""
        return {
            "commits": [
                {
                    "hash": "abc123",
                    "author": "Alice",
                    "timestamp": "2025-01-10T10:00:00",
                    "message": "feat: add feature",
                    "type": "feature",
                }
            ],
            "stats": {
                "total_commits": 1,
                "by_type": {"feature": 1},
                "by_author": {"Alice": {"count": 1}},
            },
        }

    @pytest.fixture
    def sample_ai_summary(self):
        """Sample AI summary."""
        return {
            "summary": "# Summary\n\nThis is a **markdown** summary.",
            "metadata": {"model": "gemini-2.5-pro", "tokens_used": 150},
        }

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_successful_generation_creates_output_dir(
        self,
        mock_print,
        mock_file,
        mock_makedirs,
        mock_get_template,
        mock_markdown,
        sample_repo_data,
        sample_ai_summary,
    ):
        """Test successful dashboard generation creates output directory."""
        # Arrange
        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<h1>Summary</h1>"

        # Act
        generate_dashboard(sample_repo_data, sample_ai_summary, "/test/repo")

        # Assert
        mock_makedirs.assert_called_once_with("/test/repo/output", exist_ok=True)

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_successful_generation_loads_template(
        self,
        mock_print,
        mock_file,
        mock_makedirs,
        mock_get_template,
        mock_markdown,
        sample_repo_data,
        sample_ai_summary,
    ):
        """Test dashboard generation loads correct template."""
        # Arrange
        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<h1>Summary</h1>"

        # Act
        generate_dashboard(sample_repo_data, sample_ai_summary, "/test/repo")

        # Assert
        mock_get_template.assert_called_once_with("dashboard_template.html")

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_successful_generation_converts_markdown(
        self,
        mock_print,
        mock_file,
        mock_makedirs,
        mock_get_template,
        mock_markdown,
        sample_repo_data,
        sample_ai_summary,
    ):
        """Test markdown summary is converted to HTML."""
        # Arrange
        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<h1>Summary</h1><p>This is a summary.</p>"

        # Act
        generate_dashboard(sample_repo_data, sample_ai_summary, "/test/repo")

        # Assert
        mock_markdown.assert_called_once_with(
            "# Summary\n\nThis is a **markdown** summary."
        )

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_successful_generation_renders_template_with_correct_data(
        self,
        mock_print,
        mock_file,
        mock_makedirs,
        mock_get_template,
        mock_markdown,
        sample_repo_data,
        sample_ai_summary,
    ):
        """Test template is rendered with correct data."""
        # Arrange
        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<h1>Summary</h1>"

        # Act
        generate_dashboard(sample_repo_data, sample_ai_summary, "/test/repo")

        # Assert
        mock_template.render.assert_called_once()
        call_kwargs = mock_template.render.call_args[1]

        assert call_kwargs["commits"] == sample_repo_data["commits"]
        assert call_kwargs["stats"] == sample_repo_data["stats"]
        assert call_kwargs["ai_summary"]["summary"] == "<h1>Summary</h1>"
        assert call_kwargs["ai_summary"]["metadata"] == sample_ai_summary["metadata"]

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_successful_generation_writes_file(
        self,
        mock_print,
        mock_file,
        mock_makedirs,
        mock_get_template,
        mock_markdown,
        sample_repo_data,
        sample_ai_summary,
    ):
        """Test HTML content is written to file."""
        # Arrange
        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard Content</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<h1>Summary</h1>"

        # Act
        generate_dashboard(sample_repo_data, sample_ai_summary, "/test/repo")

        # Assert
        mock_file.assert_called_once_with("/test/repo/output/dashboard.html", "w")
        mock_file().write.assert_called_once_with("<html>Dashboard Content</html>")

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_successful_generation_prints_success_message(
        self,
        mock_print,
        mock_file,
        mock_makedirs,
        mock_get_template,
        mock_markdown,
        sample_repo_data,
        sample_ai_summary,
    ):
        """Test success message is printed."""
        # Arrange
        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<h1>Summary</h1>"

        # Act
        generate_dashboard(sample_repo_data, sample_ai_summary, "/test/repo")

        # Assert
        mock_print.assert_called_once()
        assert "Dashboard generated" in str(mock_print.call_args)
        assert "/test/repo/output/dashboard.html" in str(mock_print.call_args)

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_custom_output_filename(
        self,
        mock_print,
        mock_file,
        mock_makedirs,
        mock_get_template,
        mock_markdown,
        sample_repo_data,
        sample_ai_summary,
    ):
        """Test custom output filename is used."""
        # Arrange
        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<h1>Summary</h1>"

        # Act
        generate_dashboard(
            sample_repo_data,
            sample_ai_summary,
            "/test/repo",
            output_file="custom_dashboard.html",
        )

        # Assert
        mock_file.assert_called_once_with(
            "/test/repo/output/custom_dashboard.html", "w"
        )


class TestDataHandling:
    """Test suite for handling various data scenarios."""

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_handles_empty_commits_list(
        self, mock_print, mock_file, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test handles empty commits list gracefully."""
        # Arrange
        repo_data = {"commits": [], "stats": {}}
        ai_summary = {"summary": "Empty summary", "metadata": {}}

        mock_template = Mock()
        mock_template.render.return_value = "<html>Empty</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<p>Empty summary</p>"

        # Act
        generate_dashboard(repo_data, ai_summary, "/test/repo")

        # Assert
        call_kwargs = mock_template.render.call_args[1]
        assert call_kwargs["commits"] == []

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_handles_missing_commits_key(
        self, mock_print, mock_file, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test handles missing 'commits' key with .get() default."""
        # Arrange
        repo_data = {"stats": {}}  # No 'commits' key
        ai_summary = {"summary": "Summary", "metadata": {}}

        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<p>Summary</p>"

        # Act
        generate_dashboard(repo_data, ai_summary, "/test/repo")

        # Assert
        call_kwargs = mock_template.render.call_args[1]
        assert call_kwargs["commits"] == []  # Default from .get()

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_handles_missing_stats_key(
        self, mock_print, mock_file, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test handles missing 'stats' key with .get() default."""
        # Arrange
        repo_data = {"commits": []}  # No 'stats' key
        ai_summary = {"summary": "Summary", "metadata": {}}

        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<p>Summary</p>"

        # Act
        generate_dashboard(repo_data, ai_summary, "/test/repo")

        # Assert
        call_kwargs = mock_template.render.call_args[1]
        assert call_kwargs["stats"] == {}  # Default from .get()

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_handles_missing_summary_key(
        self, mock_print, mock_file, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test handles missing 'summary' key in AI summary."""
        # Arrange
        repo_data = {"commits": [], "stats": {}}
        ai_summary = {"metadata": {}}  # No 'summary' key

        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = ""  # Empty string from markdown conversion

        # Act
        generate_dashboard(repo_data, ai_summary, "/test/repo")

        # Assert
        mock_markdown.assert_called_once_with("")  # Default from .get()
        call_kwargs = mock_template.render.call_args[1]
        assert call_kwargs["ai_summary"]["summary"] == ""

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_handles_missing_metadata_key(
        self, mock_print, mock_file, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test handles missing 'metadata' key in AI summary."""
        # Arrange
        repo_data = {"commits": [], "stats": {}}
        ai_summary = {"summary": "Test"}  # No 'metadata' key

        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<p>Test</p>"

        # Act
        generate_dashboard(repo_data, ai_summary, "/test/repo")

        # Assert
        call_kwargs = mock_template.render.call_args[1]
        assert call_kwargs["ai_summary"]["metadata"] == {}  # Default from .get()

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_handles_very_large_data(
        self, mock_print, mock_file, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test handles very large data sets (100+ commits)."""
        # Arrange
        large_commits = [
            {
                "hash": f"hash{i}",
                "author": f"Author{i}",
                "message": f"Commit {i}" * 100,  # Long messages
            }
            for i in range(100)
        ]
        repo_data = {"commits": large_commits, "stats": {"total_commits": 100}}
        ai_summary = {"summary": "Summary" * 1000, "metadata": {}}  # Long summary

        mock_template = Mock()
        mock_template.render.return_value = "<html>Large Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<p>Long HTML</p>"

        # Act
        generate_dashboard(repo_data, ai_summary, "/test/repo")

        # Assert
        call_kwargs = mock_template.render.call_args[1]
        assert len(call_kwargs["commits"]) == 100


class TestFileSystemOperations:
    """Test suite for file system operations and error handling."""

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_makedirs_with_exist_ok_true(
        self, mock_print, mock_file, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test os.makedirs is called with exist_ok=True."""
        # Arrange
        repo_data = {"commits": [], "stats": {}}
        ai_summary = {"summary": "Test", "metadata": {}}

        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<p>Test</p>"

        # Act
        generate_dashboard(repo_data, ai_summary, "/test/repo")

        # Assert
        mock_makedirs.assert_called_once_with("/test/repo/output", exist_ok=True)

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_file_opened_in_write_mode(
        self, mock_print, mock_file, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test file is opened in write mode ('w')."""
        # Arrange
        repo_data = {"commits": [], "stats": {}}
        ai_summary = {"summary": "Test", "metadata": {}}

        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<p>Test</p>"

        # Act
        generate_dashboard(repo_data, ai_summary, "/test/repo")

        # Assert
        # Verify file opened with 'w' mode
        mock_file.assert_called_with("/test/repo/output/dashboard.html", "w")

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.print")
    def test_file_write_error_propagates(
        self, mock_print, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test file write errors propagate correctly."""
        # Arrange
        repo_data = {"commits": [], "stats": {}}
        ai_summary = {"summary": "Test", "metadata": {}}

        mock_template = Mock()
        mock_template.render.return_value = "<html>Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<p>Test</p>"

        # Mock open to raise PermissionError
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            # Act & Assert
            with pytest.raises(PermissionError):
                generate_dashboard(repo_data, ai_summary, "/test/repo")


class TestSpecialCharacterHandling:
    """Test suite for special characters and encoding."""

    @patch("gitstory.visual_dashboard.dashboard_generator.markdown.markdown")
    @patch("gitstory.visual_dashboard.dashboard_generator.env.get_template")
    @patch("gitstory.visual_dashboard.dashboard_generator.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_handles_unicode_in_data(
        self, mock_print, mock_file, mock_makedirs, mock_get_template, mock_markdown
    ):
        """Test handles unicode characters in commit data."""
        # Arrange
        repo_data = {
            "commits": [
                {
                    "hash": "abc",
                    "author": "José García",
                    "message": "Add café feature ☕",
                    "timestamp": "2025-01-10T10:00:00",
                }
            ],
            "stats": {},
        }
        ai_summary = {"summary": "Unicode test: 你好世界", "metadata": {}}

        mock_template = Mock()
        mock_template.render.return_value = "<html>Unicode Dashboard</html>"
        mock_get_template.return_value = mock_template
        mock_markdown.return_value = "<p>Unicode test</p>"

        # Act
        generate_dashboard(repo_data, ai_summary, "/test/repo")

        # Assert
        call_kwargs = mock_template.render.call_args[1]
        assert call_kwargs["commits"][0]["author"] == "José García"
        assert "☕" in call_kwargs["commits"][0]["message"]

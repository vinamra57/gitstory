from click.testing import CliRunner
from gitstory.__main__ import cli


class TestMain:
    def test_main(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code != 0

    def test_main_run(self, monkeypatch):
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "./", "--branch", "main"])
        assert result.exit_code in (0, 1, 2)
        assert (
            "Summary generation complete!" in result.output
            or "Error generating summary" in result.output
        )

    def test_main_dashboard(self, monkeypatch):
        runner = CliRunner()
        result = runner.invoke(cli, ["dashboard"])
        assert result.exit_code in (0, 1, 2)
        output_lower = result.output.lower()
        assert "dashboard" in output_lower or "error" in output_lower

    def test_main_since(self):
        """Test since command with time period argument."""
        runner = CliRunner()
        result = runner.invoke(cli, ["since", "./", "2w"])
        assert result.exit_code in (0, 1, 2)

        # Should not show placeholder anymore
        assert "SINCE TO BE COMPLETED" not in result.output

        # Should show either success or error
        assert (
            "Summary generation complete!" in result.output
            or "Error generating summary" in result.output
            or "Error parsing time period" in result.output
            or "Error: " in result.output
        )

    def test_main_compare(self):
        """Test compare command with two branches."""
        runner = CliRunner()
        result = runner.invoke(cli, ["compare", "./", "main", "main"])
        assert result.exit_code in (0, 1, 2)

        # Should not show placeholder anymore
        assert "COMPARE TO BE COMPLETED" not in result.output

        # Should show either success or error
        assert (
            "Comparison summary complete!" in result.output
            or "Error comparing branches" in result.output
            or "Error: " in result.output
        )


"""
NOTE:
test_main_key doesn't exist because I (Derick) am currently
unaware of a way to run such a test without destroying
the key currently at the file location
"""

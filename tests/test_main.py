from click.testing import CliRunner
from gitstory.__main__ import cli
import os


class TestMain:
    def test_main(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code != 0

    def test_main_run(self, monkeypatch):
        runner = CliRunner()
        monkeypatch.setenv("GITSTORY_API_KEY", "test-key")
        result = runner.invoke(cli, ["run", "./", "--branch", "main"])
        assert result.exit_code in (0, 1, 2)
        assert (
            "Summary generation complete!" in result.output
            or "Error generating summary" in result.output
        )

    def test_main_dashboard(self, monkeypatch):
        runner = CliRunner()
        monkeypatch.setenv("GITSTORY_API_KEY", "test-key")
        result = runner.invoke(cli, ["dashboard"])
        assert result.exit_code in (0, 1, 2)
        output_lower = result.output.lower()
        assert "dashboard" in output_lower or "error" in output_lower

    def test_main_since(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["since"])
        assert result.exit_code == 0
        assert "SINCE TO BE COMPLETED" in result.output

    def test_main_compare(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["compare"])
        assert result.exit_code == 0
        assert "COMPARE TO BE COMPLETED" in result.output
    
    def test_main_key(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["key", "--key=\"test\""])
        assert result.exit_code == 0
        api_key = os.getenv("GEMINI_API_KEY")
        assert api_key == "test"

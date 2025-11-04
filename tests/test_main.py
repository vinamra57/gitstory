from click.testing import CliRunner
from main import cli

# Tests the main features of GitStory: run, dashboard, since, and compare
# Further specific tests for each component are located in their respective folders
# within the tests folder


class TestMain:
    def test_main(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code != 0

    def test_main_run(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["run"])
        assert result.exit_code == 0
        assert "Summary generation complete!" in result.output

    def test_main_dashboard(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["dashboard"])
        assert result.exit_code == 0
        assert "Dashboard generated:" in result.output

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

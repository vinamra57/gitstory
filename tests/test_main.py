# WARNING: THIS TEST IS ONLY FOR THE MOST RUDIMENTARY VERSION OF main.py
# JUST TO MAKE SURE MY INITIAL VERSION WORKS
# ALTER WHEN U ACTUALLY IMPLEMENT IT
from click.testing import CliRunner
from main import cli


class TestMain:
    def test_main(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code != 0

    def test_main_run(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["run"])
        assert result.exit_code == 0
        assert "RUN TO BE COMPLETED" in result.output

    def test_main_compare(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["compare"])
        assert result.exit_code == 0
        assert "COMPARE TO BE COMPLETED" in result.output

    def test_main_dashboard(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["dashboard"])
        assert result.exit_code == 0
        assert "DASHBOARD TO BE COMPLETED" in result.output

    def test_main_since(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["since"])
        assert result.exit_code == 0
        assert "SINCE TO BE COMPLETED" in result.output

# WARNING: THIS TEST IS ONLY FOR THE MOST RUDIMENTARY VERSION OF main.py
# JUST TO MAKE SURE TESTING WORKS
from click.testing import CliRunner
from main import cli


class TestMain:
    def test_main(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code != 0

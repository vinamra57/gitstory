"""
Tests for main CLI interface.
Updated to work with integrated AI module.
"""
from click.testing import CliRunner
from gitstory.cli import cli
from unittest.mock import patch, MagicMock


class TestMain:
    def test_main(self):
        """Test main CLI group."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "GitStory" in result.output

    @patch('gitstory.cli.Config.load')
    @patch('gitstory.cli.RepoParser')
    @patch('gitstory.cli.AISummarizer')
    def test_main_run(self, mock_summarizer, mock_parser, mock_config):
        """Test run command with mocked components."""
        runner = CliRunner()

        # Mock config
        mock_config_instance = MagicMock()
        mock_config_instance.api_key = "test-key"
        mock_config_instance.model = "gemini-2.5-pro"
        mock_config.return_value = mock_config_instance

        # Mock parser
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse.return_value = {
            'commits': [{'hash': 'abc', 'author': 'Test', 'message': 'Test commit',
                        'type': 'feature', 'files_changed': 1, 'changes': 10}],
            'summary_text': '## TEST',
            'stats': {'total_commits': 1, 'by_type': {}, 'by_author': {}},
            'metadata': {}
        }
        mock_parser.return_value = mock_parser_instance

        # Mock AI summarizer
        mock_summarizer_instance = MagicMock()
        mock_summarizer_instance.summarize.return_value = {
            'summary': 'Test summary',
            'metadata': {'model': 'gemini-2.5-pro', 'tokens_used': 100, 'commits_analyzed': 1},
            'error': None
        }
        mock_summarizer.return_value = mock_summarizer_instance

        result = runner.invoke(cli, ["run"])
        assert result.exit_code == 0
        assert "Analyzing repository" in result.output
        assert "Test summary" in result.output

    def test_main_compare(self):
        """Test compare command (stub)."""
        runner = CliRunner()
        result = runner.invoke(cli, ["compare", "main", "feature"])
        assert result.exit_code == 0
        assert "under development" in result.output

    def test_main_since(self):
        """Test since command (stub)."""
        runner = CliRunner()
        result = runner.invoke(cli, ["since", "--since", "10-01-2024"])
        assert result.exit_code == 0
        assert "under development" in result.output

    @patch('gitstory.cli.Config.load')
    @patch('gitstory.ai.llm_client.LLMClient')
    def test_config_check(self, mock_client, mock_config):
        """Test config-check command."""
        runner = CliRunner()

        # Mock config
        mock_config_instance = MagicMock()
        mock_config_instance.api_key = "test-key"
        mock_config_instance.model = "gemini-2.5-pro"
        mock_config.return_value = mock_config_instance

        # Mock the LLM client validation
        mock_client_instance = MagicMock()
        mock_client_instance.validate_api_key.return_value = True
        mock_client.return_value = mock_client_instance

        result = runner.invoke(cli, ["config-check"])
        assert result.exit_code == 0
        assert "Configuration Status" in result.output

"""
Main CLI interface using Click.
Handles commands, arguments, and coordinates all modules.
"""
import click
import os
import sys
from typing import Optional

from .parser import RepoParser
from .ai import AISummarizer
from .dashboard import DashboardGenerator
from .utils.config import Config
from .utils.exceptions import GitStoryError


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    GitStory - Turn Git history into readable stories.

    Generate AI-powered summaries of your repository's evolution.
    """
    click.echo("Welcome to GitStory: Turning git repos into readable stories\n")


@cli.command()
@click.option(
    '--since',
    help='Start time (e.g., "2024-01-01" or "2w" for 2 weeks ago)',
    default=None
)
@click.option(
    '--until',
    help='End time (e.g., "2024-12-31" or "1m" for 1 month ago)',
    default=None
)
@click.option(
    '--branch',
    help='Branch name (defaults to current branch)',
    default=None
)
@click.option(
    '--dashboard',
    is_flag=True,
    help='Generate HTML dashboard instead of CLI output'
)
@click.option(
    '--repo-path',
    type=click.Path(exists=True),
    default='.',
    help='Path to Git repository (defaults to current directory)'
)
def run(since: Optional[str], until: Optional[str], branch: Optional[str],
        dashboard: bool, repo_path: str):
    """
    Generate a summary of repository history.

    Examples:
        gitstory run
        gitstory run --since 2w
        gitstory run --since 2024-01-01 --until 2024-06-30
        gitstory run --branch develop --dashboard
    """
    try:
        # Load configuration
        config = Config.load()

        # Validate API key
        if not config.api_key:
            click.echo("❌ Error: API key not configured\n", err=True)
            click.echo("Please set your API key in one of these ways:", err=True)
            click.echo("1. Set environment variable: export GITSTORY_API_KEY='your-key'", err=True)
            click.echo("2. Create .env file with: GITSTORY_API_KEY=your-key", err=True)
            click.echo("\nGet your API key from: https://aistudio.google.com/apikey", err=True)
            sys.exit(1)

        # Show loading message
        click.echo("🔍 Analyzing repository...")

        # Step 1: Parse repository
        parser = RepoParser(repo_path)
        parsed_data = parser.parse(since=since, until=until, branch=branch)

        # Check if any commits found
        if parsed_data['stats']['total_commits'] == 0:
            click.echo("⚠️  No commits found in the specified range", err=True)
            sys.exit(0)

        click.echo(f"✓ Found {parsed_data['stats']['total_commits']} commits")

        # Step 2: Generate AI summary
        click.echo("🤖 Generating AI summary...")
        summarizer = AISummarizer(config.api_key, config.model)

        output_format = "dashboard" if dashboard else "cli"
        result = summarizer.summarize(parsed_data, output_format)

        # Check for errors
        if result['error']:
            click.echo(f"❌ Error generating summary: {result['error']}", err=True)
            sys.exit(1)

        # Step 3: Display or save output
        if dashboard:
            click.echo("📊 Generating dashboard...")
            generator = DashboardGenerator()
            output_path = generator.generate(parsed_data, result['summary'])

            click.echo("\n✨ Dashboard generated successfully!")
            click.echo(f"📄 Saved to: {output_path}")
            click.echo(f"\nOpen in browser: file://{output_path}")
        else:
            # Display in terminal
            click.echo("\n" + "="*60)
            click.echo(result['summary'])
            click.echo("="*60)

            # Show metadata
            metadata = result['metadata']
            click.echo(f"\n📊 Stats: {metadata['commits_analyzed']} commits analyzed | "
                      f"{metadata['tokens_used']} tokens used")

    except GitStoryError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        if os.getenv('DEBUG'):
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('branch1')
@click.argument('branch2')
def compare(branch1: str, branch2: str):
    """
    Compare two branches and show differences.

    Example:
        gitstory compare main feature/new-auth
    """
    # STRETCH GOAL - Basic implementation
    click.echo(f"🔄 Comparing {branch1} with {branch2}...")
    click.echo("⚠️  This feature is under development")

    # TODO: Implement branch comparison
    # 1. Parse both branches
    # 2. Find unique commits
    # 3. Generate comparison summary


@cli.command()
@click.option(
    '--since',
    help='Start date (MM-DD-YYYY format)',
    required=True
)
def since(since: str):
    """
    Generate a summary starting from a specific date.

    Example:
        gitstory since --since 10-01-2024
    """
    click.echo(f"📅 Generating summary since {since}...")
    click.echo("⚠️  This feature is under development")

    # TODO: Implement time-based filtering
    # Use the run command with --since parameter


@cli.command()
def config_check():
    """Check configuration and API key validity."""
    try:
        config = Config.load()

        click.echo("Configuration Status:")
        click.echo(f"  API Key: {'✓ Set' if config.api_key else '✗ Not set'}")
        click.echo(f"  Model: {config.model}")

        if config.api_key:
            click.echo("\n🔌 Testing API connection...")
            from .ai.llm_client import LLMClient
            client = LLMClient(config.api_key, config.model)

            if client.validate_api_key():
                click.echo("✓ API key is valid!")
            else:
                click.echo("✗ API key validation failed", err=True)

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()

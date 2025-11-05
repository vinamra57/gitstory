# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///

import click
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from gitstory.parser import RepoParser

# make any changes to this file? it will certainly break
# it's respective test file in tests/test_main.py
# make sure you update those tests when you make changes
# - Derick C.

@click.group()
def cli():
    click.echo("Welcome to GitStory: Turning git repos into readable stories\n")


@cli.command("run", short_help="Generates a summary based on current code repo")
@click.argument("repo_path", type=click.Path(exists=True))
@click.option("--branch", default=None, help="Branch name (defaults to current branch)")
@click.option("--since", default=None, help="Start time (ISO or relative like '2w')")
@click.option("--until", default=None, help="End time (ISO or relative)")
def run(repo_path, branch, since, until):
    try:
        # Step 1: Load Gemini API key
        api_key = os.environ.get('GITSTORY_API_KEY', 'AIzaSyCOQjy85GSN5uNmdTmZMTlwPDVSboNP28s')
        if not api_key:
            click.echo("❌ Error: API key not configured\n", err=True)
            click.echo("Please set your API key in one of these ways:", err=True)
            click.echo("1. Set environment variable: export GITSTORY_API_KEY='your-key'", err=True)
            sys.exit(1)

        # Step 2: Parse repo
        parser = RepoParser(repo_path)
        parsed_data = parser.parse()

        # Step 3: Summarize
        from gemini_ai import AISummarizer
        summarizer = AISummarizer(api_key=api_key)
        result = summarizer.summarize(parsed_data)

        # Step 4: Display summary in terminal
        click.echo("✅ Summary generation complete!")
        click.echo("\n" + "=" * 60)
        click.echo(result['summary'])
        click.echo("=" * 60 + "\n")

        return "Summary generation complete!"

    except (Exception, SystemExit) as e:
        click.echo("❌ Error generating summary", err=True)
        click.echo(f"Error: {e}")
        sys.exit(getattr(e, 'code', 1))


@cli.command("dashboard", short_help="Generates downloadable report about repo")
def dashboard():
    try:
        # Step 1: Load configuration & validate API key
        api_key = '<key>'
        if not api_key:
            click.echo("❌ Error: API key not configured\n", err=True)
            click.echo("Please set your API key in one of these ways:", err=True)
            click.echo("1. Set environment variable: export GITSTORY_API_KEY='your-key'", err=True)
            click.echo("2. Create .env file with: GITSTORY_API_KEY=your-key", err=True)
            click.echo("\nGet your API key from: <INSERT_LINK>", err=True)
            sys.exit(1)

        click.echo("🔑 API key configured & loaded...")

        # Step 2: Parse repository
        click.echo("🔍 Analyzing repository...")
        from gitstory.parser import RepoParser
        parser = RepoParser('.')
        parsed_data = parser.parse()

        # Step 3: Generate AI summary
        click.echo("🤖 Generating AI summary...")
        from gemini_ai import AISummarizer
        summarizer = AISummarizer(api_key=api_key)
        result = summarizer.summarize(parsed_data)

        # Check for errors
        if not result:
            click.echo("❌ Error generating summary", err=True)
            sys.exit(1)

        # Step 4: Display results on Visualization Dashboard
        from visual_dashboard.dashboard_generator import generate_dashboard
        generate_dashboard(
            repo_data=parsed_data,
            ai_summary=result,
            output_file="dashboard.html",
        )
        click.echo("Dashboard saved!")

    except Exception as e:
        click.echo("❌ Error generating summary", err=True)
        click.echo(f"Error: {e}")
        sys.exit(1)
        parser = RepoParser(branch="temporary branch information")
        parsed_data = parser.parse()

        # Step 3: Generate AI summary
        click.echo("🤖 Generating AI summary...")
        from gemini_ai import AISummarizer
        summarizer = AISummarizer(api_key=api_key)
        result = summarizer.summarize(parsed_data)
    # Reads the JSON format + returns only the result

        # Check for errors
        if not result:
            click.echo("❌ Error generating summary", err=True)
            sys.exit(1)

        # Step 4: Display results on Visualization Dashboard
        from visual_dashboard.dashboard_generator import generate_dashboard
        generate_dashboard(
            repo_data=parsed_data,
            ai_summary=result,
            output_file="dashboard.html",
        )
        return "Dashboard saved!"



@cli.command("since", short_help="Generate a summary starting from a date MM-DD-YYYY")
def since():
    click.echo("SINCE TO BE COMPLETED")


@cli.command("compare", short_help="Compares two branches repos & generates summary")
def compare():
    click.echo("COMPARE TO BE COMPLETED")
@cli.command("parse-repo", short_help="parses the repository and returns structured commit data")
@click.argument("repo_path", type=click.Path(exists=True))
@click.option("--since", default=None, help="Start time (ISO or relative like '2w')")
@click.option("--until", default=None, help="End time (ISO or relative)")
@click.option("--branch", default=None, help="Branch name (defaults to current branch)")
def parse_repo(repo_path, since, until, branch):
    parser = RepoParser(repo_path)
    result = parser.parse(since=since, until=until, branch=branch)
    click.echo("Summary Text:")
    click.echo(result["summary_text"])
    click.echo("Stats:")
    click.echo(result["stats"])
    click.echo("Metadata:")
    click.echo(result["metadata"])

if __name__ == "__main__":
    cli()

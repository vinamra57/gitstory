# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///

import click
import sys
import visual_dashboard

# make any changes to this file? it will certainly break
# it's respective test file in tests/test_main.py
# make sure you update those tests when you make changes
# - Derick C.


@click.group()
def cli():
    click.echo("Welcome to GitStory: Turning git repos into readable stories\n")


@cli.command("run", short_help="Generates a summary based on current code repo")
@click.pass_context
def run(ctx):
    try:
        # TODO: replace mock API key with "real" information
        # Step 1: Load configuration & validate API key
        from gemini_ai import Config

        api_key = Config.Config(api_key="<MOCK_API_KEY>", model="<MOCK_MODEL>")

        if not api_key:
            click.echo("❌ Error: API key not configured\n", err=True)
            click.echo("Please set your API key in one of these ways:", err=True)
            click.echo(
                "1. Set environment variable: export GITSTORY_API_KEY='your-key'",
                err=True,
            )
            click.echo("2. Create .env file with: GITSTORY_API_KEY=your-key", err=True)
            click.echo("\nGet your API key from: <INSERT_LINK>", err=True)
            sys.exit(1)

        click.echo("🔑 API key configured & loaded...")

        # Step 2: Parse repository
        click.echo("🔍 Analyzing repository...")
        from parser import RepoParser

        parser = RepoParser.RepoParser(branch="temporary branch information")
        parsed_data = parser.parse()

        # Step 3: Generate AI summary
        click.echo("🤖 Generating AI summary...")
        from gemini_ai import AISummarizer

        summarizer = AISummarizer.AISummarizer(api_key=api_key, parsed_info=parsed_data)
        result = summarizer.summarize(parsed_data)
        # Check for errors
        if not result:
            click.echo("❌ Error generating summary", err=True)
            sys.exit(1)

        # Step 4: Display summary in terminal
        click.echo("✅ Summary generation complete!")
        click.echo("\n" + "=" * 60)
        click.echo(result)
        click.echo("=" * 60 + "\n")

        return "Summary generation complete!"

    except Exception as e:
        click.echo(f"❌ ERROR - Unexpected error: {e}\n", err=True)
        sys.exit(1)


@cli.command("dashboard", short_help="Generates downloadable report about repo")
@click.pass_context
def dashboard(ctx):
    try:
        # TODO: replace mock API key with "real" information
        # Step 1: Load configuration & validate API key
        from gemini_ai import Config

        api_key = Config.Config(api_key="<MOCK_API_KEY>", model="<MOCK_MODEL>")

        if not api_key:
            click.echo("❌ Error: API key not configured\n", err=True)
            click.echo("Please set your API key in one of these ways:", err=True)
            click.echo(
                "1. Set environment variable: export GITSTORY_API_KEY='your-key'",
                err=True,
            )
            click.echo("2. Create .env file with: GITSTORY_API_KEY=your-key", err=True)
            click.echo("\nGet your API key from: <INSERT_LINK>", err=True)
            sys.exit(1)

        click.echo("🔑 API key configured & loaded...")

        # Step 2: Parse repository
        click.echo("🔍 Analyzing repository...")
        from parser import RepoParser

        parser = RepoParser.RepoParser(branch="temporary branch information")
        parsed_data = parser.parse()

        # Step 3: Generate AI summary
        click.echo("🤖 Generating AI summary...")

        from gemini_ai import AISummarizer

        summarizer = AISummarizer.AISummarizer(api_key=api_key, parsed_info=parsed_data)
        result = summarizer.summarize(parsed_data)
        # Check for errors
        if not result:
            click.echo("❌ Error generating summary", err=True)
            sys.exit(1)

        # Step 4: Display results on Visualization Dashboard
        # TODO: what is repo_data? & Fix the generate_dashboard import @Ian
        generate_dashboard(
            repo_data={}, ai_summary=result, output_file="dashboard.html"
        )
        return "Dashboard saved!"

    except Exception as e:
        click.echo(f"❌ ERROR - Unexpected error: {e}\n", err=True)
        sys.exit(1)


@cli.command("since", short_help="Generate a summary starting from a date MM-DD-YYYY")
def since():
    click.echo("SINCE TO BE COMPLETED")


@cli.command("compare", short_help="Compares two branches repos & generates summary")
def compare():
    click.echo("COMPARE TO BE COMPLETED")


if __name__ == "__main__":
    cli()

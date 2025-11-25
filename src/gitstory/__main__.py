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
from gitstory.read_key.read_key import read_key

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
        try:
            api_key = read_key(os.path.dirname(os.path.abspath(__file__)))
        except Exception as ex:
            click.echo(f"❌ Error: {ex}\n", err=True)
            click.echo("This is most likely due to your key being set wrong!", err=True)
            click.echo("Please set your API key in one of these ways:", err=True)
            click.echo(
                "1. Call 'gitstory key --key=\"key\" '",
                err=True,
            )
            sys.exit(1)
        click.echo("🔑 API key configured & loaded...")

        # Step 2: Parse repo
        click.echo("🔍 Analyzing repository...")
        parser = RepoParser(repo_path)
        parsed_data = parser.parse()

        # Step 3: Summarize
        click.echo("🤖 Generating AI summary...")
        from gemini_ai import AISummarizer

        summarizer = AISummarizer(api_key=api_key)
        result = summarizer.summarize(parsed_data)

        # Check for errors before displaying
        if result.get("error"):
            error_msg = result["error"]
            click.echo("❌ Error generating summary", err=True)

            # Provide specific, actionable error messages
            if "empty" in error_msg.lower() or "no candidates" in error_msg.lower():
                click.echo(
                    "💡 The AI returned an empty response after 3 attempts.", err=True
                )
                click.echo(
                    "   This might be temporary. Please try again in a few moments.",
                    err=True,
                )
            elif "incomplete" in error_msg.lower() or "end marker" in error_msg.lower():
                click.echo(
                    "💡 The AI response was incomplete after 3 attempts.", err=True
                )
                click.echo("   This might be due to:", err=True)
                click.echo("   - Network interruption", err=True)
                click.echo("   - API timeout", err=True)
                click.echo("   Please try again.", err=True)
            elif "rate limit" in error_msg.lower():
                click.echo(
                    "💡 API rate limit exceeded. Please wait a few minutes and try again.",
                    err=True,
                )
            else:
                click.echo(f"   Details: {error_msg}", err=True)

            sys.exit(1)

        # Step 4: Display summary in terminal
        click.echo("✅ Summary generation complete!")
        click.echo("\n" + "=" * 60)
        click.echo(result["summary"])
        click.echo("=" * 60 + "\n")

        return "Summary generation complete!"

    except (Exception, SystemExit) as e:
        click.echo("❌ Error generating summary", err=True)
        click.echo(f"Error: {e}")
        sys.exit(getattr(e, "code", 1))


@cli.command("dashboard", short_help="Generates downloadable report about repo")
@click.argument("repo_path", type=click.Path(exists=True))
def dashboard(repo_path):
    try:
        # Step 1: Load configuration & validate API key
        try:
            api_key = read_key(os.path.dirname(os.path.abspath(__file__)))
        except Exception as ex:
            click.echo(f"❌ Error: {ex}\n", err=True)
            click.echo("This is most likely to your key being set wrong!", err=True)
            click.echo("Please set your API key in one of these ways:", err=True)
            click.echo(
                "1. Call 'gitstory key --key=\"key\" '",
                err=True,
            )
            sys.exit(1)
        click.echo("🔑 API key configured & loaded...")

        # Step 2: Parse repository
        click.echo("🔍 Analyzing repository...")
        from gitstory.parser import RepoParser

        parser = RepoParser(repo_path)
        parsed_data = parser.parse()

        # Step 3: Generate AI summary
        click.echo("🤖 Generating AI summary in Visualization Dashboard...")
        from gemini_ai import AISummarizer

        summarizer = AISummarizer(api_key=api_key)
        result = summarizer.summarize(parsed_data, output_format="dashboard")

        # Check for errors before generating dashboard
        if result.get("error"):
            error_msg = result["error"]
            click.echo("❌ Error generating summary", err=True)

            # Provide specific, actionable error messages
            if "empty" in error_msg.lower() or "no candidates" in error_msg.lower():
                click.echo(
                    "💡 The AI returned an empty response after 3 attempts.", err=True
                )
                click.echo(
                    "   This might be temporary. Please try again in a few moments.",
                    err=True,
                )
            elif "incomplete" in error_msg.lower() or "end marker" in error_msg.lower():
                click.echo(
                    "💡 The AI response was incomplete after 3 attempts.", err=True
                )
                click.echo("   This might be due to:", err=True)
                click.echo("   - Network interruption", err=True)
                click.echo("   - API timeout", err=True)
                click.echo("   Please try again.", err=True)
            elif "rate limit" in error_msg.lower():
                click.echo(
                    "💡 API rate limit exceeded. Please wait a few minutes and try again.",
                    err=True,
                )
            else:
                click.echo(f"   Details: {error_msg}", err=True)

            sys.exit(1)

        # Step 4: Display results on Visualization Dashboard
        from visual_dashboard.dashboard_generator import generate_dashboard

        generate_dashboard(
            repo_data=parsed_data,
            ai_summary=result,
            output_file="dashboard.html",
            repo_path=repo_path,
        )
        click.echo("✅ Dashboard saved!")

        return "Dashboard saved!"

    except Exception as e:
        click.echo("❌ Error generating dashboard", err=True)
        click.echo(f"Error: {e}")
        sys.exit(1)


@cli.command("since", short_help="Generate a summary starting from a date MM-DD-YYYY")
def since():
    click.echo("SINCE TO BE COMPLETED")


@cli.command("compare", short_help="Compares two branches repos & generates summary")
def compare():
    click.echo("COMPARE TO BE COMPLETED")


@cli.command(
    "parse-repo", short_help="parses the repository and returns structured commit data"
)
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


@cli.command("key", short_help="sets key to value")
@click.option("--key", help="Gemini key")
def key(key):
    cur_folder = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isdir(cur_folder + "/data"):
        os.mkdir(cur_folder + "/data")
    key_path = cur_folder + "/data/key.txt"
    with open(key_path, "w") as key_f:
        key_f.write(key)
    click.echo(f"Key written to {key_path}!")


if __name__ == "__main__":
    cli()

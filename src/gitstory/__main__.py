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

@click.group()
def cli():
    click.echo()
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
            click.echo("This is most likely to your key being set wrong!", err=True)
            click.echo(
                'Please set your API key: gitstory key --key="your_key"', err=True
            )
            sys.exit(1)
        click.echo("🔑 API key configured & loaded...")

        # Step 2: Parse repo
        click.echo("🔍 Analyzing repository...")
        parser = RepoParser(repo_path)
        parsed_data = parser.parse()

        # Step 3: Summarize
        click.echo("🤖 Generating AI summary...")
        from gitstory.gemini_ai import AISummarizer

        summarizer = AISummarizer(api_key=api_key)
        result = summarizer.summarize(parsed_data)

        # Check for errors before displaying
        if result.get("error"):
            error_msg = result["error"]
            
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
            click.echo(
                'Please set your API key: gitstory key --key="your_key"', err=True
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
        from gitstory.gemini_ai import AISummarizer

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
        click.echo()
        return "Dashboard saved!"

    except Exception as e:
        click.echo("❌ Error generating dashboard", err=True)
        click.echo()
        sys.exit(1)


@cli.command("since", short_help="Generate summary from specified time period")
@click.argument("repo_path", type=click.Path(exists=True))
@click.argument("time_period")
@click.option("--branch", default=None, help="Branch name (defaults to current branch otherwise)")
def since(repo_path, time_period, branch):
    """Generate repository summary starting from a relative time period.

    TIME_PERIOD supports: 4w (weeks), 6d (days), 8m (months), 9y (years)

    Examples:
        gitstory since ./ 2w           # Last 2 weeks on current branch
        gitstory since ./ 3m --branch=main  # Last 3 months on main branch
    """
    try:
        # Step 1: Load API key
        try:
            api_key = read_key(os.path.dirname(os.path.abspath(__file__)))
        except Exception as ex:
            click.echo(f"❌ Error: {ex}\n", err=True)
            click.echo("This is most likely to your key being set wrong!", err=True)
            click.echo(
                'Please set your API key: gitstory key --key="your_key"', err=True
            )
            sys.exit(1)
        click.echo("🔑 API key configured & loaded...")

        # Step 2: Parse repo with since parameter
        click.echo(f"🔍 Analyzing repository from {time_period} ago...")
        parser = RepoParser(repo_path)
        parsed_data = parser.parse(since=time_period, branch=branch)

        # Step 3: Summarize
        click.echo("🤖 Generating AI summary...")
        from gitstory.gemini_ai import AISummarizer

        summarizer = AISummarizer(api_key=api_key)
        result = summarizer.summarize(parsed_data)

        # Check for errors before displaying
        if result.get("error"):
            error_msg = result["error"]

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
        click.echo()
        
        return "Summary generation complete!"

    except ValueError as e:
        click.echo("❌ Error parsing time period", err=True)
        click.echo(
            "💡 Tip: Use formats like '2w' (weeks), '7d' (days), '3m' (months), '1y' (years)",
            err=True,
        )
        click.echo()
        sys.exit(1)
    except (Exception, SystemExit) as e:
        click.echo("❌ Error generating summary", err=True)
        click.echo()
        sys.exit(getattr(e, "code", 1))


@cli.command("compare", short_help="Compares two branches in repository and generates summary & branch differences")
@click.argument("repo_path", type=click.Path(exists=True))
@click.argument("base_branch")
@click.argument("compare_branch")
@click.option("--since", default=None, help="Start time (ISO or relative like '2w')")
@click.option("--until", default=None, help="End time (ISO or relative)")
@click.option(
    "--context", default=5, type=int, help="Number of context commits from merge base"
)
def compare(repo_path, base_branch, compare_branch, since, until, context):
    """Compare two branches and generate AI-powered comparison summary."""
    try:
        # Step 1: Load API key
        try:
            api_key = read_key(os.path.dirname(os.path.abspath(__file__)))
        except Exception as ex:
            click.echo(f"❌ Error: {ex}\n", err=True)
            click.echo("This is most likely to your key being set wrong!", err=True)
            click.echo(
                'Please set your API key: gitstory key --key="your_key"', err=True
            )
            sys.exit(1)
        click.echo("🔑 API key configured & loaded...")
        
        # Step 2: Compare branches
        click.echo("🔍 Comparing branches...")
        parser = RepoParser(repo_path)
        comparison_data = parser.compare(
            base_branch=base_branch,
            compare_branch=compare_branch,
            since=since,
            until=until,
            context_commits=context,
        )

        click.echo(
            f"   Base: {comparison_data['base_branch']} ({comparison_data['divergence_metrics']['base_commit_count']} commits)"
        )
        click.echo(
            f"   Compare: {comparison_data['compare_branch']} ({comparison_data['divergence_metrics']['compare_commit_count']} commits)"
        )
        click.echo(
            f"   Diverged: {comparison_data['divergence_metrics']['time_since_divergence']}"
        )

        # Step 3: Generate AI comparison summary
        click.echo("🤖 Generating AI comparison summary...")
        from gitstory.gemini_ai import AISummarizer

        summarizer = AISummarizer(api_key=api_key)
        result = summarizer.summarize_comparison(comparison_data)

        # Step 4: Handle errors
        if result.get("error"):
            click.echo("❌ Error generating comparison summary", err=True)
            click.echo(f"   Details: {result['error']}", err=True)
            sys.exit(1)

        # Step 5: Display results
        click.echo("✅ Comparison summary complete!")
        click.echo("\n" + "=" * 60)
        click.echo(result["summary"])
        click.echo("=" * 60 + "\n")
        click.echo()

        return "Comparison complete!"

    except ValueError as e:
        click.echo("❌ Error comparing branches", err=True)
        if "not found" in str(e).lower():
            click.echo(
                "💡 Tip: Run 'git branch -a' to see available branches", err=True
            )
        click.echo()
        sys.exit(1)
    except Exception as e:
        click.echo("❌ Error comparing branches", err=True)
        click.echo()
        sys.exit(1)


@cli.command("key", short_help="Sets Gemini API key internally to key passed in")
@click.option("--key", help="Enter your Gemini API key")
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

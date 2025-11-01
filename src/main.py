# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///
import click
from dashboard.html_generator import generate_dashboard

# make any changes to this file? it will certainly break
# it's respective test file in tests/test_main.py
# make sure you update those tests when you make changes
# - Derick C.


@click.group()
def cli():
    click.echo("Welcome to GitStory")


@cli.command("run", short_help="runs on repo")
def run():
    click.echo("RUN TO BE COMPLETED")


@cli.command("compare", short_help="compares two branches")
def compare():
    click.echo("COMPARE TO BE COMPLETED")


@cli.command("dashboard", short_help="generates html dashboard about repo")
def dashboard():
    click.echo("Generating HTML dashboard...")

    # Here is just a placeholder/mock data I'm using (based off the structure specified in the docs)
    repo_data = {
        "commits": [
            {
                "hash": "abc123",
                "author": "Jane",
                "timestamp": "2024-10-15T10:30:00",
                "message": "First Commit",
                "type": "feature",
                "files_changed": 5,
                "changes": 247,
            },
            {
                "hash": "abc456",
                "author": "Noah",
                "timestamp": "2024-10-15T12:30:00",
                "message": "Fixed Bugs",
                "type": "feature",
                "files_changed": 1,
                "changes": 50,
            },
        ],
        "stats": {
            "total_commits": 297,
            "by_type": {"feature": 120, "bugfix": 80},
            "by_author": {
                "Jane": {"count": 247, "types": {}},
                "Noah": {"count": 50, "types": {}},
            },
        },
    }

    ai_summary = {
        "summary": '"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at varius dolor. Etiam suscipit lorem consectetur purus pharetra vehicula. Nam vitae pellentesque sapien. Praesent at libero ut velit elementum pharetra nec nec sapien."',
        "metadata": {
            "model": "glm-4-plus",
            "tokens_used": 1500,
            "commits_analyzed": 247,
        },
        "error": None,
    }

    output_file = generate_dashboard(repo_data, ai_summary)

    # This 'f' is to allow embedding variables/expressions inside {}
    click.echo(f"Dashboard saved to: {output_file}")


@cli.command("since", short_help='i have no idea what "since" does')
def since():
    click.echo("SINCE TO BE COMPLETED")


if __name__ == "__main__":
    cli()

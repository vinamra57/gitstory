# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///
import click
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gitstory.parser import RepoParser

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
    click.echo("DASHBOARD TO BE COMPLETED")


@cli.command("since", short_help='i have no idea what "since" does')
def since():
    click.echo("SINCE TO BE COMPLETED")


@cli.command("parse-repo", short_help="parses the repository and returns structured commit data")
@click.argument("repo_path", type=click.Path(exists=True))
@click.option("--since", default=None, help="Start time (ISO or relative like '2w')")
@click.option("--until", default=None, help="End time (ISO or relative)")
@click.option("--branch", default=None, help="Branch name (defaults to current branch)")
def parse_repo(repo_path, since, until, branch):
    parser = RepoParser(repo_path)
    result = parser.parse(since=since, until=until, branch=branch)
    click.echo("Summary Text:")
    click.echo(result['summary_text'])
    click.echo("Stats:")
    click.echo(result['stats'])
    click.echo("Metadata:")
    click.echo(result['metadata'])


if __name__ == "__main__":
    cli()

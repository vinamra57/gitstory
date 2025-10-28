# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///
import click

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


if __name__ == "__main__":
    cli()

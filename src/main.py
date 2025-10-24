# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///
import click

# make any changes to this file? check the relative test file, cuz it'll
# definitely break that and piss it off -Derick :3


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

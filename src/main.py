# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///
import click


@click.group()
def cli():
    click.echo("Welcome to GitStory")


@cli.command("run", short_help="running is good exercize")
def run():
    click.echo("TO BE COMPLETED")


@cli.command("compare", short_help="comparing isn't good exercize")
def compare():
    click.echo("TO BE COMPLETED")


'''@cli.command("pname", short_help = "implementation of the click name pgrm")
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def pname(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")'''

if __name__ == "__main__":
    cli()

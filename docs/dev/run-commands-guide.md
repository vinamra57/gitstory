# How to Run
To run GitStory's commands as you are working on the code, take the following steps:

## Step 1: Run GitStory on shell, command-line interface (CLI)
Open up a CLI tab (ex: Terminal window for macOS users), and navigate to the GitStory directory (don't reach the src directory, just GitStory itself). (you may use the CLI integrated in your IDE, such as how Visual Studio Code has a terminal window, if provided).

## Step 2: Run specific commands
Run GitStory's commands as listed below:

`gitstory run`: runs GitStory and generates a code-summary in the CLI itself (i.e. its printed on the CLI to user).

```
uv run python3.13 src/gitstory/__main__.py run "<YOUR_REPO_LOCATION_PATH>"
```

`gitstory dashboard`: this generates a HTML file called `dashboard.html` in an `output` folder, located in at the root of your chosen Git repository (the output directory will be created by GitStory).
```
uv run python3.13 src/gitstory/__main__.py dashboard "<YOUR_REPO_LOCATION_PATH>"
```

**since & compare commands: CURRENTLY WORKING ON (updated Nov 15), documentation for these commands to come soon**

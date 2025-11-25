# How to Run
To run GitStory's commands as you are working on the code, take the following steps:

## Step 1: Run GitStory on shell, command-line interface (CLI)
Open up a CLI tab (ex: Terminal window for macOS users), and navigate to the GitStory directory (don't reach the src directory, just GitStory itself). (you may use the CLI integrated in your IDE, such as how Visual Studio Code has a terminal window, if provided).

## Step 2: Run specific commands
Run GitStory's commands as listed below:

`gitstory run "<YOUR_REPO_LOCATION_PATH>"`: runs GitStory and generates a code-summary in the CLI itself (i.e. its printed on the CLI to user).

```
uv run python3.13 src/gitstory/__main__.py run "<YOUR_REPO_LOCATION_PATH>"
```

`gitstory dashboard "<YOUR_REPO_LOCATION_PATH>"`: this generates a HTML file called `dashboard.html` in an `output` folder, located in at the root of your chosen Git repository (the output directory will be created by GitStory).
```
uv run python3.13 src/gitstory/__main__.py dashboard "<YOUR_REPO_LOCATION_PATH>"
```
`gitstory compare "<YOUR_REPO_LOCATION_PATH>" <base-branch> <compare-branch>`: compares the two given branches (specifically, the "compare-branch" from the "base-branch" you list accordingly) and generates a summary stating how the two branches are different (based on functionalities and commits that each differs in each branch).
```
uv run python3.13 src/gitstory/__main__.py compare "<YOUR_REPO_LOCATION_PATH>" <BASE-BRANCH> <COMPARE-BRANCH>
```
**since commands: CURRENTLY WORKING ON (updated Nov 15), documentation for these commands to come soon**

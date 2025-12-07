# How to Run
To run GitStory's commands as you are working on the code, take the following steps:

## Step 1: Run GitStory on shell, command-line interface (CLI)
Open up a CLI tab (ex: Terminal window for macOS users), and navigate to the GitStory directory (don't reach the src directory, just GitStory itself). (you may use the CLI integrated in your IDE, such as how Visual Studio Code has a terminal window, if provided).

## Step 2: Run specific commands
Run GitStory's commands as listed below (*copy the commands in the **blocks** rather the ones listed with the description*, we have included them to link how the user runs GitStory vs. how developers run GitStory):

`gitstory key --key="<YOUR_API_KEY>"`: takes the Gemini API key given by user and integrates it into GitStory, this is **THE FIRST COMMAND** that needs to be run, otherwise other commands will throw errors (as it doesn't have an API key that it can work with). If you have not obtained your key, follow instructions [here](set-up-API.md).

```
uv run python3.13 src/gitstory/__main__.py key --key="<YOUR_API_KEY>"
```

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
uv run python3.13 src/gitstory/__main__.py compare "<YOUR_REPO_LOCATION_PATH>" <YOUR_BASE-BRANCH> <YOUR_COMPARE-BRANCH>
```
`gitstory since "<YOUR_REPO_LOCATION_PATH>" <Nx>`: Generates a concise summary of the repository’s commit history based on a given time-period on the current branch, highlighting major development events such as feature additions, bug fixes, and refactors. For example, a user could run "since 2m", where GitStory would generate a summary based on only the last 2 months worth of commits. Look below for additional time formats:

**Time Period Formats:**
- `Nd` — N days ago (e.g., `5d` = last 5 days)
- `Nw` — N weeks ago (e.g., `2w` = last 2 weeks)
- `Nm` — N months ago (e.g., `3m` = last 3 months)
- `Ny` — N years ago (e.g., `1y` = last year)

```
uv run python3.13 src/gitstory/__main__.py since "<YOUR_REPO_LOCATION_PATH>" <Nx>
```

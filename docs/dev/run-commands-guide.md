# How to Run
As of 11.08.2025, the way that you run a file in GitStory (`uv run python <file_location>`) is the CURRENT way to run GitStory on any given repo. We are working on restoring a build version that DOES NOT require users to also have to git clone, which is aiming to be released by **Nov 12**. In the meanwhile, here are the steps you take to run GitStory on your chosen git repository. 

## Step 1: Clone the GitStory repo
Clone this GitStory repo in a chosen PC location (i.e. Desktop, specific folders, etc).

## Step 2: Run GitStory on shell, command-line interface (CLI)
Open up a CLI tab (ex: Terminal window for macOS users), and navigate to the GitStory directory (don't reach the src directory, just GitStory itself).

## Step 3: Run specific commands
Run GitStory's commands as listed below:

`uv run python3.13 src/gitstory/__main__.py run "<YOUR_REPO_LOCATION_PATH>"`: equivalent to `gitstory run`, this runs GitStory and generates a code-summary in the CLI itself (i.e. its printed on the CLI to user)

`uv run python3.13 src/gitstory/__main__.py dashboard "<YOUR_REPO_LOCATION_PATH>"`: equivalent to `gitstory dashboard`, this generates a HTML file called `dashboard.html` in an `output` folder, located in at the root of your chosen Git repository (the output directory will be created by GitStory).

**since & compare commands: CURRENTLY WORKING ON (updated Nov 8)**

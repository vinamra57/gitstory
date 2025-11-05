#  Setting Up All The Stuff
This is a short writeup from Derick Chiem about setting up your computer to be able to run the project and it's tools! Please visit the documentation for these projects if you have any questions about the tools. This guide covers the process for Mac, Linux, and Windows.

**NOTE:** I have not found out how to make these tools well-integrated with VSCode or any IDE (I just call the console commands directly and refer to them). Please make a pull request if you find a way to integrate them well so that everyone can have an easier time.

## Step 0: Install git
I will presume that you have git installed already, and I assume you are smart enough to install it if you need to.

## Step 0.5: Clone the Gitstory Repository
Use the `git clone` command to clone the repository using the link provided at the GitHub, which itself is linked [here](https://github.com/vinamra57/gitstory). You can also use tools packed in with the text editor or IDE of one's choosing for this task. The following command is the most basic command for cloning the repository if you don't want to do anything else special:<br>
`git clone https://github.com/vinamra57/gitstory.git`

## Step 1: Downloading Python 3.13 (or newer)
I would presume Python has been already install, but the minimum version we are requiring is Python 3.13. Grab it [here](https://www.python.org/downloads/). The version we are using is Python 3.13, but it is unnecesary to download this exact version. Newer versions of Python should work fine.

## Step 2: Installing UV
Next, one will need to install the UV Python project/package manager. The installation guide is linked [here](https://docs.astral.sh/uv/getting-started/installation/), but below will be commands that you can use to install it.<br>
Mac/Linux:<br>
`curl -LsSf https://astral.sh/uv/install.sh | sh` <br>
or <br>
`wget -qO- https://astral.sh/uv/install.sh | sh`<br>
Windows:<br>
`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`<br>

Next, install Python locally to the directory:<br>
`uv python install` or `uv python install 3.13` should both work.<br>

Next, setup the virtual enviroment:<br>
`uv venv` <br>

When you want to run a Python file from this point forward, you would do:<br>
`uv run python <file_location>`

UV has a *lot* of features, way too many to cover here. Read [the documentation](https://docs.astral.sh/uv/getting-started/) to see the *many* features it has.

**IMPORTANT NOTE:** When committing to git, make sure that uv.lock is added to the commit if a change has occurred to it, otherwise there will be problems! This should be caught automatically, but I am noting it anyways.

## Step 3: Setting Up pre-commit
All commands from this point forward is very simple. We will use UV to install all our tools, starting with pre-commit: <br>
`uv tool install pre-commit`<br>
After this, we have to link so it runs automatically on every commit:<br>
`pre-commit install`

## Step 4: Setting Up tox
Tox is our one-command test suite that automatically does linting and testing. To install it: <br>
`uv tool install tox --with tox-uv` <br>
After that, you can run the entire testing suite at any time with: <br>
`tox run` <br>
If you want to put in more tests (which I hope you do), we are using the [pytest framework](https://docs.pytest.org/en/stable/). Look at the test guide at [test-guide.md](test-guide.md) to learn about how to use it<br>
**Side note:** If you are interested in running the formatter we are using (Ruff) by itself, you can call `uvx ruff format`. It is also in the tox suite, but in it's linter form.

## Thank you!!!
If there are any problems with installation, please tell me (Derick Chiem) ASAP!

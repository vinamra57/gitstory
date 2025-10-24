#  Setting Up All The Stuff
This is a short writeup from Derick Chiem about setting up your computer to be able to run the project and it's tools! Please visit the documentation for these projects if you have any questions about the tools. This guide covers the process for Mac, Linux, and Windows

## Step 0: Install git
I will presume that you have git installed already, and I assume you are smart enough to install it if you need to.
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

Next, setup the virtual enviorment:<br>
`uv venv` <br>

When you want to run a Python file from this point forward, you would do:<br>
`uv run <file_location>`

UV has a *lot* of features, way too many to cover here. Read [the documentation] to see the *many* features it has.

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
If you want to put in more tests (which I hope you do), we are using the [pytest framework](https://docs.pytest.org/en/stable/). Make sure to put your tests within the `tests` folder and to follow the naming scheme, or else the tests will not be detected. <br>
**Side note:** If you are interested in running the formatter we are using (Ruff) by itself, you can call `uvx ruff format`. It is also in the tox suite, but in it's linter form.

## Thank you!!!
If there are any problems with installation, please tell me (Derick Chiem) ASAP!

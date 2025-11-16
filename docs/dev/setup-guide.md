#  Setting Up GitStory
This guide covers the process of how to setup GitStory for Mac, Linux, and Windows for developers looking to contribute or view the GitStory code.

## Step 0: Make sure your PC has Git
Make sure that the PC you will be working on has Git installed, if not, please install Git on your PC (as mentioned [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)).

## Step 0.5: Clone the Gitstory Repository (if you have not done so already)
Use the `git clone` command to clone the repository using the link provided at the GitHub, which itself is linked [here](https://github.com/vinamra57/gitstory).

```
git clone https://github.com/vinamra57/gitstory.git
```

## Step 1: Downloading Python 3.13 (or newer)
The minimum version GitStory requires is Python 3.13. Grab it [here](https://www.python.org/downloads/). If you have a newer version of Python, that will also work (i.e. you don't need to download the specific 3.13 version).

## Step 2: Installing UV + Python (in GitStory folder)
Next, install the UV Python project/package manager. The installation guide is linked [here](https://docs.astral.sh/uv/getting-started/installation/), but below will be commands that you can use to install it.

For Mac/Linux users:
```
curl -LsSf https://astral.sh/uv/install.sh | sh 
--OR--
wget -qO- https://astral.sh/uv/install.sh | sh
```
For Windows:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Next, install Python locally to the directory (either command will work) + set up the virtual enviornment:
```
uv python install
--OR--
uv python install 3.13
```

```
uv venv
```

When you want to run a Python file from this point forward, you would do:
```
uv run python <file_location>
```

UV has a *lot* of features, to learn more about UV, read [the documentation](https://docs.astral.sh/uv/getting-started/).

**IMPORTANT NOTE:** When committing to git, make sure that `uv.lock` is added to the commit if a change has occurred to it, otherwise there will be problems! 

## Step 3: Setting Up pre-commit
All commands from this point forward is very simple. We will use UV to install all our tools, starting with pre-commit: 
```
uv tool install pre-commit
```
After this, we have to link so it runs automatically on every commit:
```
pre-commit install
```

## Step 4: Setting Up tox
Tox is our one-command test suite that automatically does linting and testing. To install it:
```
uv tool install tox --with tox-uv
```
After that, you can run the entire testing suite at any time with:
```
tox run
```
If you want to put in more tests, GitStory uses the [pytest framework](https://docs.pytest.org/en/stable/). Look at the test guide at [test-guide.md](test-guide.md) to learn about how to use it<br>
**Side note:** If you are interested in running the formatter we are using (Ruff) by itself, you can call `uvx ruff format`. It is also in the tox suite, but in it's linter form.

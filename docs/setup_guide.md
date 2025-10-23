#  Setting Up All The Stuff
This is a short writeup from Derick Chiem about setting up your computer to be able to run the project and it's tools! Please visit the documentation for these projects if you have any questions about the tools. This guide covers the process for Mac, Linux, and Windows
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
## Step 3: Setting up Pre-Commit

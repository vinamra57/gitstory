# How to Build GitStory

The tools of [uv](https://docs.astral.sh/uv/getting-started/installation/) and [pipx](https://pipx.pypa.io/stable/installation/) are required for installation. Linked is their relative install guides (for downloading `pipx`, it is also necessary to have `brew` installed, head over to hear to install [brew](https://brew.sh/), and a very helpful troubleshooting [guide](https://macpaw.com/how-to/fix-brew-command-not-found-mac) for those facing issues with `brew`). For Windows, they also must be included in the `PATH` environment variable.
\
\
Once you have `uv` and `pipx`, to build GitStory into a "final product" (i.e. using GitStory without `uv run` commands like a user), follow the instructions below: 

## Step 1: Run `uv build`
In the CLI terminal (navigated to the GitStory directory), run:

```
uv build --no-sources --sdist
```

This will build GitStory in your local directory, producing a `dist` folder in the root for GitStory, where you will see a .tar.gz file.

## Step 2: Install GitStory using `pipx`
pipx is heavily reccomended for the installation of GitStory, as it sandboxes GitStory within it's own Python environment. To install the file you just built, from the root directory of GitStory run:

```
pipx install ./dist/*.tar.gz
```

This will globally install GitStory to your computer, where you can open up a new terminal/command-line and run GitStory commands! (ex: `gitstory run <repo-path>`).

## Step 3: Use the GitStory build!
Once you have downloaded the GitStory build, you will be able to use GitStory using our "regular" commands. To get a quick overview of how our commands look like in GitStory, head over to our [user-documentation](https://github.com/vinamra57/gitstory/tree/main/docs/user/run-commands-guide.md).

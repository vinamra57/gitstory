# Adding Packages

Packages can be added to the local developer environment when one is experimenting with them, but it's recommended to add them to the `pyproject.toml` and `tox.toml` as dependencies so that both other developers and the test suite itself has access to them (if pushing changes to main). *This also ensures tests pass and no external issues occur when trying to run new edits that may need these packages.*

## Adding Packages to the Developer Enviroment
To do this, simply `uv pip install <PACKAGE_OF_CHOICE>`

## Adding Dependencies to UV 
To add a dependency to UV, call the following command:\
\
`uv add <package>`\
\
You can append a `>=[version number]` to set a version number explicitly, but UV automatically sets the most recent version as the required version by default.

## Adding Dependencies to Tox
Adding a dependency to tox is simple as well, but requires editing the tox file manually. You have to add a new line to the `deps` section of `tox.toml` from root, adding a line between the brackets consisting of (of course with proper whitespacing which I cannot show here):\
\
`"[package name]>=[min version number]",`\
\
You can also manually add dependencies to UV with this exact format in the `dependencies` section, but doing so is wholly unnecesary.

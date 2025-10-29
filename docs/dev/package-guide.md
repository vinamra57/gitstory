# Adding Packages

Packages can be added to the local developer environment when one is experimenting with them, but it's recommended to add them to the `pyproject.toml` and `tox.toml` as dependencies so that both other developers and the test suite itself has access to them.

## Adding Packages to the Developer Enviroment
To do this, simply `uv pip install <package of choice>`

## Adding Dependencies to UV 
Adding a dependency to UV is simple. Simply call the following command:<br>
`uv add <package>`<br>
You can append a `>=[version number]` to set a version number explicitly, but UV automatically sets the most recent version as the required version by default.

## Adding Dependencies to tox
Adding a dependency to tox is simple as well, but requires editing the tox file manually. You have to add a new line to the `deps` section of `tox.toml` from root, adding a line between the brackets consisting of (of course with proper whitespacing which I cannot show here): <br>
`"[package name]>=[min version number]",`<br>
You can also manually add dependencies to UV with this exact format in the `dependencies` section, but doing so is wholly unnecesary.
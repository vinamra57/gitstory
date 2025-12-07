# Builds, than uninstalls then reinstalls gitstory
# Made for quick rebuilding so that you can get to testing the built version ASAP
# Install pipx before you use this https://pipx.pypa.io/stable/installation/
# (technically it also requires UV but you have it by this point, I presume)
# If you don't go read the docs
# If you run into trouble with this script, tell me and/or fix it yourself
# It's three whole lines that I threw together in actually 10 seconds
# - Derick Chiem

uv build --no-sources --sdist
pipx uninstall gitstory
pipx install ./dist/*.tar.gz
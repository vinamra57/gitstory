# Windows script built for testing, similar to reinstall-gitstory.sh

uv build --no-sources --sdist
pipx uninstall gitstory
$files = Get-ChildItem ./dist/gitstory-*.tar.gz
foreach ($file in $files) {pipx install $file}
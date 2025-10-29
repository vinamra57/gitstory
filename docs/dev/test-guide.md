# How to Test
Out tests use pytest, but everything regarding pytest will be automatically handled using our test handler tox.
## Running Tests

You call the `tox run` command to run the entire test suite and linter, once everything is setup. This also runs the tests by installing the dependencies to a new folder then running it there, so that it is sandboxed from the development enviroment.

## Adding tests

To add a test, you **must** put it within the `tests` folder, or else it won't be detected. The file it is in must also follow the `test_<TESTED FILE>.py` name scheme for the same reason. Tests are otherwise just `def` functions without any parameters containing `assert` statements, with a name scheme of `test_<relevant test name>`. You can also create a class containing many tests for organization purposes, Following a `Test<Relevant Category Name>` naming scheme. There are examples at `tests/test_sample.py` and `tests/test_sample_other.py` from root.
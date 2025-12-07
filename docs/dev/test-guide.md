# How to Test GitStory
GitStory's tests use `pytest`, but everything regarding pytest will be automatically handled using our test handler tox.

## Running Tests

You call the `tox run` command to run the entire test suite and linter, once everything is setup. This also runs the tests by installing the dependencies to a new folder then running it there, so that it is sandboxed from the development enviroment.

## Adding tests
Tests are `def` functions without any parameters (other than `self` if in a test class) containing `assert` statements. <br>
In order for tests to be detected by `pytest`:<br>
- Tests must be added within the `tests` folder
- Test files must follow the `test_<TESTED FILE>.py` name scheme
- Tests functions must follow a name scheme of `test_<relevant test name>`
- Classes that wrap tests must be named `Test<Relevant Category Name>`

To see how our tests look like, head over to the `/tests` folder located at the root of the project.

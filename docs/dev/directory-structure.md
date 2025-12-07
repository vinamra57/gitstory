# Directory Layout

Here is a layout of how GitStory’s files are structured:
- `.github/workflows`: Contains main.yml, which configure the Python dependencies, tests, and linter for GitHub Actions and continuous integration, and publish.yml, which is used for creating a GitStory build
- `docs`: Contains documentation and guidelines for different users, with a `user` folder for user-related documentation and a `dev` folder for developer information and documentation
- `reports`: Includes the GitStory’s weekly updates (pushed every Monday)
- `src/gitstory`: Stores the main codebase - contains of gemini_ai, parser, and visual_dashboard directories which store each respective component's code; main.py calls each of the components (and puts the whole program together)
- `tests`: Where all the tests are stored for each function/class in `src` 

Other files present in the main directory relate to the Python installation, project setup (i.e. imports) and testing for the codebase.

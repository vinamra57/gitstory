# Directory Layout

Here is a layout of how GitStory’s files are structured:
- `.github/workflows`: Contains main.yml, which configure the Python dependencies, tests, and linter for GitHub Actions and continuous integration.
- `docs`: Contains documentation and guidelines for different users, with a `user` folder for user-related documentation and a `dev` folder for developer information and documentation
- `reports`: Includes the GitStory’s weekly updates (pushed every Monday)
- `src`: Stores the main codebase - currently this only has a couple of files, but will be where main.py is stored (the client-interface) and folders containing other files such as those connecting the LLM to RepoParser will be
- `tests`: Where all the tests are stored for each function/class in `src` 

Other files present in the main directory relate to the Python installation, project setup (i.e. imports) and testing for the codebase

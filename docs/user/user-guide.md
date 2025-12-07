# GitStory User Guide



## 1. Overview

**GitStory** is a command-line tool designed to help developers quickly understand the history and structure of a software project by turning Git commit data into a readable “story.”  

Instead of sifting through long commit logs or complex branches, GitStory will summarize a repository’s evolution into clear, concise language.  

The goal is to help users—especially new team members or project managers—gain an understanding of a project’s development in minutes rather than hours.

### Key Features
- **Repository Parsing Engine:** Extract commit messages, authors, timestamps, and branch data.  
- **Commit Grouping:** Cluster related commits (e.g., features, bug fixes, refactors).  
- **AI Summarization:** Use commit metadata to produce human-readable summaries.  
- **Command-Line Interface:** Run directly from the terminal with intuitive commands.  
- **Visualization Dashboard:** Generate a static HTML dashboard showing project evolution.  
- **Time-Bound Summarization:** Filter summaries by date or development period.  

GitStory runs locally to maintain privacy and never sends source code outside the user’s environment.

---

## 2. Installation

### 2.1 Prerequisites

| Requirement | Version | Purpose |
|--------------|----------|----------|
| **Python** | 3.13 or newer | Core runtime environment, head over to [setup-guide.md](https://github.com/vinamra57/gitstory/blob/release-branch/docs/dev/setup-guide.md) for more details |
| **Git** | Latest stable | Repository access, head over to [setup-guide.md](https://github.com/vinamra57/gitstory/blob/release-branch/docs/dev/setup-guide.md) for more details |
| **UV** | Latest | Virtual environment and package management, head over to [setup-guide.md](https://github.com/vinamra57/gitstory/blob/release-branch/docs/dev/setup-guide.md) for more details |
| **Gemini API-Key** | N/A | Used in GitStory project, head over to [set-up-API.md](set-up-API.md) to obtain API-Key

### 2.2 Clone the Repository

```bash
git clone https://github.com/vinamra57/gitstory.git
cd gitstory
```

### 2.3 Install UV and Set Up the Environment

**macOS/Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If it doesn't work right after, then try running these lines:
```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

source ~/.zshrc
```

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
If it doesn't work right after, then try running these lines:
```
$env:Path = "$env:USERPROFILE\.local\bin;" + $env:Path

[System.Environment]::SetEnvironmentVariable('Path', "$env:USERPROFILE\.local\bin;" + [System.Environment]::GetEnvironmentVariable('Path', 'User'), 'User')
```

Then, install Python and create a virtual environment:
```bash
uv python install 3.13
uv venv
uv sync
```

This will install all necessary dependencies for development and testing.

---

## 3. Running GitStory commands

When development is complete, GitStory will run as a command-line tool from the terminal. Users will navigate to a Git repository and use the following commands to generate summaries or reports. Until then, here are the commands to use to run GitStory:

### 3.0  `uv run python3.13 src/gitstory/__main__.py key key="<YOUR_API_KEY>"`
Takes the Gemini API key given by user and integrates it into GitStory, this is **THE FIRST COMMAND** that needs to be run, otherwise other commands will throw errors (as it doesn't have an API key that it can work with). If you have not obtained your key, follow instructions [here](set-up-API.md).

```
uv run python3.13 src/gitstory/__main__.py key --key="<YOUR_API_KEY>"
```

### 3.1 `uv run python3.13 src/gitstory/__main__.py run "<YOUR_REPO_LOCATION_PATH>"`
Generates a concise summary of the repository’s commit history on the current branch, highlighting major development events such as feature additions, bug fixes, and refactors.

```
uv run python3.13 src/gitstory/__main__.py run "<YOUR_REPO_LOCATION_PATH>"
```

### 3.2 `uv run python3.13 src/gitstory/__main__.py dashboard "<YOUR_REPO_LOCATION_PATH>"`
Creates a static HTML dashboard report containing:
- A timeline of key commits  
- Contributor statistics and activity charts  
- Summaries grouped by time period or feature area  

This report will be saved locally for offline viewing or sharing.

```
uv run python3.13 src/gitstory/__main__.py dashboard "<YOUR_REPO_LOCATION_PATH>"
```

### 3.3 `uv run python3.13 src/gitstory/__main__.py compare "<YOUR_REPO_LOCATION_PATH>" <YOUR_BASE_BRANCH> <YOUR_COMPARE-BRANCH>`
Compares the two given branches (specifically, the "compare-branch" from the "base-branch" you list accordingly) and generates a summary stating how the two branches are different (based on functionalities and commits that each differs in each branch).

```
uv run python3.13 src/gitstory/__main__.py compare "<YOUR_REPO_LOCATION_PATH>" <YOUR_BASE_BRANCH> <YOUR_COMPARE-BRANCH>
```

### 3.4 `uv run python3.13 src/gitstory/__main__.py since "<YOUR_REPO_LOCATION_PATH>" <Nx>`
Generates a concise summary of the repository’s commit history based on a given time-period on the current branch, highlighting major development events such as feature additions, bug fixes, and refactors. For example, a user could run "since 2m", where GitStory would generate a summary based on only the last 2 months worth of commits. Look below for additional time formats:

**Time Period Formats:**
- `Nd` — N days ago (e.g., `5d` = last 5 days)
- `Nw` — N weeks ago (e.g., `2w` = last 2 weeks)
- `Nm` — N months ago (e.g., `3m` = last 3 months)
- `Ny` — N years ago (e.g., `1y` = last year)

```
uv run python3.13 src/gitstory/__main__.py since "<YOUR_REPO_LOCATION_PATH>" <Nx>
```

---

## 4. Using GitStory

1. Navigate to a valid Git repository:
   ```bash
   cd path/to/repository
   ```

2. Run one of the supported commands (see above).

3. GitStory will:
   - Parse commit metadata from the repository.
   - Group related commits by type or time period.
   - Generate a readable summary (terminal output or HTML dashboard).

4. If errors occur (e.g., invalid repository, no commits, or missing dependencies), GitStory will display descriptive error messages and instructions for resolution.

---

## 5. Troubleshooting

| Problem | Possible Cause | Recommended Solution |
|----------|----------------|----------------------|
| “Not a valid Git repository” | Running outside a folder containing `.git/` | Navigate to a valid Git repository. |
| “No commits found” | Empty repository | Make at least one commit before running GitStory. |
| “Missing API key” | AI summarization key not configured | Add your key using the 'key' functionality above |
| “Permission denied” | Insufficient permissions for output files | Run terminal with appropriate privileges or change directory. |

If problems persist, reinstall your environment:
```bash
uv venv
uv sync
```

---

## 6. Privacy and Security

GitStory only processes **commit metadata** such as commit messages, authors, timestamps, and branch names.  
No source code or sensitive data is transmitted outside the user’s computer.  

When AI summarization is used, metadata is sent securely over HTTPS to the configured model API.  
Users supply their own API keys via environment variables or a `.env` file.

---

## 7. Reporting Bugs and Issues

As of this stage of development, GitStory’s core features have been implemented. The GitStory team uses **GitHub Issues** to track bugs and feature requests, and encourages users to open issues they see in GitStory. Users and testers may also report setup or documentation problems directly to the team (via Discord or class communication channels), though GitHub Issues is preferred.

When GitStory’s issue tracker is active, a helpful bug report should include:

- **Summary:** short, specific title (e.g., `gitstory run --dashboard fails on Windows`)  
- **Steps to reproduce:** numbered actions to replicate the issue  
- **Expected result:** what should have happened  
- **Actual result:** what actually happened  
- **Environment:** OS, Python version, and GitStory commit hash
- **Screenshots:** Any screenshots or recordings of how GitStory looks like on your end will be much appreciated, if applicable!

Example:

```
Summary: gitstory run fails when executed outside a Git repository
Steps:
1. cd ~/Desktop
2. Run `gitstory run`
Expected: Prints “Not a valid Git repository.”
Actual: Displays a Python traceback.
Environment: macOS 14.4, Python 3.13
```

Each issue should describe only one problem. More detailed reporting instructions will be added once public testing begins.

---

## 8. Known Bugs and Limitations (updated November 24)

At this stage, any bugs that exist are currently being dealt with, seen in GitStory's Github Issues tab. Some current issues include:

| Area | Description | Status |
|------|--------------|--------|
| Build Packaging | GitStory currently runs from source; executable packaging planned. | Working on |
| Windows Setup Issues | Users on Windows run into small issues when setting up GitStory. | Working on |

This section will be updated as the project reaches the final version of GitStory and does further testing.

---

## 9. Contact

**GitStory Development Team**  
University of Washington — CSE 403  
GitHub Repository: [https://github.com/vinamra57/gitstory](https://github.com/vinamra57/gitstory)  
Discord: [https://discord.gg/4CXwpcWF](https://discord.gg/4CXwpcWF)

---

# GitStory User Guide



## 1. Overview

**GitStory** is a command-line tool designed to help developers quickly understand the history and structure of a software project by turning Git commit data into a readable “story.”  

Instead of sifting through long commit logs or complex branches, GitStory will summarize a repository’s evolution into clear, concise language.  

The goal is to help users—especially new team members or project managers—gain an understanding of a project’s development in minutes rather than hours.

### Key Intended Features
- **Repository Parsing Engine:** Extract commit messages, authors, timestamps, and branch data.  
- **Commit Grouping:** Cluster related commits (e.g., features, bug fixes, refactors).  
- **AI Summarization:** Use commit metadata to produce human-readable summaries.  
- **Command-Line Interface:** Run directly from the terminal with intuitive commands.  
- **Visualization Dashboard (planned):** Generate a static HTML dashboard showing project evolution.  
- **Time-Bound Summarization:** Filter summaries by date or development period.  

GitStory runs locally to maintain privacy and never sends source code outside the user’s environment.

---

## 2. Installation

### 2.1 Prerequisites

| Requirement | Version | Purpose |
|--------------|----------|----------|
| **Python** | 3.13 or newer | Core runtime environment |
| **Git** | Latest stable | Repository access |
| **UV** | Latest | Virtual environment and package management |

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

Then, install Python and create a virtual environment:
```bash
uv python install 3.13
uv venv
uv sync
```

This will install all necessary dependencies for development and testing.

---

## 3. Intended Functionality (Planned CLI Commands)

When development is complete, GitStory will run as a command-line tool from the terminal.  
Users will navigate to a Git repository and use the following commands to generate summaries or reports.

**UPDATES: to run GitStory, head over to [run-commands-guide.md](run-commands-guide.md) and run GitStory on your chosen Git Repo. The following instructions will work when the GitStory team is able get GitStory builds to work and run on their end.**

### 3.1 `gitstory run`
Generates a concise summary of the repository’s commit history on the current branch, highlighting major development events such as feature additions, bug fixes, and refactors.

### 3.2 `gitstory run --2w` (and other time filters)
Produces a summary limited to a specific time period. Planned flags include:
- `--5d` — last five days  
- `--2w` — last two weeks  
- `--1m` — last month  

Useful for reviewing progress during sprints or short development cycles.

### 3.3 `gitstory run --dashboard`
Creates a static HTML dashboard report containing:
- A timeline of key commits  
- Contributor statistics and activity charts  
- Summaries grouped by time period or feature area  

This report will be saved locally for offline viewing or sharing.

### 3.4 `gitstory compare <branch1> <branch2>`
Compares two branches and summarizes their key differences.  
Intended for understanding merge impacts before creating pull requests.

---

## 4. Using GitStory (Expected Workflow)

Once implemented, GitStory will follow this general workflow:

1. Navigate to a valid Git repository:
   ```bash
   cd path/to/repository
   ```

2. Run one of the supported commands (e.g., `gitstory run`).

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
| “Missing API key” | AI summarization key not configured | Add your key to a `.env` file or environment variable. |
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

As of this stage of development, GitStory’s core features are not yet implemented.  
Once development progresses, the team will use **GitHub Issues** to track bugs and feature requests.

For now, users and testers can report setup or documentation problems directly to the team (via Discord or class communication channels).

When GitStory’s issue tracker is active, a helpful bug report should include:

- **Summary:** short, specific title (e.g., `gitstory run --dashboard fails on Windows`)  
- **Steps to reproduce:** numbered actions to replicate the issue  
- **Expected result:** what should have happened  
- **Actual result:** what actually happened  
- **Environment:** OS, Python version, and GitStory commit hash  

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

## 8. Known Bugs and Limitations

At this stage, no bugs exist because GitStory’s functionality has not yet been implemented.  
However, several key features are planned and will be developed in upcoming iterations:

| Area | Description | Status |
|------|--------------|--------|
| Build Packaging | GitStory currently runs from source; executable packaging planned. | Planned |
| Visualization Dashboard | HTML report generation not yet implemented. | Planned |
| AI Summarization | Model integration under design; outputs unavailable. | Planned |
| API Rate Limits | Retry and backoff logic to be implemented. | Planned |

This section will be updated as the project reaches testing and beta release stages.

---

## 9. Contact

**GitStory Development Team**  
University of Washington — CSE 403  
GitHub Repository: [https://github.com/vinamra57/gitstory](https://github.com/vinamra57/gitstory)  
Discord: [https://discord.gg/4CXwpcWF](https://discord.gg/4CXwpcWF)

---

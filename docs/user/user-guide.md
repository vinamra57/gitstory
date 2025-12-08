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
| **Gemini API-Key** | Latest | Used in GitStory project, head over to [set-up-API_user.md](set-up-API_user.md) to obtain a Gemini API key.

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

After running the UV installer on your Windows PC, restart your PowerShell window OR run (this allows `uv` commands to be recognized):

```
$env:Path = "C:\Users<your-username>.local\bin;$env:Path"
```

## 2.4 Install Python and create a virtual environment 
Once you have installed `uv` on your PC, install Python and create a virtual environment. This will install all necessary dependencies for development and testing:
```bash
uv python install
--OR--
uv python install 3.13
```
```
uv venv
```
```
uv sync
```

---

## 3. Getting GitStory Build

Now that you have set all the dependencies up, head over to the [build-guide.md](https://github.com/vinamra57/gitstory/blob/main/docs/dev/build-guide.md) to create a GitStory build that you can use as a user!

---

## 4. Running GitStory!

When set-up is complete, GitStory will run as a command-line tool from the terminal: 

1. Navigate to a valid Git repository:
   ```bash
   cd path/to/repository
   ```

2. Run one of the supported commands, see [run-commands-guide.md](run-commands-guid.md) for more information on GitStory's commands.

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

## 8. Known Bugs and Limitations (updated December 7th)

At this stage, any bugs that exist are currently listed below and in GitStory's Github Issues tab. As of December 7th, GitStory has no bugs. Previously, we ran into issues such as GitStory not working on Windows or GitStory build not functioning, but we are happy to say these are now resolved!

| Area | Description | Status |
|------|--------------|--------|
|N/A|N/A|N/A|

---

## 9. Contact

**GitStory Development Team**  
University of Washington — CSE 403  
GitHub Repository: [https://github.com/vinamra57/gitstory](https://github.com/vinamra57/gitstory)  
Discord: [https://discord.gg/4CXwpcWF](https://discord.gg/4CXwpcWF)

---

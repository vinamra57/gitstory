# GitStory Commands Guide

This guide provides detailed examples and usage instructions for all GitStory commands.

## Prerequisites

Before using GitStory, ensure you have:

1. **Python 3.13+** installed
2. **GitStory repository cloned** to your local machine
3. **Dependencies installed** via `uv pip install -e .`
4. **Gemini API key configured** using the `key` command

## Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `run` | Generate summary for a branch | `python -m gitstory run ./ --branch=main` |
| `since` | Summary from time period | `python -m gitstory since ./ 2w` |
| `dashboard` | Generate HTML dashboard | `python -m gitstory dashboard ./` |
| `compare` | Compare two branches | `python -m gitstory compare ./ main feature` |
| `key` | Set API key | `python -m gitstory key --key="your_key"` |
| `parse-repo` | View raw commit data | `python -m gitstory parse-repo ./` |

---

## 1. Setting Your API Key

Before generating summaries, you must configure your Gemini API key.

### Get an API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key

### Set the Key

```bash
python -m gitstory key --key="AIzaSyC-EXAMPLE_API_KEY_HERE"
```

**Output:**
```
Welcome to GitStory: Turning git repos into readable stories

Key written to /path/to/gitstory/src/gitstory/data/key.txt!
```

The key is stored locally and used for all AI-powered summary generation.

---

## 2. Generate Repository Summary (`run`)

Creates an AI-powered summary of your repository's commit history.

### Basic Usage

```bash
python -m gitstory run ./ --branch=main
```

### Command Options

```
python -m gitstory run <repo_path> [OPTIONS]

Arguments:
  repo_path                  Path to the Git repository

Options:
  --branch TEXT             Branch to analyze (default: current branch)
  --since TEXT              Start time (ISO or relative like '2w')
  --until TEXT              End time (ISO or relative)
```

### Examples

**Analyze current branch:**
```bash
python -m gitstory run ./
```

**Analyze specific branch:**
```bash
python -m gitstory run ./ --branch=develop
```

**Analyze last 3 weeks on main:**
```bash
python -m gitstory run ./ --branch=main --since=3w
```

**Analyze specific date range:**
```bash
python -m gitstory run ./ --since=2025-01-01T00:00:00 --until=2025-01-15T00:00:00
```

### Sample Output

```
Welcome to GitStory: Turning git repos into readable stories

🔑 API key configured & loaded...
🔍 Analyzing repository...
🤖 Generating AI summary...
✅ Summary generation complete!

============================================================
• [FEATURE] User Authentication System (PR #42)
  - Implemented OAuth2 login flow in src/auth/oauth.py
  - Added JWT token management with 24-hour expiration
  - Created user session middleware for request validation

• [BUGFIX] Memory Leak in Data Processing (Issue #38)
  - Fixed unclosed database connections in src/db/connector.py
  - Reduced memory usage by 40% during bulk operations

• [REFACTOR] Database Schema Migration
  - Migrated from SQLite to PostgreSQL
  - Updated all ORM models in src/models/
  - Added migration scripts in db/migrations/
============================================================
```

---

## 3. Time-Based Summary (`since`)

Generates a summary of commits from a specific time period in the past.

### Basic Usage

```bash
python -m gitstory since ./ 2w
```

### Command Options

```
python -m gitstory since <repo_path> <time_period> [OPTIONS]

Arguments:
  repo_path                  Path to the Git repository
  time_period                Time period (Nd, Nw, Nm, Ny)

Options:
  --branch TEXT             Branch to analyze (default: current branch)
```

### Time Period Formats

- `Nd` — N days ago (e.g., `7d` = last 7 days)
- `Nw` — N weeks ago (e.g., `2w` = last 2 weeks)
- `Nm` — N months ago (e.g., `3m` = last 3 months)
- `Ny` — N years ago (e.g., `1y` = last year)

### Examples

**Last 5 days:**
```bash
python -m gitstory since ./ 5d
```

**Last 2 weeks on feature branch:**
```bash
python -m gitstory since ./ 2w --branch=feature/new-ui
```

**Last 6 months:**
```bash
python -m gitstory since ./ 6m
```

**Last year:**
```bash
python -m gitstory since ./ 1y
```

### Sample Output

```
Welcome to GitStory: Turning git repos into readable stories

🔑 API key configured & loaded...
🔍 Analyzing repository from 2w ago...
🤖 Generating AI summary...
✅ Summary generation complete!

============================================================
• [FEATURE] Dark Mode Support (PR #45)
  - Added theme switcher component in src/ui/ThemeToggle.tsx
  - Implemented CSS variables for dynamic theming
  - Updated all components to support dark mode

• [DOCS] API Documentation Update
  - Regenerated OpenAPI specs from code annotations
  - Added usage examples for all endpoints
  - Fixed broken links in README.md
============================================================
```

---

## 4. Generate Dashboard (`dashboard`)

Creates an interactive HTML dashboard with visualizations and AI summary.

### Basic Usage

```bash
python -m gitstory dashboard ./
```

### Command Options

```
python -m gitstory dashboard <repo_path>

Arguments:
  repo_path                  Path to the Git repository
```

### Example

```bash
python -m gitstory dashboard ./my-project
```

### Output

```
Welcome to GitStory: Turning git repos into readable stories

🔑 API key configured & loaded...
🔍 Analyzing repository...
🤖 Generating AI summary in Visualization Dashboard...
✅ Dashboard saved!
```

The dashboard is saved as `dashboard.html` in the current directory. Open it in any web browser to view:

- **Timeline visualization** of commits
- **Contributor statistics** and activity charts
- **AI-generated summary** grouped by commit type
- **File change metrics** and code churn analysis

---

## 5. Compare Branches (`compare`)

Compares two branches and generates an AI-powered summary of their differences.

### Basic Usage

```bash
python -m gitstory compare ./ main feature-branch
```

### Command Options

```
python -m gitstory compare <repo_path> <base_branch> <compare_branch> [OPTIONS]

Arguments:
  repo_path                  Path to the Git repository
  base_branch               Base branch name
  compare_branch            Branch to compare against base

Options:
  --since TEXT              Filter commits after this time
  --until TEXT              Filter commits before this time
  --context INTEGER         Number of context commits from merge base (default: 5)
```

### Examples

**Compare feature branch to main:**
```bash
python -m gitstory compare ./ main feature/new-api
```

**Compare with 10 context commits:**
```bash
python -m gitstory compare ./ main develop --context=10
```

**Compare recent changes only:**
```bash
python -m gitstory compare ./ main feature/ui --since=1w
```

### Sample Output

```
Welcome to GitStory: Turning git repos into readable stories

🔑 API key configured & loaded...
🔍 Comparing branches...
   Base: main (3 commits)
   Compare: feature/new-api (7 commits)
   Diverged: 5 days ago
🤖 Generating AI comparison summary...
✅ Comparison summary complete!

============================================================
### DIVERGENCE OVERVIEW

Branches diverged at commit abc1234 on 2025-01-20. The feature branch has
7 unique commits while main has 3 unique commits since divergence.

### KEY DIFFERENCES

• **Main Branch (3 commits):**
  - [BUGFIX] Fixed authentication timeout issue
  - [DOCS] Updated API documentation
  - [CHORE] Dependency version bumps

• **Feature Branch (7 commits):**
  - [FEATURE] New REST API endpoints for user management
  - [FEATURE] Added request validation middleware
  - [TEST] Comprehensive API endpoint tests
  - [REFACTOR] Reorganized API route handlers
  - [DOCS] API endpoint documentation
  - [FEATURE] Rate limiting for API calls
  - [BUGFIX] Fixed response serialization bug

### MERGE CONSIDERATIONS

• **Conflict Risk:** Medium - both branches modified src/api/routes.py
• **Recommendation:** Review route handler changes before merging
• **Test Coverage:** Feature branch adds 45 new tests
============================================================
```

---

## 6. Parse Repository (`parse-repo`)

Outputs raw structured commit data without AI summarization. Useful for debugging or custom analysis.

### Basic Usage

```bash
python -m gitstory parse-repo ./
```

### Command Options

```
python -m gitstory parse-repo <repo_path> [OPTIONS]

Arguments:
  repo_path                  Path to the Git repository

Options:
  --since TEXT              Start time (ISO or relative like '2w')
  --until TEXT              End time (ISO or relative)
  --branch TEXT             Branch to analyze (default: current branch)
```

### Example

```bash
python -m gitstory parse-repo ./ --branch=main --since=1w
```

### Sample Output

```
Summary Text:
## FEATURE COMMITS
- [abc1234] John Doe: Add user authentication
- [def5678] Jane Smith: Implement OAuth2 flow

## BUGFIX COMMITS
- [ghi9012] John Doe: Fix memory leak

Stats:
{'total_commits': 3, 'by_type': {'feature': 2, 'bugfix': 1}}

Metadata:
{'total_commits_analyzed': 3, 'commit_types_present': ['feature', 'bugfix']}
```

---

## Common Workflows

### Weekly Development Review

```bash
# Review last week's changes on main branch
python -m gitstory since ./ 1w --branch=main
```

### Pre-Merge Branch Comparison

```bash
# Compare feature branch before creating PR
python -m gitstory compare ./ main feature/my-feature
```

### Project Overview for New Team Members

```bash
# Generate comprehensive dashboard
python -m gitstory dashboard ./

# Generate 3-month summary
python -m gitstory since ./ 3m
```

### Sprint Summary

```bash
# Review last 2 weeks (typical sprint length)
python -m gitstory since ./ 2w
```

---

## Troubleshooting

### "Not a valid Git repository"

**Cause:** Running command outside a Git repository or path is incorrect.

**Solution:** Navigate to a valid Git repository or provide correct path.

```bash
cd /path/to/your/repo
python -m gitstory run ./
```

### "Error: cannot import name 'AISummarizer'"

**Cause:** Package not installed or installed incorrectly.

**Solution:** Reinstall the package:

```bash
uv pip install -e .
```

### "Missing API key"

**Cause:** Gemini API key not configured.

**Solution:** Set your API key:

```bash
python -m gitstory key --key="your_api_key_here"
```

### "Branch not found: feature-xyz"

**Cause:** Specified branch doesn't exist.

**Solution:** Check available branches:

```bash
git branch -a
```

Then use the correct branch name.

---

## Platform-Specific Notes

### macOS/Linux

Use `python3` or `python3.13` if `python` is not available:

```bash
python3 -m gitstory run ./
```

### Windows

Use `python` (not `python3`):

```bash
python -m gitstory run ./
```

If using PowerShell, ensure execution policy allows scripts:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Getting Help

View help for any command:

```bash
python -m gitstory --help
python -m gitstory run --help
python -m gitstory since --help
python -m gitstory compare --help
```

For bug reports or feature requests, visit:
[https://github.com/vinamra57/gitstory/issues](https://github.com/vinamra57/gitstory/issues)

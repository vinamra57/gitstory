"""Prompt engineering helpers for GitStory summaries."""

from __future__ import annotations

from typing import Dict


class PromptEngine:
    """Construct prompts for the Gemini model."""

    CLI_SYSTEM_PROMPT = """You are a technical code historian analyzing a git repository for developers.

OBJECTIVE: Create a fact-dense, actionable summary that helps developers understand what changed and why.

STRICT REQUIREMENTS:
1. Be specific: Name actual features, files, and modules - not "improvements" or "enhancements"
2. Include file paths when discussing changes (e.g., src/auth/jwt.py, tests/*)
3. Cite metrics when relevant (commit counts, contributors, line changes)
4. Focus on impact and implications, not just descriptions
5. Use technical terminology appropriately - your audience is developers
6. Highlight breaking changes, API changes, and migration needs prominently

FORBIDDEN - Never use vague phrases:
- "significant progress" / "various improvements" / "enhanced quality"
- "several commits" / "multiple changes" (be specific with numbers)
- "better performance" without metrics
- Generic statements without concrete examples

DATA INTERPRETATION GUIDE:
- feature commits: New functionality or capabilities
- bugfix commits: Stability and correctness improvements
- refactor commits: Code quality and maintainability work
- File paths reveal architecture (src/auth/* = authentication, src/api/* = API layer)
- High commit count in one area suggests focused development or instability
- Multiple contributors on same files indicates collaboration or complexity

OUTPUT FORMAT:
Write 5-7 bullet points in this structure:

[CATEGORY] Feature/Area Name (specifics)
- Key fact with context
- Impact or implication if significant

EXAMPLES OF GOOD BULLETS:
• [FEATURE] JWT Authentication System (src/auth/jwt.py, 12 commits)
  Replaced session-based auth with token system. Breaking change: all /api/* endpoints now require Authorization header.

• [BUGFIX] Login Race Condition (src/auth/login.py, 8 commits by Alice & Bob)
  Fixed intermittent 500 errors affecting login flow. Addressed concurrency issue in session handling.

• [REFACTOR] Test Suite Restructuring (tests/unit/*, tests/integration/*)
  Reorganized 45 test files into logical modules. Added pytest fixtures for common setup patterns.

EXAMPLES OF BAD BULLETS (Don't do this):
✗ The team made significant progress on authentication features with various improvements.
✗ Several commits focused on enhancing code quality and performance.
✗ Bug fixes were implemented to improve stability.

Now analyze the repository data below and create your summary:

IMPORTANT: End your summary with [END-SUMMARY] on a new line to indicate completion.
"""

    DASHBOARD_SYSTEM_PROMPT = """You are a technical project analyst creating a comprehensive repository report for multiple stakeholders (developers, managers, and contributors).

OBJECTIVE: Provide data-driven insights with narrative flow that helps stakeholders understand the project's evolution, health, and trajectory.

ANALYSIS FRAMEWORK - Address these questions:
1. WHAT changed? (features, fixes, refactors with file paths and scope)
2. WHY does it matter? (impact, risks, opportunities, implications)
3. WHO contributed? (team patterns, ownership areas, collaboration signals)
4. WHERE is development focused? (hot spots, architectural areas, trends)
5. TRAJECTORY? (what direction is the project heading, focus shifts over time)

QUALITY REQUIREMENTS:
- Support every claim with data: commit counts, file paths, contributor names, percentages
- Identify patterns and trends, not just list changes
- Call out risks: high churn areas, bug concentration, potential instability
- Highlight opportunities: under-developed areas, contribution gaps
- Use specific terminology: actual file paths, function names, module names
- Maintain narrative flow while being data-driven

FORBIDDEN PHRASES (never use these):
- "significant progress" / "various improvements" / "enhanced quality"
- "the team worked hard" / "great effort was made"
- "moving in the right direction" without specifics
- Any marketing language or generic praise without substance

TONE: Professional technical analysis, not marketing copy. Think senior engineer reviewing a project for leadership.

OUTPUT STRUCTURE:

# Repository Analysis

## Executive Summary
2-3 sentences capturing the most critical changes and their implications. Include key metrics (commit count, major features, primary focus area).

## Development Focus
What did the team prioritize? Use percentages and specifics.
- Example: "Primary focus on authentication system (35% of commits, src/auth/*) with secondary emphasis on API refactoring (20%, src/api/*)."
- Highlight any focus shifts over time period

## Major Technical Changes
3-5 significant changes with detail:
- Name the feature/change
- Specify affected files/modules
- Explain the technical approach or architecture
- Note any breaking changes or migration requirements
- Include commit count and contributors

## Code Health Signals
Analyze what the commit patterns reveal:
- Bug fix rate (what % of commits are fixes? Is this increasing/decreasing?)
- Refactoring activity (code quality investment)
- Test coverage signals (test file changes, new test patterns)
- Technical debt indicators (repeated fixes in same files)
- Hot spots (files with unusually high churn - potential risk areas)

## Team Dynamics
Contribution patterns and collaboration:
- Primary contributors with their focus areas
- Collaboration indicators (files with multiple authors)
- Knowledge distribution (is knowledge concentrated or spread?)
- Onboarding signals (new contributors and their initial areas)

## Forward-Looking Assessment
Based on the data, what are the implications?
- Areas needing attention (high bug concentration, under-tested modules)
- Architectural direction suggested by changes
- Potential bottlenecks or risk areas
- Recommendations for new contributors (where to start, what's active)

EXAMPLE OF GOOD ANALYSIS:
"Authentication system underwent major refactoring (src/auth/*, 23 commits by 3 developers). The shift from session-based to JWT tokens represents a breaking architectural change affecting all 15 API endpoints in src/api/routes/*. This concentrated development activity (35% of all commits) suggests this was the sprint's primary focus. Risk consideration: high churn in src/auth/jwt.py (8 revisions) may indicate complexity or evolving requirements."

EXAMPLE OF BAD ANALYSIS (Don't do this):
"The team made great progress on authentication features with various security improvements and enhancements to the overall system quality."

Now analyze the repository data below:

IMPORTANT: End your summary with [END-SUMMARY] on a new line to indicate completion.
"""

    def build_prompt(self, parsed_data: Dict, output_format: str) -> str:
        """Build a complete prompt for the requested output format."""
        system_prompt = (
            self.CLI_SYSTEM_PROMPT
            if output_format == "cli"
            else self.DASHBOARD_SYSTEM_PROMPT
        )
        data_section = self._format_data(parsed_data)
        return f"{system_prompt}\n\n{data_section}"

    def build_comparison_prompt(self, branch1_data: Dict, branch2_data: Dict) -> str:
        """Generate a prompt comparing two branches (stretch goal)."""
        return f"""Compare these two branches and highlight:
1. Unique commits in each branch
2. Key differences in functionality
3. Recommended merge strategy

BRANCH 1 DATA:
{self._format_data(branch1_data)}

BRANCH 2 DATA:
{self._format_data(branch2_data)}

Provide a clear comparison summary."""

    def _format_data(self, data: Dict) -> str:
        """Format repository data with rich context for LLM analysis."""
        sections = ["# REPOSITORY DATA\n"]
        stats = data.get("stats", {})
        commits = data.get("commits", [])

        # Enhanced overview statistics
        sections.append("## Overview Statistics")
        sections.append(f"- Total commits analyzed: {stats.get('total_commits', 0)}")
        sections.append(f"- Active contributors: {len(stats.get('by_author', {}))}")

        # Calculate total change magnitude
        total_changes = sum(c.get("changes", 0) for c in commits)
        if total_changes > 0:
            sections.append(f"- Total lines changed: {total_changes:,}")
            avg_change = total_changes / len(commits) if commits else 0
            sections.append(f"- Average commit size: {avg_change:.0f} lines")
        sections.append("")

        # Commit type distribution with percentages
        sections.append("## Commit Type Distribution")
        by_type = stats.get("by_type", {})
        total = stats.get("total_commits", 1)  # Avoid division by zero
        for commit_type, count in sorted(
            by_type.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / total * 100) if total > 0 else 0
            sections.append(f"- {commit_type}: {count} commits ({percentage:.1f}%)")
        sections.append("")

        # Top contributors with focus areas
        sections.append("## Top Contributors")
        by_author = stats.get("by_author", {})
        # Sort by commit count, show top 10
        sorted_authors = sorted(
            by_author.items(), key=lambda x: x[1]["count"], reverse=True
        )[:10]
        for author, author_data in sorted_authors:
            count = author_data["count"]
            percentage = (count / total * 100) if total > 0 else 0

            # Find primary focus area (commit type with most commits)
            types = author_data.get("types", {})
            if types:
                primary_type = max(types.items(), key=lambda x: x[1])
                focus = f"{primary_type[0]} ({primary_type[1]} commits)"
            else:
                focus = "mixed"

            sections.append(
                f"- {author}: {count} commits ({percentage:.1f}%) - Primary focus: {focus}"
            )
        sections.append("")

        # Detailed commit history by type
        sections.append("## Detailed Commit History")
        sections.append(data.get("summary_text", ""))

        return "\n".join(sections)

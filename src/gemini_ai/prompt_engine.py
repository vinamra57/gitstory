"""Prompt engineering helpers for GitStory summaries."""

from __future__ import annotations

from typing import Dict


class PromptEngine:
    """Construct prompts for the Gemini model."""

    CLI_SYSTEM_PROMPT = """You are a senior software engineer summarizing code history.
Create a concise, readable summary that helps developers quickly understand what happened.

RULES:
1. Focus on WHY changes were made, not just WHAT changed
2. Use past tense and active voice
3. Group related changes together
4. Highlight breaking changes or major refactors
5. Keep it under 500 words
6. Use bullet points for clarity
7. Avoid technical jargon unless necessary

FORMAT:
# Repository Summary

## Overview
[2-3 sentence high-level summary]

## Key Changes
[3-5 bullet points about major updates]

## Activity Breakdown
[Brief stats about commit types and contributors]
"""

    DASHBOARD_SYSTEM_PROMPT = """You are a senior software engineer creating a detailed code history report.
Generate a comprehensive narrative that will be displayed in an HTML dashboard.

RULES:
1. Write in sections with clear headers
2. Include specific examples and commit references
3. Explain the evolution and reasoning behind changes
4. Highlight patterns and trends
5. Make it engaging and story-like
6. Length: 800-1200 words

FORMAT:
# Project Evolution Story

## Executive Summary
[Paragraph overview]

## Feature Development
[Detailed narrative about features added]

## Bug Fixes & Stability
[Discussion of bug fixes and improvements]

## Code Quality & Refactoring
[Analysis of refactoring efforts]

## Team Contributions
[Breakdown of who did what]

## Recent Activity
[What's been happening lately]
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
        sections = ["# REPOSITORY DATA\n"]
        stats = data.get("stats", {})

        sections.append("## Statistics")
        sections.append(f"- Total commits: {stats.get('total_commits', 0)}")
        types = stats.get("by_type", {}).keys()
        sections.append(f"- Commit types: {', '.join(types) if types else 'n/a'}")
        sections.append(f"- Contributors: {len(stats.get('by_author', {}))}")
        sections.append("")

        sections.append("## Commit History")
        sections.append(data.get("summary_text", ""))

        return "\n".join(sections)

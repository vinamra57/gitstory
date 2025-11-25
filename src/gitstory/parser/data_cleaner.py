"""
Cleans and optimizes commit data for LLM processing.
Reduces token usage and improves summary quality.
"""

from typing import Dict, List


class DataCleaner:
    """Cleans and optimizes data for AI consumption."""

    MAX_MESSAGE_LENGTH = 200
    MAX_COMMITS_PER_GROUP = 50
    MAX_DIFF_CHUNK_SIZE = 2000

    def clean_data(self, grouped_data: Dict) -> Dict:
        cleaned_commits = []
        summary_chunks = []
        for commit_type, commits in grouped_data["grouped_commits"].items():
            if not commits:
                continue
            commits = commits[: self.MAX_COMMITS_PER_GROUP]
            for commit in commits:
                cleaned = self._clean_commit(commit, commit_type)
                cleaned_commits.append(cleaned)
            chunk = self._create_summary_chunk(commit_type, commits)
            summary_chunks.append(chunk)
        return {
            "commits": cleaned_commits,
            "summary_text": "\n\n".join(summary_chunks),
            "stats": grouped_data["stats"],
            "metadata": {
                "total_commits_analyzed": len(cleaned_commits),
                "commit_types_present": list(grouped_data["stats"]["by_type"].keys()),
            },
        }

    def _clean_commit(self, commit: Dict, commit_type: str) -> Dict:
        message = commit["message"]
        if len(message) > self.MAX_MESSAGE_LENGTH:
            message = message[: self.MAX_MESSAGE_LENGTH] + "..."
        # Chunk diff text
        diff_chunks = self._chunk_diff(commit.get("diff", ""))
        return {
            "hash": commit["hash"],
            "author": commit["author"],
            "timestamp": commit["timestamp"],
            "message": message,
            "type": commit_type,
            "files_changed": len(commit["files_changed"]),
            "changes": commit["insertions"] + commit["deletions"],
            "diff_chunks": diff_chunks,
        }

    def _chunk_diff(self, diff_text: str) -> List[str]:
        """Chunk large diff text into blocks for LLM token limits."""
        if not diff_text:
            return []
        return [
            diff_text[i : i + self.MAX_DIFF_CHUNK_SIZE]
            for i in range(0, len(diff_text), self.MAX_DIFF_CHUNK_SIZE)
        ]

    def _create_summary_chunk(self, commit_type: str, commits: List[Dict]) -> str:
        chunk = [f"## {commit_type.upper()} COMMITS ({len(commits)} total)"]
        for commit in commits[:10]:
            chunk.append(
                f"- [{commit['hash']}] {commit['author']}: {commit['message'][:100]}"
            )
        if len(commits) > 10:
            chunk.append(f"... and {len(commits) - 10} more {commit_type} commits")
        return "\n".join(chunk)

    def clean_comparison_data(self, comparison_data: Dict) -> Dict:
        """
        Clean and optimize branch comparison data for LLM processing.

        - Truncate messages to MAX_MESSAGE_LENGTH
        - Limit commits per branch to MAX_COMMITS_PER_GROUP
        - Create formatted summary text
        """
        base_commits = comparison_data["base_only_commits"][
            : self.MAX_COMMITS_PER_GROUP
        ]
        compare_commits = comparison_data["compare_only_commits"][
            : self.MAX_COMMITS_PER_GROUP
        ]
        context_commits = comparison_data["context_commits"]

        # Truncate commit messages
        for commit in base_commits + compare_commits + context_commits:
            if len(commit["message"]) > self.MAX_MESSAGE_LENGTH:
                commit["message"] = commit["message"][: self.MAX_MESSAGE_LENGTH] + "..."

        # Create summary text
        summary_text = self._create_comparison_summary_text(
            comparison_data["base_branch"],
            comparison_data["compare_branch"],
            comparison_data["merge_base"],
            base_commits,
            compare_commits,
            context_commits,
            comparison_data["divergence_metrics"],
            comparison_data["base_stats"],
            comparison_data["compare_stats"],
            comparison_data["file_analysis"],
        )

        return {
            **comparison_data,
            "base_only_commits": base_commits,
            "compare_only_commits": compare_commits,
            "context_commits": context_commits,
            "summary_text": summary_text,
        }

    def _create_comparison_summary_text(
        self,
        base_branch,
        compare_branch,
        merge_base,
        base_commits,
        compare_commits,
        context_commits,
        divergence_metrics,
        base_stats,
        compare_stats,
        file_analysis,
    ) -> str:
        """Create formatted summary text for LLM analysis."""
        text = f"""# BRANCH COMPARISON: {base_branch} vs {compare_branch}

## DIVERGENCE SUMMARY
Branches diverged at commit {merge_base["hash"]} ({merge_base["timestamp"]})
Time since divergence: {divergence_metrics["time_since_divergence"]}

{base_branch}: {divergence_metrics["base_commit_count"]} commits, {len(divergence_metrics["base_contributors"])} contributors
{compare_branch}: {divergence_metrics["compare_commit_count"]} commits, {len(divergence_metrics["compare_contributors"])} contributors

## COMMIT TYPE DISTRIBUTION
{base_branch}: {self._format_stats(base_stats)}
{compare_branch}: {self._format_stats(compare_stats)}

## FILE CHANGE ANALYSIS
Files changed ONLY in {base_branch}: {len(file_analysis["base_only_files"])} files
Files changed ONLY in {compare_branch}: {len(file_analysis["compare_only_files"])} files
Files changed in BOTH (conflict risk): {len(file_analysis["shared_files"])} files
{self._format_file_list(file_analysis["shared_files"][:10])}

## UNIQUE COMMITS - {base_branch.upper()} ({len(base_commits)} commits)
{self._format_commits_by_type(base_commits, base_stats)}

## UNIQUE COMMITS - {compare_branch.upper()} ({len(compare_commits)} commits)
{self._format_commits_by_type(compare_commits, compare_stats)}

## SHARED CONTEXT ({len(context_commits)} recent commits from merge base)
{self._format_commit_list(context_commits)}
"""
        return text

    def _format_stats(self, stats: Dict) -> str:
        """Format commit type statistics."""
        by_type = stats.get("by_type", {})
        if not by_type:
            return "No commits"
        parts = []
        for commit_type, count in sorted(
            by_type.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (
                (count / stats["total_commits"] * 100)
                if stats["total_commits"] > 0
                else 0
            )
            parts.append(f"{commit_type} {count} ({percentage:.0f}%)")
        return ", ".join(parts)

    def _format_file_list(self, files: List[str]) -> str:
        """Format a list of files."""
        if not files:
            return "None"
        return "\n".join(f"  - {f}" for f in files)

    def _format_commits_by_type(self, commits: List[Dict], stats: Dict) -> str:
        """Format commits grouped by type."""
        if not commits:
            return "No commits"

        # Group commits by type (manually since we don't have grouped data here)
        by_type = {}
        for commit in commits:
            # Infer type from stats or classify
            commit_type = "other"  # Default
            by_type.setdefault(commit_type, []).append(commit)

        lines = []
        for commit_type, type_commits in sorted(by_type.items()):
            lines.append(f"### {commit_type.upper()} ({len(type_commits)} commits)")
            for commit in type_commits[:5]:  # Show max 5 per type
                lines.append(
                    f"- [{commit['hash']}] {commit['author']}: {commit['message'][:80]}"
                )
            if len(type_commits) > 5:
                lines.append(f"... and {len(type_commits) - 5} more")

        return "\n".join(lines)

    def _format_commit_list(self, commits: List[Dict]) -> str:
        """Format a simple list of commits."""
        if not commits:
            return "No commits"
        lines = []
        for commit in commits[:10]:  # Show max 10
            lines.append(
                f"- [{commit['hash']}] {commit['author']}: {commit['message'][:80]}"
            )
        if len(commits) > 10:
            lines.append(f"... and {len(commits) - 10} more")
        return "\n".join(lines)

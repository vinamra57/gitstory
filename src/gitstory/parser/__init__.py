"""
Repository parser package.
Exports the main RepoParser class for external use.
"""

from .git_extractor import GitExtractor
from .commit_grouper import CommitGrouper
from .data_cleaner import DataCleaner
from .branch_comparator import BranchComparator
from .validation import (
    validate_commits,
    validate_grouped_data,
    validate_cleaned_data,
    ValidationError,
    ValidationReport,
)


class RepoParser:
    """Main interface for repository parsing."""

    def __init__(self, repo_path: str, on_validation_error: str = "raise"):
        self.extractor = GitExtractor(repo_path)
        self.grouper = CommitGrouper()
        self.cleaner = DataCleaner()
        self.comparator = BranchComparator(self.grouper)
        self.validation_report = ValidationReport()
        # Policy: 'raise' (default) or 'fallback' to attempt best-effort outputs
        self.on_validation_error = on_validation_error

    def parse(self, since: str = None, until: str = None, branch: str = None):
        """
        Parse repository and return structured data with validation.
        Gracefully handles bad commits by skipping them and continuing.
        """
        try:
            # Stage 1: Extract commits
            raw_commits = self.extractor.get_commits(since, until, branch)
            
            # Validate and sanitize commits
            validated_commits = validate_commits(raw_commits, self.validation_report)
            
            if not validated_commits:
                msg = "No valid commits found after validation"
                err = ValidationError(msg)
                # attach a snapshot of the validation report for callers
                err.report = self.validation_report.to_dict()
                err.stage = "commits"
                raise err
            
            # Stage 2: Group commits
            grouped = self.grouper.group_commits(validated_commits)
            is_valid, error_msg = validate_grouped_data(grouped)
            if not is_valid:
                msg = f"Grouper output validation failed: {error_msg}"
                # If configured to fallback, construct a minimal per-commit grouping and continue
                if self.on_validation_error == "fallback":
                    self.validation_report.add_warning(msg + " — falling back to per-commit grouping")
                    fallback_grouped = {
                        "grouped_commits": {c["hash"]: [c] for c in validated_commits},
                        "stats": {"groups": len(validated_commits)},
                    }
                    grouped = fallback_grouped
                else:
                    err = ValidationError(msg)
                    err.report = self.validation_report.to_dict()
                    err.stage = "grouper"
                    raise err
            
            # Stage 3: Clean data
            cleaned = self.cleaner.clean_data(grouped)
            is_valid, error_msg = validate_cleaned_data(cleaned)
            if not is_valid:
                msg = f"Cleaner output validation failed: {error_msg}"
                if self.on_validation_error == "fallback":
                    self.validation_report.add_warning(msg + " — returning partial cleaned data")
                    partial = {
                        "commits": validated_commits,
                        "summary_text": "Partial summary (cleaner validation failed)",
                        "stats": {},
                        "metadata": {"validation_report": self.validation_report.to_dict()},
                    }
                    return partial
                err = ValidationError(msg)
                err.report = self.validation_report.to_dict()
                err.stage = "cleaner"
                raise err
            
            # Attach validation report to metadata
            if 'metadata' not in cleaned:
                cleaned['metadata'] = {}
            cleaned['metadata']['validation_report'] = self.validation_report.to_dict()
            
            return cleaned
            
        except ValidationError as e:
            # Preserve report and stage if provided
            new_msg = f"Pipeline validation error: {str(e)}"
            new_err = ValidationError(new_msg)
            if hasattr(e, "report"):
                new_err.report = e.report
            if hasattr(e, "stage"):
                new_err.stage = e.stage
            raise new_err

    def compare(
        self,
        base_branch: str,
        compare_branch: str,
        since: str = None,
        until: str = None,
        context_commits: int = 5,
    ):
        """
        Compare two branches and return structured comparison data.

        Pipeline: Extract → Process → Clean
        """
        # 1. Extract raw comparison data from Git
        raw_comparison = self.extractor.compare_branches(
            base_branch, compare_branch, since, until, context_commits
        )

        # Lightweight validation for compare() input to avoid obscure errors
        required_comp_keys = [
            "base_only_commits",
            "compare_only_commits",
            "context_commits",
            "merge_base",
            "base_branch",
            "compare_branch",
        ]

        missing = [k for k in required_comp_keys if k not in raw_comparison]
        if missing:
            err = ValidationError(f"compare_branches output missing keys: {missing}")
            err.report = self.validation_report.to_dict()
            err.stage = "compare"
            raise err

        # Basic type checks
        if not isinstance(raw_comparison.get("base_only_commits"), list) or not isinstance(
            raw_comparison.get("compare_only_commits"), list
        ):
            err = ValidationError("compare_branches expected lists for base/compare commits")
            err.report = self.validation_report.to_dict()
            err.stage = "compare"
            raise err

        # 2. Process comparison (calculate metrics, classify, analyze)
        processed = self.comparator.process_comparison(
            base_commits=raw_comparison["base_only_commits"],
            compare_commits=raw_comparison["compare_only_commits"],
            context_commits=raw_comparison["context_commits"],
            merge_base=raw_comparison["merge_base"],
            base_branch_name=raw_comparison["base_branch"],
            compare_branch_name=raw_comparison["compare_branch"],
        )

        # 3. Clean and optimize for LLM
        cleaned = self.cleaner.clean_comparison_data(processed)

        return cleaned


__all__ = ["RepoParser"]

"""
HTML dashboard generator (stub implementation).
This is a placeholder for Ian's dashboard implementation.
"""
from pathlib import Path
from typing import Dict


class DashboardGenerator:
    """Generates HTML dashboard from repository data (STUB - Ian's module)."""

    def __init__(self):
        """Initialize dashboard generator."""
        pass

    def generate(self, parsed_data: Dict, ai_summary: str,
                 output_path: str = 'gitstory-report.html') -> str:
        """
        Generate HTML dashboard.

        Args:
            parsed_data: Output from RepoParser (includes commits and stats)
            ai_summary: AI-generated summary from AISummarizer
            output_path: Where to save the HTML file

        Returns:
            Path to generated HTML file

        NOTE: This is a STUB implementation for integration testing.
        Ian will implement the actual HTML generation with visualizations.
        """
        # For now, create a simple HTML file
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>GitStory Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
        h1 {{ color: #333; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        .stats {{ background: #e8f4f8; padding: 15px; margin: 20px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>📖 GitStory Repository Report</h1>
    <div class="stats">
        <h2>Statistics</h2>
        <p>Total Commits: {parsed_data['stats']['total_commits']}</p>
        <p>Contributors: {len(parsed_data['stats']['by_author'])}</p>
    </div>
    <h2>AI-Generated Summary</h2>
    <pre>{ai_summary}</pre>
    <hr>
    <p><em>This is a stub dashboard. Ian will implement the full visualization with charts and interactive elements.</em></p>
</body>
</html>"""

        # Write to file
        with open(output_path, 'w') as f:
            f.write(html_content)

        return str(Path(output_path).absolute())

import os
import markdown
import shutil

# Jinja allows dyanmic variable reassignment for static HTML files
from jinja2 import Environment, FileSystemLoader

# These take the current path to this folder, and appends "templates"
CURR_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(CURR_DIR, "templates")

# This creates a Jinja2 object which stores & manages templates
# We tell it to look for templates inside the folder specific in the TEMPLATE_DIR path
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def generate_dashboard(
    repo_data: dict, ai_summary: dict, repo_path: str, output_file="dashboard.html"
):
    # Here dict is basically to specify that it should be a JSON
    # These take the current path to this folder, and appends "output"

    OUTPUT_DIR = os.path.join(repo_path, "output")
    # This goes to the OUTPUT_DIR path and adds an output folder if it doesnt exist yet
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # We fetch the specified template first through the Jinja2 object
    template = env.get_template("dashboard_template.html")

    html_summary = markdown.markdown(ai_summary.get("summary", ""))

    # We render the specified template with these paramaters
    html_content = template.render(
        commits=repo_data.get("commits", []),
        stats=repo_data.get("stats", {}),
        ai_summary={
            "summary": html_summary,
            "metadata": ai_summary.get("metadata", {}),
        },
    )

    css_source = os.path.join(CURR_DIR, "static", "styles.css")  # adjust if needed
    css_dest = os.path.join(OUTPUT_DIR, "styles.css")
    shutil.copyfile(css_source, css_dest)

    js_source = os.path.join(CURR_DIR, "static", "script.js")
    js_dest = os.path.join(OUTPUT_DIR, "script.js")
    shutil.copyfile(js_source, js_dest)

    # We append the output file to the OUTPUT_DIR path
    output_path = os.path.join(OUTPUT_DIR, output_file)

    # We write the html contents into the output file
    #'with ... as f' makes it so that it closes the file automatically over having to do f.close()
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(html_content)

    print(f"Dashboard generated: {os.path.abspath(output_path)}")

    # Didn't return output_path, since it would be hard to write tests for this
    # Might change this later, @Ian
    # return output_path

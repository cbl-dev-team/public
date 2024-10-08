import requests
import os

ORG_NAME = 'cbl-dev-team'
REPOSITORIES = ['cbl-v2', 'CBL-LiveScoring', 'cbl-backend']
GITHUB_TOKEN = os.getenv('ACCESS_TOKEN_GIT')
OUTPUT_FILE = 'docs/index.html'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def fetch_open_issues(org, repo):
    url = f'https://api.github.com/repos/{org}/{repo}/issues?state=open'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch issues for {repo}: {response.status_code}")
        return []

def generate_html(issues_by_repo):
    # Add some basic CSS for styling
    html_content = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
            }
            h1 {
                color: #333;
            }
            h2 {
                color: #555;
                margin-top: 30px;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin-bottom: 10px;
            }
            a {
                text-decoration: none;
                color: #0073e6;
            }
            a:hover {
                text-decoration: underline;
            }
            .label {
                font-weight: bold;
                padding: 2px 5px;
                border-radius: 3px;
                margin-right: 10px;
            }
            .high-priority {
                background-color: #ff4d4d;
                color: white;
            }
            .medium-priority {
                background-color: #ffa500;
                color: white;
            }
            .low-priority {
                background-color: #4CAF50;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>Open Issues</h1>
    """

    for repo, issues in issues_by_repo.items():
        html_content += f"<h2>{repo}</h2><ul>"
        
        if issues:
            for issue in issues:
                # Check if any labels are related to priority
                labels = issue.get("labels", [])
                label_text = ""
                
                # Check for specific priority labels
                for label in labels:
                    if label["name"].lower() == "high-priority":
                        label_text = '<span class="label high-priority">[High Priority]</span>'
                    elif label["name"].lower() == "medium-priority":
                        label_text = '<span class="label medium-priority">[Medium Priority]</span>'
                    elif label["name"].lower() == "low-priority":
                        label_text = '<span class="label low-priority">[Low Priority]</span>'
                
                html_content += f'<li>{label_text}<a href="{issue["html_url"]}">{issue["title"]}</a></li>'
        else:
            html_content += "<li>No open issues</li>"
        
        html_content += "</ul>"

    html_content += """
    </body>
    </html>
    """

    return html_content

def main():
    issues_by_repo = {}
    for repo in REPOSITORIES:
        issues = fetch_open_issues(ORG_NAME, repo)
        issues_by_repo[repo] = issues

    html_content = generate_html(issues_by_repo)

    # Write HTML content to index.html in the docs folder
    with open(OUTPUT_FILE, 'w') as f:
        f.write(html_content)
    print(f"Generated {OUTPUT_FILE} with open issues.")

if __name__ == "__main__":
    main()

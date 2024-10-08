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
    html_content = """<html><body><h1>Open Issues</h1><ul>"""
    for repo, issues in issues_by_repo.items():
        html_content += f"<h2>{repo}</h2><ul>"
        for issue in issues:
            html_content += f'<li><a href="{issue["html_url"]}">{issue["title"]}</a></li>'
        html_content += "</ul>"
    html_content += "</ul></body></html>"
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

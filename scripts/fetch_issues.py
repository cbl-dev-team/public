import requests
import os

ORG_NAME = 'cbl-dev-team'
REPOSITORIES = ['cbl-web-app', 'cbl-mobile-app', 'cbl-backend']
GITHUB_TOKEN = os.getenv('ACCESS_TOKEN_GIT')
OUTPUT_FILE = 'docs/index.html'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def fetch_open_issues(org, repo):
    issues = []
    page = 1
    while True:
        url = f'https://api.github.com/repos/{org}/{repo}/issues?state=open&per_page=100&page={page}'
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch issues for {repo}: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        
        filtered_issues = [issue for issue in data if "pull_request" not in issue]
        issues.extend(filtered_issues)
        page += 1
    
    return issues

def generate_html(issues_by_repo):

    # Mapping for username substitutions
    name_mapping = {
        "ha22001872": "Hafiz (Dev)",
        "mrafsyam": "Raf (Dev)",
        "aqhareus": "Aqhar (Dev)",
        "Mazri02": "Azri (Dev)",
        "hafyze": "Zul (Dev)",
        "HaziqAS": "Haziq Anaki (QA / Project Manager)"
    }

    assignees_set = set()
    
    # Helper function to determine issue priority value
    # Assigns a numeric value to each priority label:
    #   1 for "high-priority", 2 for "medium-priority", 3 for "low-priority"
    # If none of these labels exist, returns 4 so the issue is sorted last.
    def get_priority(issue):
        priority_map = {
            "high-priority": 1,
            "medium-priority": 2,
            "low-priority": 3
        }
        # Get all priorities from the issue's labels, defaulting to 4 if no match is found
        priorities = [priority_map.get(label["name"].lower(), 4) for label in issue.get("labels", [])]
        return min(priorities) if priorities else 4

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
            ol {
                padding-left: 20px;
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
            .assignees {
                font-weight: bold;
                padding: 2px 5px;
                border-radius: 3px;
                margin-right: 10px;
                background-color: #3f8df2;
                color: white;
            }
            /* New style for status labels */
            .status-label {
                background-color: #2196F3;
                color: white;
            }
        </style>
        <script>
            function filterIssues() {
                let selectedAssignee = document.getElementById("assigneeFilter").value;
                let issues = document.querySelectorAll(".issue-item");
                
                issues.forEach(issue => {
                    let assignee = issue.getAttribute("data-assignee");
                    if (selectedAssignee === "all" || assignee.includes(selectedAssignee)) {
                        issue.style.display = "block";
                    } else {
                        issue.style.display = "none";
                    }
                });
            }
        </script>
    </head>
    <body>
        <h1>CBL Project - Open Issues</h1>
        <label for="assigneeFilter">Filter by Assignee: </label>
        <select id="assigneeFilter" onchange="filterIssues()">
            <option value="all">All</option>
    """
    
    for repo, issues in issues_by_repo.items():
        for issue in issues:
            assignees = issue.get("assignees", [])
            assignee_names = ", ".join([assignee["login"] for assignee in assignees])
            if assignee_names:
                assignees_set.update([assignee["login"] for assignee in assignees])

    for assignee in sorted(assignees_set):
        html_content += f'<option value="{assignee}">{assignee}</option>'
    
    html_content += """
        </select>
        <br><br>
    """
    
    for repo, issues in issues_by_repo.items():
        # Sort issues by the determined priority using get_priority
        sorted_issues = sorted(issues, key=get_priority)
        html_content += f"<h2>{repo}</h2><ol>"
        
        for issue in sorted_issues:
            issue_number = issue.get("number", "")
            labels = issue.get("labels", [])

            # We'll collect both priority labels and status labels
            # into a list, then join them into label_text.
            label_html_list = []
            for label in labels:
                label_lower = label["name"].lower()
                
                # Keep existing priority logic
                if label_lower == "high-priority":
                    label_html_list.append('<span class="label high-priority">[High Priority]</span>')
                elif label_lower == "medium-priority":
                    label_html_list.append('<span class="label medium-priority">[Medium Priority]</span>')
                elif label_lower == "low-priority":
                    label_html_list.append('<span class="label low-priority">[Low Priority]</span>')
                
                # Add status label if it starts with "status : "
                elif label_lower.startswith("status : "):
                    # Display the full label name as-is
                    label_html_list.append(f'<span class="label status-label">{label["name"]}</span>')

            # Join all collected label HTML fragments
            label_text = " ".join(label_html_list)

            assignees = issue.get("assignees", [])

            # Replace usernames based on mapping
            assignee_names = ", ".join(
                [name_mapping.get(assignee["login"], assignee["login"]) for assignee in assignees]
            )
        
            html_content += f'<li class="issue-item" data-assignee="{assignee_names}">{label_text} <a href="{issue["html_url"]}">#{issue_number} {issue["title"]}</a> - {assignee_names}</li>'
        
        html_content += "</ol>"
    
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

    with open(OUTPUT_FILE, 'w') as f:
        f.write(html_content)
    print(f"Generated {OUTPUT_FILE} with open issues.")

if __name__ == "__main__":
    main()

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
        .bug-label {
            font-weight: bold;
            padding: 2px 5px;
            border-radius: 3px;
            margin-right: 10px;
            background-color: #ff4d4d;
            color: white;
        }
        .task-label {
            font-weight: bold;
            padding: 2px 5px;
            border-radius: 3px;
            margin-right: 10px;
            background-color: #4CAF50;
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
        <script>
            let assigneesSet = new Set();
        </script>
        <!-- Dynamic Assignee Options Will be Inserted Here -->
    </select>
    <br><br>
    
    %s
</body>
</html>

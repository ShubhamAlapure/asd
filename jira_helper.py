#!/usr/bin/env python3
"""
Jira helper script to interact with Jira REST API.
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.parse
import urllib.error

def load_env(filepath=".env"):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip("\"'")

load_env()

EMAIL = os.environ.get("JIRA_EMAIL")
TOKEN = os.environ.get("JIRA_API_TOKEN")
BASE_URL = os.environ.get("JIRA_BASE_URL", "").rstrip("/")

if not EMAIL or not TOKEN or not BASE_URL:
    print("Error: Missing JIRA_EMAIL, JIRA_API_TOKEN, or JIRA_BASE_URL in .env", file=sys.stderr)
    sys.exit(1)

AUTH_HEADER = "Basic " + base64.b64encode(f"{EMAIL}:{TOKEN}".encode()).decode()

def request(path, method="GET", body=None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", AUTH_HEADER)
    req.add_header("Accept", "application/json")
    if body:
        req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            if not content:
                return {}
            return json.loads(content)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"HTTPError {e.code} on {method} {path}: {err_msg}", file=sys.stderr)
        raise

def get_myself():
    return request("/rest/api/3/myself")

def list_projects():
    return request("/rest/api/3/project")

def create_project(name, key, template="com.pyxis.greenhopper.jira:gh-simplified-agility-scrum"):
    myself = get_myself()
    body = {
        "key": key,
        "name": name,
        "projectTypeKey": "software",
        "projectTemplateKey": template,
        "leadAccountId": myself.get("accountId")
    }
    return request("/rest/api/3/project", method="POST", body=body)

def create_issue(project_key, summary, description="", issuetype="Task", extra_fields=None):
    myself = get_myself()
    # Find issue type id
    proj = request(f"/rest/api/3/project/{project_key}")
    issue_type_id = None
    for it in proj.get("issueTypes", []):
        if it.get("name").lower() == issuetype.lower():
            issue_type_id = it.get("id")
            break
    if not issue_type_id and proj.get("issueTypes"):
        issue_type_id = proj["issueTypes"][0]["id"]

    body = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"id": issue_type_id} if issue_type_id else {"name": issuetype},
            "assignee": {"accountId": myself.get("accountId")}
        }
    }
    if description:
        body["fields"]["description"] = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": description}]
                }
            ]
        }
    if extra_fields:
        body["fields"].update(extra_fields)
    return request("/rest/api/3/issue", method="POST", body=body)

def search_issues(jql="", max_results=50, fields=None):
    if fields is None:
        fields = ["summary", "status", "assignee", "issuetype", "priority", "description", "created", "updated"]
    params = {"maxResults": max_results, "fields": ",".join(fields)}
    if jql:
        params["jql"] = jql
    query = urllib.parse.urlencode(params)
    return request(f"/rest/api/3/search/jql?{query}")

def get_issue(issue_id_or_key):
    return request(f"/rest/api/3/issue/{issue_id_or_key}")

def get_transitions(issue_id_or_key):
    return request(f"/rest/api/3/issue/{issue_id_or_key}/transitions")

def transition_issue(issue_id_or_key, transition_id):
    body = {"transition": {"id": transition_id}}
    return request(f"/rest/api/3/issue/{issue_id_or_key}/transitions", method="POST", body=body)

def add_comment(issue_id_or_key, text):
    # Jira Cloud v3 uses Atlassian Document Format (ADF) for comments
    body = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        }
    }
    return request(f"/rest/api/3/issue/{issue_id_or_key}/comment", method="POST", body=body)

def extract_text_from_adf(node):
    if not isinstance(node, dict):
        return str(node or "")
    text = ""
    if node.get("type") == "text":
        text += node.get("text", "")
    for child in node.get("content", []):
        text += extract_text_from_adf(child)
    if node.get("type") in ("paragraph", "heading", "bulletList", "listItem"):
        text += "\n"
    return text

def print_issue_details(iss):
    f = iss.get("fields", {})
    key = iss.get("key", iss.get("id"))
    summary = f.get("summary")
    itype = f.get("issuetype", {}).get("name")
    status = f.get("status", {}).get("name")
    assignee = f.get("assignee")
    assignee_name = assignee.get("displayName") if assignee else "Unassigned"
    desc = f.get("description")
    desc_str = extract_text_from_adf(desc).strip() if desc else "(No description)"
    
    print("=" * 60)
    print(f"[{key}] {summary}")
    print(f"Type: {itype} | Status: {status} | Assignee: {assignee_name}")
    print("Description:")
    print(desc_str)
    print("=" * 60)

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if action == "projects":
        projects = list_projects()
        print(f"Total Projects: {len(projects)}")
        for p in projects:
            print(f"- [{p.get('key')}] {p.get('name')} (id: {p.get('id')})")
            
    elif action == "list":
        jql = sys.argv[2] if len(sys.argv) > 2 else "order by updated DESC"
        results = search_issues(jql=jql)
        issues = results.get("issues", [])
        print(f"Found {len(issues)} issues:")
        for iss in issues:
            key = iss.get("key")
            fields = iss.get("fields", {})
            summary = fields.get("summary")
            status = fields.get("status", {}).get("name")
            assignee = fields.get("assignee")
            assignee_name = assignee.get("displayName") if assignee else "Unassigned"
            issuetype = fields.get("issuetype", {}).get("name")
            print(f"[{key}] ({issuetype} | {status}) {summary} -> {assignee_name}")
            
    elif action == "get":
        if len(sys.argv) < 3:
            print("Usage: jira_helper.py get <issue_key>")
            sys.exit(1)
        key = sys.argv[2]
        iss = get_issue(key)
        print_issue_details(iss)

    elif action == "all_details":
        jql = sys.argv[2] if len(sys.argv) > 2 else "project = SCRUM"
        results = search_issues(jql=jql)
        for iss in results.get("issues", []):
            full_iss = get_issue(iss.get("key", iss.get("id")))
            print_issue_details(full_iss)
        
    elif action == "transitions":
        if len(sys.argv) < 3:
            print("Usage: jira_helper.py transitions <issue_key>")
            sys.exit(1)
        key = sys.argv[2]
        trans = get_transitions(key)
        print(f"Available transitions for {key}:")
        for t in trans.get("transitions", []):
            print(f"- ID: {t.get('id')}: {t.get('name')} -> {t.get('to', {}).get('name')}")

    else:
        print(f"Unknown action: {action}")

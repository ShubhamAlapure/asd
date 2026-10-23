import jira_helper

print("=== VERIFYING MBAJ2 IN JIRA ===")
issues = jira_helper.search_issues("project = MBAJ2", max_results=100)
all_issues = issues.get("issues", [])
print(f"Total issues found in MBAJ2: {len(all_issues)}")

type_counts = {}
for iss in all_issues:
    t = iss.get("fields", {}).get("issuetype", {}).get("name")
    type_counts[t] = type_counts.get(t, 0) + 1
print("Counts by type:", type_counts)

sprints = jira_helper.request("/rest/agile/1.0/board/35/sprint")
print("\nSprints:")
for s in sprints.get("values", []):
    sid = s["id"]
    sname = s["name"]
    sstate = s["state"]
    sgoal = s.get("goal")
    s_issues = jira_helper.request(f"/rest/agile/1.0/sprint/{sid}/issue?fields=summary,customfield_10016")
    issues_list = s_issues.get("issues", [])
    total_pts = sum(i.get("fields", {}).get("customfield_10016", 0) or 0 for i in issues_list)
    print(f"  * [{sid}] {sname} (State: {sstate}) - {len(issues_list)} issues, {total_pts} story points")
    print(f"    Goal: {sgoal}")

board = jira_helper.request("/rest/agile/1.0/board/35")
print("\nBoard:", board.get("name"), f"(ID: {board.get('id')})")

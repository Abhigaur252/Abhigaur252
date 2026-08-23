import json
import re
import urllib.request
from datetime import datetime, timezone

USERNAME = "Abhigaur252"
README_PATH = "README.md"

QUOTES = [
    "“First, solve the problem. Then, write the code.” — John Johnson",
    "“Experience is the name everyone gives to their mistakes.” — Oscar Wilde",
    "“In order to be irreplaceable, one must always be different.” — Coco Chanel",
    "“Java is to JavaScript what car is to carpet.” — Chris Heilmann",
    "“Knowledge is power.” — Francis Bacon",
    "“Code is like humor. When you have to explain it, it’s bad.” — Cory House",
    "“Simplicity is the soul of efficiency.” — Austin Freeman",
    "“Make it work, make it right, make it fast.” — Kent Beck",
    "“Fix the cause, not the symptom.” — Steve Maguire",
    "“Optimism is an occupational hazard of programming: feedback is the treatment.” — Kent Beck"
]

def fetch_github_events():
    url = f"https://api.github.com/users/{USERNAME}/events/public"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Python-Urllib-Script"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = response.read().decode("utf-8")
                return json.loads(data)
    except Exception as e:
        print(f"Error fetching GitHub events: {e}")
    return []

def format_activity(events):
    activity_items = []
    seen = set()

    for event in events:
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name", "")
        repo_url = f"https://github.com/{repo_name}"
        repo_basename = repo_name.split("/")[-1] if "/" in repo_name else repo_name

        if not repo_name or repo_name in seen:
            continue

        if event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            msg = commits[0]["message"].split("\n")[0] if commits else "Pushed commits"
            activity_items.append(f"📌 Pushed to [{repo_basename}]({repo_url}): *{msg}*")
            seen.add(repo_name)
        elif event_type == "CreateEvent":
            ref_type = event.get("payload", {}).get("ref_type", "repository")
            activity_items.append(f"✨ Created {ref_type} [{repo_basename}]({repo_url})")
            seen.add(repo_name)
        elif event_type == "WatchEvent":
            activity_items.append(f"⭐ Starred [{repo_basename}]({repo_url})")
            seen.add(repo_name)
        elif event_type == "PullRequestEvent":
            action = event.get("payload", {}).get("action", "")
            pr = event.get("payload", {}).get("pull_request", {})
            title = pr.get("title", "")
            activity_items.append(f"🔀 {action.capitalize()} PR in [{repo_basename}]({repo_url}): *{title}*")
            seen.add(repo_name)
        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action", "")
            issue = event.get("payload", {}).get("issue", {})
            title = issue.get("title", "")
            activity_items.append(f"❓ {action.capitalize()} issue in [{repo_basename}]({repo_url}): *{title}*")
            seen.add(repo_name)

        if len(activity_items) >= 5:
            break

    if not activity_items:
        activity_items = [
            "🚀 Building cool projects & pushing code to GitHub!",
            "⚙️ Working on full-stack web apps, Java backends, and AI models."
        ]

    return "\n".join([f"- {item}" for item in activity_items])

def get_random_quote():
    import random
    return random.choice(QUOTES)

def replace_section(content, section_name, new_content):
    start_tag = f"<!-- START_SECTION:{section_name} -->"
    end_tag = f"<!-- END_SECTION:{section_name} -->"
    pattern = re.compile(f"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
    replacement = f"{start_tag}\n{new_content}\n{end_tag}"
    return pattern.sub(replacement, content)

def update_readme():
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {README_PATH} not found.")
        return

    events = fetch_github_events()
    activity_md = format_activity(events)
    quote_md = f"> {get_random_quote()}"
    timestamp_md = f"⚡ *Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC*"

    content = replace_section(content, "activity", activity_md)
    content = replace_section(content, "quote", quote_md)
    content = replace_section(content, "updated_at", timestamp_md)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("README.md updated successfully!")

if __name__ == "__main__":
    update_readme()

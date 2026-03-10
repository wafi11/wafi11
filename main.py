import requests
import os
import re
from datetime import datetime

GITHUB_USERNAME = "wafi11"

def get_github_stats():
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}

    # Stats user
    url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    res = requests.get(url, headers=headers).json()

    # Ambil semua repo
    repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
    repos = requests.get(repos_url, headers=headers).json()

    # Hitung total bytes per bahasa
    lang_totals = {}
    for repo in repos:
        if repo.get("fork"):  # skip forked repo
            continue
        lang_url = repo["languages_url"]
        langs = requests.get(lang_url, headers=headers).json()
        for lang, bytes_count in langs.items():
            lang_totals[lang] = lang_totals.get(lang, 0) + bytes_count

    # Sort by bytes, ambil top 5
    total_bytes = sum(lang_totals.values())
    top_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "repos": res["public_repos"],
        "followers": res["followers"],
        "following": res["following"],
        "languages": top_langs,
        "total_bytes": total_bytes
    }

def make_bar(percentage: float, length: int = 20) -> str:
    filled = int(percentage / 100 * length)
    return "█" * filled + "░" * (length - filled)

def update_readme():
    stats = get_github_stats()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Build language table
    lang_rows = ""
    for lang, bytes_count in stats["languages"]:
        pct = (bytes_count / stats["total_bytes"]) * 100
        bar = make_bar(pct)
        lang_rows += f"| {lang:<20} | {bar} | {pct:.1f}% |\n"

    content = f"""
## 📊 GitHub Stats

| 📦 Public Repos | 👥 Followers | 🔁 Following |
|----------------|-------------|-------------|
| {stats['repos']} | {stats['followers']} | {stats['following']} |

## 🧑‍💻 Most Used Languages

| Language             | Usage                    | % |
|----------------------|--------------------------|---|
{lang_rows}
> 🕐 Last updated: {now}
"""

    if not os.path.exists("README.md"):
        with open("README.md", "w") as f:
            f.write("# Hi, I'm Wafi 👋\n\n<!-- GITHUB_STATS -->\n<!-- /GITHUB_STATS -->\n")

    with open("README.md", "r") as f:
        readme = f.read()

    new_readme = re.sub(
        r"<!-- GITHUB_STATS -->.*<!-- /GITHUB_STATS -->",
        f"<!-- GITHUB_STATS -->{content}<!-- /GITHUB_STATS -->",
        readme,
        flags=re.DOTALL
    )

    with open("README.md", "w") as f:
        f.write(new_readme)

    print("README updated!")

if __name__ == "__main__":
    update_readme()

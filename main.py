import requests
from datetime import datetime

GITHUB_USERNAME = "wafi11" 

def get_github_stats():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    res = requests.get(url).json()
    return {
        "repos": res["public_repos"],
        "followers": res["followers"],
        "following": res["following"],
    }

def update_readme():
    stats = get_github_stats()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    content = f"""
| 📦 Repos | 👥 Followers | 🔁 Following |
|----------|-------------|-------------|
| {stats['repos']} | {stats['followers']} | {stats['following']} |

> 🕐 Last updated: {now}
"""

    with open("README.md", "r") as f:
        readme = f.read()

    # Replace konten antara marker
    import re
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
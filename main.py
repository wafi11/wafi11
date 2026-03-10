import requests
import os
from datetime import datetime

GITHUB_USERNAME = "wafi11"

def get_github_stats():
    token = os.environ.get("GITHUB_TOKEN")  # ambil dari env
    headers = {"Authorization": f"token {token}"} if token else {}
    
    url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    res = requests.get(url, headers=headers)
    data = res.json()

    # Debug kalau masih error
    if "public_repos" not in data:
        print(f"API Response: {data}")
        raise Exception(f"GitHub API error: {data.get('message', 'unknown')}")

    return {
        "repos": data["public_repos"],
        "followers": data["followers"],
        "following": data["following"],
    }
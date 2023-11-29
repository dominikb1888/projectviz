from collections import Counter
from datetime import datetime
import json
import os

import requests
import pandas as pd


from dotenv import load_dotenv

load_dotenv()

GHTOKEN = os.getenv("GHTOKEN")
GHURL = os.getenv("GHURL")
GHORG = os.getenv("GHORG")
STARTDATE = os.getenv("STARTDATE")

print(GHURL, GHORG)


def get_repo(org, repos=True, *args):
    base_url = f"https://api.github.com"

    if repos:
        url = f"{base_url}/orgs/{org}/repos"
    else:
        url = f"{base_url}/repos/{org}"
        for arg in args:
            url += f"/{arg}"

    headers = {"Authorization": f"token {GHTOKEN}"}

    all_data = []
    page = 1
    per_page = 100  # Number of items per page

    while True:
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            data = [data] if not isinstance(data, list) else data
            all_data.extend(data)
            if len(data) < per_page:
                break
            else:
                page += 1
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break
            
    return all_data

def filter_images(json_list):
    images = []
    for content in json_list:
        if content["type"] == "file" and content["path"].endswith(
            (".jpg", ".gif", ".png")
        ):
            images.append(content["download_url"])

    return images


def get_data(org=GHORG):
    repo_list = []
    for repo in get_repo(org=org, repos=True):
        project = repo["name"]
        full_repo = get_repo(org, False, project)[0]
        print(full_repo)
        tags = get_repo(org, False, project, "tags")
        contents = get_repo(org, False, project, "contents")
        commits = sorted(
            get_repo(org, False, project, "commits"),
            key=lambda commit: commit["commit"]["author"]["date"],
        )
        languages = get_repo(org, False, project, "languages")
        user = (
            full_repo["parent"]["owner"] if full_repo.get("parent", False) else full_repo["owner"]
        )  # Mapping Data
        item = {
            "user": user["login"],
            "repo": full_repo,
            "avatar": user["avatar_url"],
            "description": full_repo["description"],
            "tags": tags,
            "images": filter_images(contents),
            "commits": commits,
            "commit_count": len(commits),
            "commit_latest": commits[-1],
            "commit_latest_date": str(commits[-1]["commit"]["author"]["date"]),
            "commit_latest_message": commits[-1]["commit"]["message"],
            "commit_histogram_daily": json.dumps(get_commit_histogram(commits)),
            "languages": languages,
        }

        repo_list.append(item)
        repo_list = sorted(
            repo_list, key=lambda x: x["commit_latest_date"], reverse=True
        )
        df = pd.DataFrame(repo_list)
        df.to_json("data.json", orient="records")

    return repo_list


def get_commit_histogram(commits):
    dates = [
        datetime.strptime(
            commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ"
        ).date()
        for commit in commits
    ]

    return [{"date": str(k), "count": v} for k, v in dict(Counter(dates)).items()]

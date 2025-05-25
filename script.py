import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_gfg_stats(username):
    url = f"https://auth.geeksforgeeks.org/user/{username}/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    stats = {
        "username": username,
        "coding_score": "N/A",
        "problems_solved": "N/A",
    }

    # Find coding score
    coding_score_heading = soup.find("h5", string="Coding Score")
    if coding_score_heading:
        # The next sibling h5 has the score
        score_tag = coding_score_heading.find_next_sibling("h5")
        if score_tag:
            stats["coding_score"] = score_tag.text.strip()

    # Find problems solved
    problems_heading = soup.find("h5", string="Problems Solved")
    if problems_heading:
        problems_tag = problems_heading.find_next_sibling("h5")
        if problems_tag:
            stats["problems_solved"] = problems_tag.text.strip()

    return stats

def generate_readme(stats):
    new_content = f"""

---

# GeeksforGeeks Stats Card

**Username:** [{stats['username']}](https://auth.geeksforgeeks.org/user/{stats['username']}/)  
**Coding Score:** {stats['coding_score']}  
**Problems Solved:** {stats['problems_solved']}  

_Last updated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_
"""

    # Read existing README content
    try:
        with open("README.md", "r") as f:
            existing = f.read()
    except FileNotFoundError:
        existing = ""

    # Append new content at the end
    with open("README.md", "w") as f:
        f.write(existing)
        f.write(new_content)

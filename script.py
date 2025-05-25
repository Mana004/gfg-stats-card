import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_gfg_stats(username):
    url = f"https://auth.geeksforgeeks.org/user/{username}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    labels = soup.find_all('div', class_='scoreCard_head_left--text__KZ2S1')
    stats = {}

    for label_div in labels:
        label = label_div.text.strip()
        value_div = label_div.find_next_sibling('div', class_='scoreCard_head_left--score__oSi_x')
        if value_div:
            value = value_div.text.strip()
            stats[label] = value

    coding_score = stats.get('Coding Score', 'N/A')
    problems_solved = stats.get('Problem Solved', 'N/A')

    return {
        'username': username,
        'coding_score': coding_score,
        'problems_solved': problems_solved
    }

def update_readme(stats):
    stats_block = f"""<!-- GFG_STATS_START -->
  
## GeeksforGeeks Stats

**Username:** [{stats['username']}](https://auth.geeksforgeeks.org/user/{stats['username']}/)  
**Coding Score:** {stats['coding_score']}  
**Problems Solved:** {stats['problems_solved']}  
  
_Last updated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_

<!-- GFG_STATS_END -->"""

    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    if "<!-- GFG_STATS_START -->" in content and "<!-- GFG_STATS_END -->" in content:
        content = re.sub(
            r"<!-- GFG_STATS_START -->.*<!-- GFG_STATS_END -->",
            stats_block,
            content,
            flags=re.DOTALL
        )
    else:
        content += "\n\n" + stats_block

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    username = "itsmanhy69"  # Replace with your GfG username if needed
    stats = get_gfg_stats(username)
    update_readme(stats)

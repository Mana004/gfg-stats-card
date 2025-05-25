import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_gfg_stats(username):
    url = f"https://www.geeksforgeeks.org/user/{username}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    coding_score_div = soup.find('div', class_='rating-number')
    coding_score = coding_score_div.text.strip() if coding_score_div else 'N/A'

    problems_solved = 'N/A'
    stats_sections = soup.find_all('div', class_='stat-number')
    for stat in stats_sections:
        label = stat.find_previous_sibling('div')
        if label and 'Solved' in label.text:
            problems_solved = stat.text.strip()
            break

    return {
        'username': username,
        'coding_score': coding_score,
        'problems_solved': problems_solved
    }

def update_readme(stats):
    stats_block = f"""<!-- GFG_STATS_START -->
  
## GeeksforGeeks Stats

**Username:** [{stats['username']}](https://www.geeksforgeeks.org/user/{stats['username']}/)  
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
    username = "itsmanhy69"
    stats = get_gfg_stats(username)
    update_readme(stats)

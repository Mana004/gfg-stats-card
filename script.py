import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_gfg_stats(username):
    url = f"https://www.geeksforgeeks.org/user/{username}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    coding_score = 'N/A'
    problems_solved = 'N/A'

    # Find Coding Score
    coding_div = soup.find('div', class_='rating-number')
    if coding_div:
        coding_score = coding_div.text.strip()

    # Find Problems Solved by matching label and its value
    stats_labels = soup.find_all('div', class_='stat-text')
    stats_values = soup.find_all('div', class_='stat-number')

    for label, value in zip(stats_labels, stats_values):
        label_text = label.text.strip()
        if 'Solved' in label_text:
            problems_solved = value.text.strip()
            break

    print(f"Debug: coding_score={coding_score}, problems_solved={problems_solved}")

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

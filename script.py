import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Function to scrape data
def get_gfg_stats(username):
    url = f"https://auth.geeksforgeeks.org/user/{username}/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch profile: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract coding score
    coding_score_div = soup.find("div", class_="score_card_value")
    coding_score = coding_score_div.text.strip() if coding_score_div else "N/A"

    # Extract number of problems solved
    problems_solved = "N/A"
    stats_divs = soup.find_all("div", class_="score_cards_item_content")
    for div in stats_divs:
        if "Problems Solved" in div.text:
            problems_solved = div.find("span").text.strip()
            break

    return {
        "username": username,
        "coding_score": coding_score,
        "problems_solved": problems_solved
    }

# Function to update README
def generate_readme(stats):
    stats_block = f"""<!-- GFG_STATS_START -->

# GeeksforGeeks Stats Card

**Username:** [{stats['username']}](https://auth.geeksforgeeks.org/user/{stats['username']}/)  
**Coding Score:** {stats['coding_score']}  
**Problems Solved:** {stats['problems_solved']}  

_Last updated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_

<!-- GFG_STATS_END -->"""

    try:
        with open("README.md", "r") as f:
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
        content += f"\n{stats_block}"

    with open("README.md", "w") as f:
        f.write(content)

# Run scraper and update readme
if __name__ == "__main__":
    stats = get_gfg_stats("itsmanhy69")
    print("✅ Stats fetched successfully.")
    generate_readme(stats)
    print("✅ README updated successfully.")
    print("DEBUG: Fetched stats:", stats)  # Add this line


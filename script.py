import re
from datetime import datetime

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

    # Replace content between markers
    if "<!-- GFG_STATS_START -->" in content and "<!-- GFG_STATS_END -->" in content:
        content = re.sub(
            r"<!-- GFG_STATS_START -->.*<!-- GFG_STATS_END -->",
            stats_block,
            content,
            flags=re.DOTALL
        )
    else:
        # If markers not found, append block at the end
        content += f"\n{stats_block}"

    with open("README.md", "w") as f:
        f.write(content)

if __name__ == "__main__":
    stats = get_gfg_stats("itsmanhy69")  # or your GfG username
    generate_readme(stats)
print("Generating README with latest stats...")

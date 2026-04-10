import requests
import json
import os
import time
from datetime import datetime

# Configuration and Keywords
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def fetch_trending_data():
    collected_stories = []
    category_counts = {cat: 0 for cat in CATEGORIES}
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    try:
        # Step 1: Get top 500 story IDs
        print("Fetching top stories from HackerNews...")
        response = requests.get(f"{BASE_URL}/topstories.json", headers=HEADERS)
        response.raise_for_status()
        story_ids = response.json()[:500]
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return

    # Step 2: Iterate through stories and categorize
    for category, keywords in CATEGORIES.items():
        print(f"Processing category: {category}...")
        
        for item_id in story_ids:
            # Stop if we have 25 stories for this category
            if category_counts[category] >= 25:
                break
                
            try:
                item_url = f"{BASE_URL}/item/{item_id}.json"
                item_res = requests.get(item_url, headers=HEADERS)
                item_res.raise_for_status()
                story = item_res.json()

                # Skip if not a story or missing title
                if not story or 'title' not in story:
                    continue

                title = story.get('title', '')
                title_upper = title.upper()
                
                # Check if any keyword matches the title
                if any(kw.upper() in title_upper for kw in keywords):
                    # Extract required fields
                    story_data = {
                        "post_id": story.get("id"),
                        "title": title,
                        "category": category,
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by", "unknown"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    collected_stories.append(story_data)
                    category_counts[category] += 1
                    
            except Exception as e:
                print(f"Skipping story {item_id} due to error: {e}")
                continue
        
        # Mandatory 2-second sleep between category loops
        time.sleep(2)

    # Step 3: Save to JSON
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(collected_stories, f, indent=4)
    
    print(f"Collected {len(collected_stories)} stories. Saved to {filename}")

if __name__ == "__main__":
    fetch_trending_data()


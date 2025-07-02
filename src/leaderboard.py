import json
import os

# Path to the leaderboard JSON file
LEADERBOARD_FILE = "data/leaderboard.json"

def load_leaderboard():
    # Load leaderboard data from the JSON file
    if not os.path.exists(LEADERBOARD_FILE):
        # If file doesn't exist, return empty list
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        # Load and return the JSON data
        return json.load(f)

def save_score(name, score):
    # Save or update a player's score in the leaderboard
    scores = load_leaderboard()
    for entry in scores:
        if entry["name"] == name:
            # If player exists, update score if new score is higher
            entry["score"] = max(entry["score"], score)
            break
    else:
        # If player not found, add new entry
        scores.append({"name": name, "score": score})
    # Sort scores in descending order and keep only top 10
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        # Save updated leaderboard back to the file
        json.dump(scores, f, indent=4)

import json
import os

LEADERBOARD_FILE = "data\leaderboard.json"

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_score(name, score):
    scores = load_leaderboard()
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f, indent=4)

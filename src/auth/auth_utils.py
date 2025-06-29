import os
import csv
import json

USER_FILE = "src/auth/users.csv"
SCORES_FILE = 'data/user_scores.json'
LAST_USER_FILE = 'data/last_user.txt'

def init_user_file():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password", "high_score"])

def user_exists(username):
    with open(USER_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        return any(row["username"] == username for row in reader)

def register_user(username, password):
    if user_exists(username):
        return False
    with open(USER_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password, 0])
    return True

def validate_user(username, password):
    with open(USER_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                return True
    return False

def remember_user(username):
    with open(LAST_USER_FILE, 'w') as f:
        f.write(username)

def get_remembered_user():
    if os.path.exists(LAST_USER_FILE):
        with open(LAST_USER_FILE, 'r') as f:
            return f.read().strip()
    return None

def logout_user():
    if os.path.exists(LAST_USER_FILE):
        os.remove(LAST_USER_FILE)

def auth_save_score(username, score):
    scores = {}
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            scores = json.load(f)
    scores[username] = max(score, scores.get(username, 0))  # Save highest
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def get_all_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return {}

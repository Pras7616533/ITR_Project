import os
import csv
import json
import config

# File paths for user data and scores
USER_FILE = "src/auth/users.csv"
SCORES_FILE = 'data/user_scores.json'
LAST_USER_FILE = 'data/last_user.txt'

def init_user_file():
    """
    Initialize the user CSV file with headers if it doesn't exist.
    """
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password", "high_score"])

def user_exists(username):
    """
    Check if a user with the given username exists in the user file.
    """
    with open(USER_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        return any(row["username"] == username for row in reader)

def register_user(username, password):
    """
    Register a new user with username and password.
    Returns False if user already exists, True otherwise.
    """
    if user_exists(username):
        return False
    with open(USER_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password, 0])
    return True

def validate_user(username, password):
    """
    Validate if the username and password match an entry in the user file.
    """
    with open(USER_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                return True
    return False

def remember_user(username):
    """
    Save the username to a file to remember the last logged-in user.
    """
    with open(LAST_USER_FILE, 'w') as f:
        f.write(username)

def get_remembered_user():
    """
    Retrieve the last remembered username, if available.
    """
    if os.path.exists(LAST_USER_FILE):
        with open(LAST_USER_FILE, 'r') as f:
            return f.read().strip()
    return None

def logout_user():
    """
    Log out the current user by removing the remembered user file and resetting config.level.
    """
    if os.path.exists(LAST_USER_FILE):
        os.remove(LAST_USER_FILE)
    config.level = 0

def auth_save_score(username, score):
    """
    Save the user's highest score to a JSON file.
    Only updates if the new score is higher than the previous one.
    """
    scores = {}
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            scores = json.load(f)
    scores[username] = max(score, scores.get(username, 0))  # Save highest
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def get_all_scores():
    """
    Retrieve all user scores from the JSON file.
    Returns an empty dictionary if the file does not exist.
    """
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return {}

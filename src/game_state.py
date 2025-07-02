class GameState:
    # The main menu or home screen state
    HOME = "home"
    # The state when the game is actively being played
    PLAYING = "playing"
    # The state used for transitions between other states (e.g., animations)
    TRANSITION = "transition"
    # The state when the game has been completed
    COMPLETED = "completed"
    # The state when the player has lost the game
    LOST = "lost"
    # The state when the player has won the game
    WON = "won"
    # The state when a level has been completed successfully
    LEVEL_WON = "level_won"
    # The state for displaying help or instructions
    HELP = "help"
    # The state for user login
    LOGIN = "login"
    # The state for user logout
    LOGOUT = "logout"
    # The state for admin access or admin panel
    ADMIN = "admin"
    # The state for displaying the leaderboard
    LEADERBOARD = "leaderboard"
    # The state for inputting the player's name
    NAME_INPUT = "name_input"
    # The state for resetting the user's password
    RESET_PASSWORD = "reset_password"

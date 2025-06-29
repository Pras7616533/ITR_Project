# 🌀 Mystic Maze: The Quest for the Crystal

Welcome to *Mystic Maze*, a fantasy-themed 2D adventure game built with **Python & Pygame**. Explore challenging mazes, avoid traps, collect keys, and claim the legendary crystal! Featuring user authentication, themes, leaderboard, and more.

---

## 🎮 Features

* 🧩 **Maze Gameplay**: Randomly generated mazes with increasing difficulty.
* 🔐 **Authentication System**:

  * Login & Sign-Up screens
  * "Remember Me" support
  * Admin panel
* 📊 **Leaderboard**: Tracks top high scores across users.
* 🧙‍♂️ **User-Specific Data**:

  * Per-user high score
  * Theme preferences (wall, player, strip)
* 🖼️ **Theming System**:

  * Switch player, wall, strip themes in-game (`P`, `S`)
* 🗺️ **Mini-map & Hints**:

  * `M`: Toggle mini-map
  * `H`: Toggle path-to-nearest-key hints
* 🛠️ **Admin Panel**:

  * View all users and top scores
* 🔁 **Reset Password Feature**
* 🖼️ **Custom UI with assets**: Backgrounds, buttons, sound effects
* 🧍‍♂️ **Profile Avatars** *(Planned)*

---

## 🧾 Requirements

* Python 3.8+
* `pygame`

Install dependencies:

```bash
pip install pygame
```

---

## 🕹️ Controls

| Action             | Key                 |
| ------------------ | ------------------- |
| Move Player        | Arrow Keys          |
| Toggle Hint to Key | `H`                 |
| Toggle Mini-map    | `M`                 |
| Restart Level      | `R`                 |
| Change Theme       | `P`, `S`            |
| Quit Game          | `Q`                 |
| Back to Menu       | `B` (in Help/Admin) |

---

## 👤 User Roles

* **Player**: Can log in, play, and save high scores.
* **Admin**:

  * Use `username: admin`, `password: admin`
  * Access admin panel to view global stats.

---

## 📚 Future Improvements

* 🎨 Avatar/Profile Picture upload
* 🌈 Theme Selector in settings
* 📧 Email verification for password reset
* 🗃️ SQLite support (optional upgrade from CSV)
* 📱 Mobile port (Kivy / Android)

---

## 🧠 Credits

* Built by: Prashant K Deshmukh
* Assets: Custom-drawn or from open source repositories
* Fonts: None
* Icons: Emoji Unicode

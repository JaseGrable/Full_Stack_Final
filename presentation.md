# 🏈 Fantasy Football Web App (Sleeper API)

## 🎯 Project Overview
This is a full-stack Flask web application that integrates with the **Sleeper Fantasy Football API** to display NFL league, team, and roster data. Users can browse team rosters and leave comments. An admin interface allows comment moderation.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS, JavaScript (Responsive Design)
- **Backend**: Flask (Python)
- **Database**: SQLite (`nfl_players.db` for player info, `comments.db` for comments)
- **Authentication**: Simple form-based login for admin
- **Session Management**: Flask session

---

## 🧭 How It Works

### 1. Homepage (`/`)
- Users enter their **Sleeper username**.
- The app fetches their **user ID** and active **NFL leagues** for the 2025 season.
- Leagues are displayed as clickable cards.

### 2. Users in a League (`/users/<league_id>/<league_name>`)
- Shows all users (participants) in a selected fantasy league.

### 3. Roster Page (`/roster/<league_id>/<user_id>/<user_name>`)
- Shows a player's roster, separated into:
  - **Starters**
  - **Bench**
  - **Taxi Squad**
- Player info comes from a local `nfl_players.db` database.
- Each position is color-coded:
  - QB: Blue
  - RB: Red
  - WR: Yellow
  - TE: Purple
  - K: Green
  - DEF: Orange
- Users can leave **comments** on rosters.
- Comments are stored in `comments.db` and signed with the username entered on the homepage.

---

## 💬 Comments System

- SQLite table `comments` holds:
  - `id`
  - `user_id` (roster owner)
  - `username` (who posted the comment)
  - `comment`
- Comments are displayed under the relevant roster.
- Stored using SQL `INSERT`, retrieved with `SELECT`.

---

## 🔐 Admin Panel

### Login (`/admin/login`)
- Simple form-based login with hardcoded credentials.

### Dashboard (`/admin`)
- Admin can **view all comments**.
- Admin can **delete comments** by ID.
- Access is restricted to logged-in admins via Flask session.

### Logout (`/admin/logout`)
- Clears the session and redirects to login.

---

## ⚙️ Session Management

- `session['username']` stores the name users enter on the homepage.
- Used to sign roster comments.

---

## 🌱 Possible Future Improvements

- Replace hardcoded admin login with a database + hashed passwords.
- Add player statistics or real-time updates.
- Implement comment editing or upvoting.
- Add search/filter for leagues, teams, and players.
- Deploy on a live server (e.g., Render or Heroku).

---

## 📁 Database Overview

### `nfl_players.db`
| Column       | Description        |
|--------------|--------------------|
| `player_id`  | Sleeper API player ID |
| `full_name`  | Player name        |
| `team`       | NFL team           |
| `position`   | Player position    |

### `comments.db`
| Column     | Description           |
|------------|-----------------------|
| `id`       | Comment ID (PK)       |
| `user_id`  | Roster owner's user ID |
| `username` | Name of commenter     |
| `comment`  | The comment text      |

---

## 🧪 Testing & Debugging Tips

- Use `/admin` to check if comments are being stored properly.
- Enable Flask's `debug=True` for live error tracking.
- Ensure both SQLite files (`nfl_players.db` and `comments.db`) are in your project root.

---

## 🚀 How to Run

```bash
# 1. Activate your virtual environment (if applicable)
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Run the app
python app.py

# 3. Open in your browser
http://127.0.0.1:5000

from flask import Flask, render_template, request, redirect, session
import requests
import sqlite3
from nfl_teams import nfl_teams
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    leagues = None
    error_message = None

    if request.method == "POST":
        username = request.form["username"]
        user_url = f"https://api.sleeper.app/v1/user/{username}"
        user_response = requests.get(user_url)

        if user_response.status_code == 200:
            user_data = user_response.json()
            user_id = user_data.get("user_id")

            if user_id:
                sport = "nfl"
                season = "2025"
                leagues_url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/{sport}/{season}"
                leagues_response = requests.get(leagues_url)

                if leagues_response.status_code == 200:
                    leagues = leagues_response.json()
                    if not leagues:
                        error_message = f"No leagues found for user {username}."
                else:
                    error_message = f"Failed to retrieve leagues. Status code: {leagues_response.status_code}"
            else:
                error_message = f"User ID not found for username: {username}"
        else:
            error_message = f"Failed to retrieve user data. Status code: {user_response.status_code}"

        session['username'] = username

    return render_template("index.html", leagues=leagues, error_message=error_message, nfl_teams=nfl_teams)

# Users in League
@app.route("/users/<league_id>/<league_name>", methods=["GET"])
def users(league_id, league_name):
    users_url = f"https://api.sleeper.app/v1/league/{league_id}/users"
    users_response = requests.get(users_url)

    users = None
    error_message = None

    if users_response.status_code == 200:
        users = users_response.json()
        if not users:
            error_message = f"No users found for league ID {league_id}."
    else:
        error_message = f"Failed to retrieve users. Status code: {users_response.status_code}"

    return render_template("users.html", users=users, error_message=error_message, league_id=league_id, league_name=league_name, nfl_teams=nfl_teams)

# Roster for a User
@app.route("/roster/<league_id>/<user_id>/<user_name>", methods=["GET", "POST"])
def user_roster(league_id, user_id, user_name):
    rosters_url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    traded_picks_url = f"https://api.sleeper.app/v1/league/{league_id}/traded_picks"
    users_url = f"https://api.sleeper.app/v1/league/{league_id}/users"

    rosters_response = requests.get(rosters_url)
    traded_picks_response = requests.get(traded_picks_url)
    users_response = requests.get(users_url)

    starters_data = []
    bench_data = []
    taxi_data = []
    traded_picks = []
    error_message = None
    roster = None
    user_names = {}

    if users_response.status_code == 200:
        users = users_response.json()
        user_names = {user['user_id']: user['display_name'] for user in users}

    if rosters_response.status_code == 200:
        rosters = rosters_response.json()
        roster = next((r for r in rosters if r["owner_id"] == user_id), None)

        if roster:
            starters = roster.get("starters", [])
            all_players = roster.get("players", [])
            taxi = roster.get("taxi", [])
            bench = [p for p in all_players if p not in starters and p not in taxi]

            conn = sqlite3.connect("nfl_players.db")
            cursor = conn.cursor()

            def get_player_details(player_id):
                cursor.execute('''
                    SELECT full_name, team, position FROM nfl_players WHERE player_id = ?
                ''', (player_id,))
                result = cursor.fetchone()
                name = result[0] if result else "Unknown"
                team = result[1] if result else "-"
                position = result[2] if result else "-"
                position_colors = {
                    "QB": "#d0e1f9",
                    "RB": "#f9d0d0",
                    "WR": "#fcf8cf",
                    "TE": "#e5d0f9",
                    "K": "#d0f9d9",
                    "DEF": "#fce0b2"
                }
                color = position_colors.get(position, "#ffffff")
                return {
                    "id": player_id,
                    "name": name,
                    "team": team,
                    "position": position,
                    "position_color": color,
                }

            starters_data = [get_player_details(pid) for pid in starters]
            bench_data = [get_player_details(pid) for pid in bench]
            taxi_data = [get_player_details(pid) for pid in taxi]
            conn.close()

    # Handle comment submission
    if request.method == "POST":
        comment_text = request.form.get("comment")
        username = session.get("username", "")  
        conn = sqlite3.connect("comments.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            comment TEXT
        )''')
        cursor.execute("INSERT INTO comments (user_id, username, comment) VALUES (?, ?, ?)", (user_id, username, comment_text))
        conn.commit()
        conn.close()
        return redirect(f"/roster/{league_id}/{user_id}/{user_name}")

    # Retrieve existing comments
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, comment FROM comments WHERE user_id = ?", (user_id,))
    comments = cursor.fetchall()
    conn.close()

    return render_template("user_roster.html",
                           user_name=user_name,
                           starters_data=starters_data,
                           bench_data=bench_data,
                           taxi_data=taxi_data,
                           roster=roster,
                           error_message=error_message,
                           traded_picks=traded_picks,
                           nfl_teams=nfl_teams,
                           comments=comments)

if __name__ == "__main__":
    app.run(debug=True)

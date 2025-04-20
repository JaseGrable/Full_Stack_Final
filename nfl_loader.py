import requests
import sqlite3

# Step 1: Fetch the data from Sleeper API
url = "https://api.sleeper.app/v1/players/nfl"
response = requests.get(url)
players_data = response.json()

# Step 2: Connect to SQLite and create table
conn = sqlite3.connect("nfl_players.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS nfl_players (
    player_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    full_name TEXT,
    team TEXT,
    position TEXT,
    status TEXT,
    fantasy_positions TEXT,
    number INTEGER,
    height TEXT,
    weight TEXT,
    age INTEGER,
    college TEXT,
    years_exp INTEGER,
    depth_chart_position INTEGER,
    depth_chart_order INTEGER,
    hashtag TEXT
);
''')

# Step 3: Insert players into the table
for player_id, player in players_data.items():
    try:
        cursor.execute('''
        INSERT OR REPLACE INTO nfl_players (
            player_id, first_name, last_name, full_name, team, position, status,
            fantasy_positions, number, height, weight, age, college, years_exp,
            depth_chart_position, depth_chart_order, hashtag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player_id,
            player.get("first_name"),
            player.get("last_name"),
            f"{player.get('first_name', '')} {player.get('last_name', '')}".strip(),
            player.get("team"),
            player.get("position"),
            player.get("status"),
            ','.join(player.get("fantasy_positions", [])),
            player.get("number"),
            player.get("height"),
            player.get("weight"),
            player.get("age"),
            player.get("college"),
            player.get("years_exp"),
            player.get("depth_chart_position"),
            player.get("depth_chart_order"),
            player.get("hashtag")
        ))
    except Exception as e:
        print(f"Error inserting player {player_id}: {e}")

# Step 4: Save and close
conn.commit()
conn.close()

print("Done! Data saved to nfl_players.db")

import csv
import sqlite3

conn = sqlite3.connect("nfl_players.db")
cursor = conn.cursor()

cursor.execute("SELECT player_id, first_name, last_name, team, position FROM nfl_players")
players = cursor.fetchall()

with open("nfl_players_export.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Player ID", "First Name", "Last Name", "Team", "Position"])  # Header row
    writer.writerows(players)

conn.close()
print("Data exported to nfl_players_export.csv")

from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Connect to Kafka topic
consumer = KafkaConsumer(
    "nba-momentum",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="nba-group"
)

# Track total team points
team_points = defaultdict(int)

# Set up the live plot
plt.ion()
fig, ax = plt.subplots()
fig.canvas.manager.set_window_title("NBA Momentum Tracker")

# Custom style
plt.style.use("dark_background")

while True:
    for message in consumer:
        event = message.value
        team = event.get("team")
        points = event.get("points", 0)
        player = event.get("player", "Unknown")

        # Update points
        team_points[team] += points

        # Update chart
        ax.clear()
        teams = list(team_points.keys())
        totals = list(team_points.values())

        ax.bar(teams, totals, color=["#007FFF", "#FF6B00"])
        ax.set_xlabel("Teams")
        ax.set_ylabel("Total Points")
        ax.set_title(f"Live NBA Scoring Momentum — {team}: +{points} ({player})", fontsize=12, pad=15)
        plt.tight_layout()
        plt.pause(0.5)

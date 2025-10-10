"""
NBA Momentum Streaming Producer
--------------------------------
Streams live NBA team statistics using the nba_api.
Each record includes team performance metrics and a calculated momentum score.
Sends messages to a Kafka topic and logs them locally to CSV for analysis.
"""

from kafka import KafkaProducer
from nba_api.stats.endpoints import leaguedashteamstats
from datetime import datetime
import pandas as pd
import json
import time
import logging
import os

# Configuration
TOPIC_NAME = "nba-momentum"
LOG_DIR = "data"
LOG_FILE = os.path.join(LOG_DIR, "nba_stream_log.csv")

# Logging setup
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "nba_producer.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def get_team_stats():
    """Fetch team stats for the current NBA season."""
    data = leaguedashteamstats.LeagueDashTeamStats(season="2024-25").get_data_frames()[0]
    data = data[["TEAM_ID", "TEAM_NAME", "GP", "W_PCT", "PTS", "REB", "AST", "FG_PCT", "PLUS_MINUS"]]
    return data

def calculate_momentum(row):
    """Simple formula combining performance stats into a momentum score."""
    return round(
        (row["PTS"] * 0.4 + row["REB"] * 0.25 + row["AST"] * 0.2 + row["W_PCT"] * 100 + row["PLUS_MINUS"]) / 10,
        2
    )

def ensure_log_file():
    """Create data directory and CSV log if they do not exist."""
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        columns = [
            "timestamp", "team_id", "team_name", "games_played",
            "win_pct", "points", "rebounds", "assists",
            "fg_pct", "plus_minus", "momentum_score"
        ]
        pd.DataFrame(columns=columns).to_csv(LOG_FILE, index=False)

def stream_nba_data():
    """Continuously fetch, log, and send NBA data to Kafka."""
    ensure_log_file()

    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    logging.info("NBA producer started - streaming live data")

    while True:
        try:
            # Get fresh NBA stats
            df = get_team_stats()

            # Loop through each team and send data
            for _, row in df.iterrows():
                record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "team_id": int(row["TEAM_ID"]),
                    "team_name": row["TEAM_NAME"],
                    "games_played": int(row["GP"]),
                    "win_pct": round(row["W_PCT"], 3),
                    "points": int(row["PTS"]),
                    "rebounds": int(row["REB"]),
                    "assists": int(row["AST"]),
                    "fg_pct": round(row["FG_PCT"], 3),
                    "plus_minus": float(row["PLUS_MINUS"]),
                    "momentum_score": calculate_momentum(row)
                }

                # Send to Kafka topic
                producer.send(TOPIC_NAME, value=record)

                # Log locally
                pd.DataFrame([record]).to_csv(LOG_FILE, mode="a", header=False, index=False)

            logging.info(f"Streamed {len(df)} records successfully.")
            time.sleep(15)  # Pause before next stream batch

        except Exception as e:
            logging.error(f"Error in producer: {e}")
            time.sleep(10)

if __name__ == "__main__":
    stream_nba_data()

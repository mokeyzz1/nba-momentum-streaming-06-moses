"""
NBA Momentum Streaming Consumer
--------------------------------
Consumes NBA team data from the Kafka topic 'nba-momentum'.
Each message contains team statistics and a calculated momentum score.
Displays a live bar chart of team momentum in real time.
"""

from kafka import KafkaConsumer
import matplotlib.pyplot as plt
import json
import pandas as pd
import time

# Configuration
TOPIC_NAME = "nba-momentum"
BOOTSTRAP_SERVERS = "localhost:9092"

def main():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="nba-group"
    )

    print("Consumer started...")

    # Prepare a DataFrame for storing team data
    df = pd.DataFrame(columns=["team_name", "momentum_score"])

    plt.ion()
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title("NBA Momentum Stream")

    for message in consumer:
        event = message.value
        team_name = event["team_name"]
        momentum_score = event["momentum_score"]

        # Update DataFrame
        if team_name in df["team_name"].values:
            df.loc[df["team_name"] == team_name, "momentum_score"] = momentum_score
        else:
            df.loc[len(df)] = [team_name, momentum_score]

        # Sort teams by score for clearer chart
        df_sorted = df.sort_values(by="momentum_score", ascending=False)

        # Clear and replot
        ax.clear()
        ax.barh(df_sorted["team_name"], df_sorted["momentum_score"])
        ax.set_xlabel("Momentum Score")
        ax.set_ylabel("Team")
        ax.set_title("Live NBA Team Momentum Stream")
        plt.tight_layout()
        plt.draw()
        plt.pause(0.5)

        time.sleep(0.1)

if __name__ == "__main__":
    main()

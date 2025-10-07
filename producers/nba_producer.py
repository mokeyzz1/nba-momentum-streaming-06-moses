from kafka import KafkaProducer
import json
import time
import random

# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = "nba-momentum"

# Simple team scores
teams = ["BOS", "NYK"]
scores = {"BOS": 0, "NYK": 0}

print("Producer started...")

while True:
    # Pick random team and points
    team = random.choice(teams)
    points = random.choice([2, 3])
    scores[team] += points

    # Create event
    event = {
        "team": team,
        "points": points,
        "BOS_score": scores["BOS"],
        "NYK_score": scores["NYK"]
    }

    # Send event
    producer.send(topic, event)
    print("Sent:", event)

    time.sleep(2)

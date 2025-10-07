# nba-momentum-streaming-06-moses

# NBA Momentum Streaming Project

## Overview
This project implements a custom real-time streaming pipeline that tracks NBA team momentum using Kafka producers and consumers.
The system simulates scoring events during NBA games, streams them to a Kafka topic, and visualizes the live momentum between teams.

## Features
- **Producer**: Streams JSON-formatted scoring events (team, player, points, current score).
- **Consumer**: Tracks team scores, lead changes, and scoring runs in real time.
- **Visualization**: Animated line chart of team scores over time with lead-change markers.
- **Optional Alerts**: Trigger an alert if a team goes on a scoring run.

## Project Structure
producers/ → contains Kafka producer
consumers/ → contains Kafka consumer
utils/ → helper functions for data + visualization
data/ → sample game files (optional)

### Run Instructions
Start Zookeeper

cd ~/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties

Start Kafka Server
Open a new terminal:
cd ~/kafka
bin/kafka-server-start.sh config/server.properties

Create Kafka Topic (if not already created)
bin/kafka-topics.sh --create --topic nba-momentum --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

Run Producer
cd ~/nba-momentum-streaming-06-moses
source .venv/bin/activate
python producers/nba_producer.py

Run Consumer
python consumers/nba_consumer.py




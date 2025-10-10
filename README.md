# nba-momentum-streaming-06-moses

# NBA Momentum Streaming Project

## Overview
This project implements a custom real-time streaming pipeline that tracks NBA team momentum using Kafka producers and consumers.
The system simulates scoring events during NBA games, streams them to a Kafka topic, and visualizes the live momentum between teams.


## Insight Focus

Each Kafka message represents a scoring event (team + player + points).
As messages arrive, the consumer updates each team’s total score in real time.

This creates a live momentum visualization, letting you see which team is currently gaining the upper hand.
It’s a simplified version of what sports broadcasters use for live performance tracking.
## Features
- **Producer**: Streams JSON-formatted scoring events (team, player, points, current score).
- **Consumer**: Tracks team scores, lead changes, and scoring runs in real time.
- **Visualization**: Animated line chart of team scores over time with lead-change markers.
- **Optional Alerts**: Trigger an alert if a team goes on a scoring run.

## Objectives

- Create a Kafka streaming pipeline using Python.

- Stream live NBA data (scores, stats, or win probabilities) from the API.

- Consume and visualize the data in real time.

- Demonstrate the flow of information between producer and consumer.
  
## Project Structure
nba-momentum-streaming-06-moses/
│
├── producers/
│   └── nba_producer.py        # Fetches NBA data and streams to Kafka
│
├── consumers/
│   └── nba_consumer.py        # Receives data and plots it dynamically
│
├── data/
│   └── (optional logs or saved outputs)
│
├── requirements.txt
└── README.md


## How It Works

Producer:

Connects to the NBA API using nba_api.stats.endpoints.leaguedashteamstats.

Extracts live or recent team performance data.

Sends formatted JSON messages to a Kafka topic (nba_momentum).

Consumer:

Listens to the same topic.

Parses incoming JSON messages.

Uses Matplotlib to update a live chart showing team performance trends.

Logging:

Each message and update is recorded to logs/ for transparency and debugging.

Avoids print statements by using Python’s logging library.

### Run Instructions
How to Run

Start Kafka and Zookeeper

bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties


Create Topic

bin/kafka-topics.sh --create --topic nba_momentum --bootstrap-server localhost:9092


Run Producer

python producers/nba_producer.py


Run Consumer

python consumers/nba_consumer.py


Observe Results
Watch the live chart update as new NBA data streams in.




![alt text](<Screenshot 2025-10-10 at 12.28.46 AM.png>)
# nba-momentum-streaming-06-moses

# NBA Momentum Streaming Project

## Overview
This project simulates **live NBA scoring events** and streams them into a Kafka topic.  
A Kafka consumer reads these events, tracks scoring momentum, and visualizes live game scores dynamically using Matplotlib.

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
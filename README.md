League of Legends Champion Scaling Analysis
Overview

This project analyzes how League of Legends champions scale throughout a game based on real match data collected through the Riot Games API. Instead of relying on static win-rate curves or tier lists, this project examines actual performance trajectories over time. Specifically focusing on gold advantage, damage, and kill participation in order to reveal when champions are strongest.

Why?

Champions like Zed are often misunderstood. Though he is perceived as an early-game assassin, data shows he may scale better than expected, especially compared to burstier early-game champs like Talon or Naafiri. This project uncovers data-backed insights about champion power spikes and scaling trends.

Features

Win rate and performance trend graphs over game time

SQL-based analysis using normalized match datasets

Focus on advantage accrual (gold/damage/impact) instead of just final win/loss

Data stored and queried through PostgreSQL

Analysis powered by Python (pandas, matplotlib, etc.)

Tech Stack

Riot Games API (Match & Timeline Endpoints)

PostgreSQL (for relational data storage)

Python (for API calls, data processing, and visualization)

SQL (for extracting relevant time-series stats)

Getting Started

Clone this repo

Set up a PostgreSQL database

Add your Riot API key in config.py

Run fetch_matches.py to collect data

Use analyze_scaling.py to generate graphs

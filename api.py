import os
import time
import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------- SETUP --------------------
API_KEY = 'RGAPI-36b2fb3a-6d65-40aa-951a-33539dc7bf5e'
HEADERS = {'X-Riot-Token': API_KEY}
REGION = 'na1'
AMERICAS = 'americas'
DATA_PATH = './CS210_Final_Project'
os.makedirs(DATA_PATH, exist_ok=True)

# Only the one-trick champions you care about
SUMMONERS = [
    ("Laceration", "Zed"),
    ("Mental Clarity", "Shen"),
    ("dusklol", "000"),
    ("ame", "eve"),
    ("Bronny James", "bball"),
    ("Lebron James", "0131"),
    ("WiiWaterMelon", "NA1"),
    ("Salad", "1998")
]

# -------------------- API FUNCTIONS --------------------
def get_puuid(name, tag):
    url = f"https://{AMERICAS}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("puuid") if res.status_code == 200 else None

def get_match_ids(puuid, count=10):
    url = f"https://{AMERICAS}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&type=ranked"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else []

def get_match_data(match_id):
    url = f"https://{AMERICAS}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else None

# -------------------- DATA COLLECTION --------------------
match_rows = []

for name, tag in SUMMONERS:
    puuid = get_puuid(name, tag)
    if not puuid:
        continue
    match_ids = get_match_ids(puuid, count=10)
    for match_id in match_ids:
        match = get_match_data(match_id)
        if not match:
            continue
        duration_minutes = match['info']['gameDuration'] / 60
        for p in match["info"]["participants"]:
            challenges = p.get("challenges", {})
            row = {
                "match_id": match_id,
                "puuid": p["puuid"],
                "champion": p["championName"],
                "game_duration_minutes": duration_minutes,
                "win": int(p.get("win", False)),
                "gold_per_min": challenges.get("goldPerMinute", 0),
                "damage_per_min": challenges.get("damagePerMinute", 0),
                "kill_participation": challenges.get("killParticipation", 0),
                "dragon_takedowns": challenges.get("dragonTakedowns", 0),
                "baron_takedowns": challenges.get("baronTakedowns", 0),
                "kills": p.get("kills", 0),
                "deaths": p.get("deaths", 0),
                "assists": p.get("assists", 0),
            }
            match_rows.append(row)
        time.sleep(1.3)

df = pd.DataFrame(match_rows)
csv_path = os.path.join(DATA_PATH, "champion_scaling_data.csv")
df.to_csv(csv_path, index=False)

# -------------------- DATABASE --------------------
# Drop any columns without a name (causes SQLite issues)
df = df.loc[:, df.columns.notnull()]
df.columns = [str(col).strip() if col else f"unnamed_{i}" for i, col in enumerate(df.columns)]

# Drop completely empty rows (very rare case)
df.dropna(how='all', inplace=True)

# Save to SQLite
conn = sqlite3.connect(os.path.join(DATA_PATH, "champion_scaling.sqlite"))
df.to_sql("champion_data", conn, if_exists="replace", index=False)

# -------------------- WIN RATE OVER TIME GRAPH --------------------
df['duration_bin'] = (df['game_duration_minutes'] // 5 * 5).astype(int)
winrate_df = df.groupby(['champion', 'duration_bin'])['win'].mean().reset_index()
winrate_df.rename(columns={'win': 'win_rate'}, inplace=True)

plt.figure(figsize=(12, 6))
sns.lineplot(data=winrate_df, x='duration_bin', y='win_rate', hue='champion', marker='o')
plt.title("Champion Win Rate Over Game Time")
plt.xlabel("Game Time (Minutes, Binned)")
plt.ylabel("Win Rate")
plt.ylim(0, 1)
plt.grid(True)
plt.legend(title="Champion", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

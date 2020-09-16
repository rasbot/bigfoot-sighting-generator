import src.data_prep as dp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime
import src.data_prep as dp

reports = dp.import_data("data/data.json")
df = dp.create_df(reports)

with open("temp_environment.txt", "r") as f:
    env = f.read()
f.close()
with open("temp_observed.txt", "r") as f:
    obs = f.read()
f.close()
with open("temp_time_conditions.txt", "r") as f:
    tc = f.read()
f.close()

with open("data/states.json", "r") as f:
    states_data = json.load(f)

unique_states = np.unique(np.array(df["STATE"].dropna()))
idx = np.argwhere(unique_states == "(International)")
unique_states = np.delete(unique_states, idx)
unique_seasons = np.unique(np.array(df["SEASON"].dropna()))

state = np.random.choice(unique_states)
county = np.random.choice(states_data[state]["Counties"])
nearest_town = np.random.choice(states_data[state]["Nearest Town"])
nearest_road = np.random.choice(states_data[state]["Nearest Road"])
season = np.random.choice(unique_seasons)

sighting_d = { str(datetime.now()): 
        {"SEASON: ": season, 
        "STATE: ": state,
        "NEAREST TOWN: ": nearest_town,
        "NEAREST ROAD: ": nearest_road,
        "ENVIRONMENT: ": env,
        "TIME AND CONDITIONS: ": tc,
        "OBSERVATION: ": obs}
        }

with open("generated_sightings.json", "a") as f:
        with open("generated_sightings.json") as f:
            data = json.load(f)
        data.update(sighting_d)
        with open("generated_sightings.json", "w") as f:
            json.dump(data, f, indent=4, sort_keys=False)
f.close()

with open("generated_sightings.json") as f:
    data = json.load(f)

# key of the newest entry
latest_key = sorted(data.keys())[-1]

latest_sighting = data[latest_key]

sighting_info = """SEASON: {season}

STATE: {state}

NEAREST TOWN: {nearest_town}

NEAREST ROAD: {nearest_road}

ENVIRONMENT: {env}

TIME AND CONDITIONS: {tc}

""".format(season=latest_sighting["SEASON: "], state=latest_sighting["STATE: "], nearest_town=latest_sighting["NEAREST TOWN: "], nearest_road=latest_sighting["NEAREST ROAD: "], env=latest_sighting["ENVIRONMENT: "], tc=latest_sighting["TIME AND CONDITIONS: "])

observation = """OBSERVATION: {obs}""".format(obs=latest_sighting["OBSERVATION: "])

print(sighting_info)
print(observation)
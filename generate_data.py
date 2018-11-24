import random

moods = ["rad", "good", "meh", "bad", "awful"]
weathers = ["cloudly", "sunny", "rainy", "foggy", "partly sunny"]

def generate_data_for_users(nr_users, nr_days):
    data_users = []
    for nth_user in range(nr_users):
        user_data = []
        for nth_day in range(nr_days):
            previous_config = config = None
            for hour in range(24):
                previous_config = config
                config = generate_data(hour, previous_config)
                user_data.append(config)
        data_users.append(user_data)
    return data_users


def generate_data(hour, previous_config):
    print(hour, previous_config)
    wake_up = 6 + random.randint(-1, 1)
    sleepy_time = 22 + random.randint(-1, 1)
    if hour <= wake_up or hour >= sleepy_time:
        activity = "sleep"
    elif hour > wake_up and hour <= 12:
        activity = "work"
    else:
        activity = random.choice(
            tuple({
                "training": True, "movies": False, "reading": True,
                "programming": False, "girlfriend time": True,
                "work": True, "relax": True, "friends": True, "sleeping": True,
                "coffee": False, "good meal": True, "hangout with friends": True
            }.keys())
        )
    if hour == 0:
        mood = random.choice(moods)
    else:
        previous_mood = previous_config["mood"]
        if previous_mood == "awful":
            mood = moods[moods.index(previous_mood) + random.randint(-1, 0)]
        elif previous_mood == "rad":
            mood = moods[moods.index(previous_mood) + random.randint(0, 1)]
        else:
            mood = moods[moods.index(previous_mood) + random.randint(-1, 1)]

    weather = random.choice(["cloudly", "sunny", "rainy", "foggy", "partly sunny"])

    daily_heat = 15 + random.randint(-10, 10)

    temperature = daily_heat if 11 <= hour <= 16 else daily_heat / 3 * 2

    return {"hour": hour, "activity": activity, "mood": mood, "weather": weather, "temperature": temperature}


import json
import pandas as pd

df = pd.DataFrame(generate_data_for_users(10, 1000))
print(df)

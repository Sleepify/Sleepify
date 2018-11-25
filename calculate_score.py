import json
import random
from collections import defaultdict


# Temp
HIGH_TEMP = 25
NORMAL_TEMP = 15
LOW_TEMP = 1

# Mood
BAD_MOOD = ["bad", "awful"]
NORMAL_MOOD = ["meh"]

# Weather
BAD_WEATHER = ["foggy", "rainy"]
NORMAL_WEATHER = ["cloudly", "partly sunny"]


def predict_score(hour, activity, temperature, mood, weather):
    if activity == "sleeping" or activity == "sleep":
        return 1
    if activity == "work":
        return predict_work(hour, temperature, mood, weather)
    if activity == "training":
        return predict_training(hour, temperature, mood, weather)
    if activity == "coffee":
        return predict_coffee(hour, temperature, mood, weather)
    if activity == "movies":
        return predict_movies(hour, temperature, mood, weather)
    if activity == "reading":
        return predict_reading(hour, temperature, mood, weather)
    if activity == "programming":
        return predict_programming(hour, temperature, mood, weather)
    if activity == "girlfriend hour":
        return predict_girlfriend(hour, temperature, mood, weather)
    if activity == "relax":
        return predict_relax(hour, temperature, mood, weather)
    if activity == "friends" or activity == "hangout with friends":
        return predict_friends(hour, temperature, mood, weather)
    if activity == "good meal":
        return predict_meal(hour, temperature, mood, weather)

#############################
#    GENERAL PREDICTION     #
#############################


def predict_mood(mood, score):
    if mood in NORMAL_MOOD:
        return score * getRandom(60, 70)
    elif mood in BAD_MOOD:
        return score * getRandom(40, 60)
    return score


def predict_weather(weather, score):
    if weather in BAD_WEATHER:
        return score * getRandom(10, 30)
    elif weather in NORMAL_WEATHER:
        return score * getRandom(40, 60)
    return score


def getRandom(start, stop):
    return random.randrange(start, stop) / 100

def predict(hour, temperature, mood, weather, early_hour=range(1, 8), late_hour=range(18, 24)):
    score = 1

    if hour in early_hour:
        score = score * getRandom(60, 70)
    elif hour in late_hour:
        score = score * -1

    score = predict_mood(mood, score)
    score = predict_weather(weather, score)
    if NORMAL_TEMP <= int(temperature) <= HIGH_TEMP:
        score = score * 1
    else:
        score = score * getRandom(70, 80)
    return score


#############################
#    SPECIFIC PREDICTION    #
#############################

# WORK
def predict_work(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather)

# TRAINING
def predict_training(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather, early_hour=range(1, 10), late_hour=range(20, 24))

# coffee
def predict_coffee(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather, early_hour=range(1, 4), late_hour=range(16, 24))


# movies
def predict_movies(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather, early_hour=range(1, 14), late_hour=range(22, 24))

# reading
def predict_reading(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather, early_hour=range(1, 14), late_hour=range(22, 24))

# programming
def predict_programming(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather, early_hour=range(1, 6), late_hour=range(20, 24))

# girlfriend
def predict_girlfriend(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather, early_hour=range(1, 8), late_hour=range(22, 24))

# relax
def predict_relax(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather, early_hour=range(1, 12), late_hour=range(24, 24))

# friends
def predict_friends(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather, early_hour=range(1, 10), late_hour=range(22, 24))

# meal
def predict_meal(hour, temperature, mood, weather):
    return predict(hour, temperature, mood, weather, early_hour=range(1, 8), late_hour=range(23, 24))


if __name__ == "__main__":

    with open("train.json", "r") as f:
        data = json.loads(f.read())

    full_data = []
    for user_days in data:
        user_data = []
        for day in user_days:
            day_data = []
            for hour in day:
                hour["score"] = predict_score(**hour)
                day_data.append(hour)
            user_data.append(day_data)
        full_data.append(user_data)

    import pandas as pd
    df = pd.DataFrame.from_records(day_data)
    df.to_csv("all_the_best_data.csv")

    # with open("Data/data.json", "w") as f:
    #     json.dump(full_data, f)

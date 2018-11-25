import json
import random


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

def predict_score(time, activity, temp, mood, weather):
    if activity == "sleeping" or activity == "sleep":
        return 1
    if activity == "work":
        return predict_work(time, temp, mood, weather)
    if activity == "training":
        return predict_training(time, temp, mood, weather)
    if activity == "coffee":
        return predict_coffee(time, temp, mood, weather)
    if activity == "movies":
        return predict_movies(time, temp, mood, weather)
    if activity == "reading":
        return predict_reading(time, temp, mood, weather)
    if activity == "programming":
        return predict_programming(time, temp, mood, weather)
    if activity == "girlfriend time":
        return predict_girlfriend(time, temp, mood, weather)
    if activity == "relax":
        return predict_relax(time, temp, mood, weather)
    if activity == "friends" or activity == "hangout with friends":
        return predict_friends(time, temp, mood, weather)
    if activity == "good meal":
        return predict_meal(time, temp, mood, weather)

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


def predict(time, temp, mood, weather, early_time=range(1, 8), late_time=range(18, 24)):
    score = 1

    if time in early_time:
        score = score * getRandom(60, 70)
    elif time in late_time:
        score = score * -1

    score = predict_mood(mood, score)
    score = predict_weather(weather, score)
    if NORMAL_TEMP <= int(temp) <= HIGH_TEMP:
        score = score * 1
    else:
        score = score * getRandom(70, 80)
    return score


#############################
#    SPECIFIC PREDICTION    #
#############################

# WORK
def predict_work(time, temp, mood, weather):
    return predict(time, temp, mood, weather)

# TRAINING
def predict_training(time, temp, mood, weather):
    return predict(time, temp, mood, weather, early_time=range(1, 10), late_time=range(20, 24))

# coffee
def predict_coffee(time, temp, mood, weather):
    return predict(time, temp, mood, weather, early_time=range(1, 4), late_time=range(16, 24))


# movies
def predict_movies(time, temp, mood, weather):
    return predict(time, temp, mood, weather, early_time=range(1, 14), late_time=range(22, 24))

# reading
def predict_reading(time, temp, mood, weather):
    return predict(time, temp, mood, weather, early_time=range(1, 14), late_time=range(22, 24))

# programming
def predict_programming(time, temp, mood, weather):
    return predict(time, temp, mood, weather, early_time=range(1, 6), late_time=range(20, 24))

# girlfriend
def predict_girlfriend(time, temp, mood, weather):
    return predict(time, temp, mood, weather, early_time=range(1, 8), late_time=range(22, 24))

# relax
def predict_relax(time, temp, mood, weather):
    return predict(time, temp, mood, weather, early_time=range(1, 12), late_time=range(24, 24))

# friends
def predict_friends(time, temp, mood, weather):
    return predict(time, temp, mood, weather, early_time=range(1, 10), late_time=range(22, 24))

# meal
def predict_meal(time, temp, mood, weather):
    return predict(time, temp, mood, weather, early_time=range(1, 8), late_time=range(23, 24))


if __name__ == "__main__":

    with open("train.json", "r") as f:
        data = json.loads(f.read())

    full_data = {}

    for i, user in enumerate(data):
        userName = "user-{}".format(i)
        full_data[userName] = []
        for j, day in enumerate(user):
            activity_per_day = {}
            for hour in day:
                time = hour.get("hour", "")
                activity = hour.get("activity", "")
                temperature = hour.get("temperature", "")
                mood = hour.get("mood", "")
                weather = hour.get("weather", "")

                score = predict_score(time, activity, temperature, mood, weather)
                if not score:
                    continue
                if activity not in activity_per_day:
                    activity_per_day[activity] = {}
                    activity_per_day[activity]["time"] = []
                    activity_per_day[activity]["score"] = []
                    activity_per_day[activity]["mood"] = []
                    activity_per_day[activity]["weather"] = []
                    activity_per_day[activity]["temperature"] = []
                activity_per_day[activity]["time"].append(time)
                activity_per_day[activity]["score"].append(score)
                activity_per_day[activity]["mood"].append(mood)
                activity_per_day[activity]["weather"].append(weather)
                activity_per_day[activity]["temperature"].append(temperature)
            full_data[userName].append(activity_per_day)

    with open("Data/data.json", "w") as file:
        json.dump(full_data, file)

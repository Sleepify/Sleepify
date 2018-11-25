import csv
import codecs
import json
import urllib.request

def month_MMM_to_MM(month):
    switcher = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    return switcher.get(month, "99")



with codecs.open('Data/daylio_data.csv', 'rU', 'utf-16') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    data = {}
    weather_dict = {}
    weather_history_list = {}

    with open('Data/weather_history_list.json') as weather_json:
        weather_history_list = json.load(weather_json)

    for row in reader:
        hasNew = False

        # Retrieve day number from the date column (ex: 1 from 1-Sep and 30 from 30-Sep)
        day = row['date'][:row['date'].find("-")]

        if row['date'].find("-") == 1:
            day = "0" + day
        
        # Retrieve the hour from the time column (ex: 1 from 1:23 and 12 from 12:34)
        hour = row['time'][:row['time'].find(":")]

        if row['time'].find(":") == 1:
            hour = "0" + hour

        # Retrieve the month number from the date column (ex: 30-Sep > Sep > 09)
        month_MMM = row['date'][-3:]
        month_MM = month_MMM_to_MM(month_MMM)

        # Start building the generated JSON file from here onward
        # Create year level
        if row['year'] not in data:
            data[row['year']] = {}

        year_root = data[row['year']]

        # Create month level
        if month_MM not in year_root:
            year_root[month_MM] = {}

        month_root = year_root[month_MM]

        # Create day level
        if day not in month_root:
            month_root[day] = {}
        
        day_root = month_root[day]

        # Create hour level
        if hour not in day_root:
            day_root[hour] = {'activities': {}}
        
        hour_root = day_root[hour]
        hour_root['mood'] = row['mood']

        # Activities in the daylio file are exported as a list separated by " | "
        # f.e.: Work (employment) | Networking | Reading | Programming / Server | Miracle morning | Girlfriend time
        for activity in row['activities'].split(" | "):
            hour_root['activities'][activity.lower()] = True

        timestamp_yyyymmdd = row['year'] + month_MM + day
        timestamp_yyyymmddhh = row['year'] + month_MM + day + hour

        # Already entry for this YYYYMMDDHH processed before? So for example Daylio entry for same day and same hour as already processed, but half hour later
        if timestamp_yyyymmddhh not in weather_dict:
            try:
                # Already retrieved weather data in the past for this date? If not, retrieve it from the Weather Underground API and store it for later in the history list JSON file
                if timestamp_yyyymmdd not in weather_history_list:
                    with urllib.request.urlopen("https://api.wunderground.com/api/41e8f2f12e558b69/history_" + timestamp_yyyymmdd + "/q/ch/Basel.json") as url:
                        print("Called API for date " + timestamp_yyyymmdd)
                        weather_data = json.loads(url.read().decode())
                        weather_history_list[timestamp_yyyymmdd] = weather_data
                        hasNew = True
                else:
                    weather_data = weather_history_list[timestamp_yyyymmdd]
                    hasNew = False

                # Add retrieved data in the dict for later use
                for observation in weather_data['history']['observations']:
                    timestamp_yyyymmddhh = observation['date']['year'] + observation['date']['mon'] + observation['date']['mday'] + observation['date']['hour']
                    weather_dict[timestamp_yyyymmddhh] = {'temperature_celsius': observation['tempm'], 'conds': observation['conds'], 'icon': observation['icon']}
    
                pass
            except KeyError:
                print("API Error - Key Missing")
                pass
            finally:
                # Store newly retrieved data in the history list JSON
                if hasNew == True:
                    with open('Data/weather_history_list.json','w') as weather_json:
                        weather_json.write(json.dumps(weather_history_list, sort_keys=True))
                pass

            
        timestamp_yyyymmddhh = row['year'] + month_MM + day + hour
        hour_root['weather'] = weather_dict[timestamp_yyyymmddhh]['conds']
        hour_root['temperature_celsius'] = weather_dict[timestamp_yyyymmddhh]['temperature_celsius']
        # ICON URL: https://icons.wxug.com/i/c/a/<ICON>.gif
        hour_root['icon'] = weather_dict[timestamp_yyyymmddhh]['icon']


    json_data = json.dumps(data, sort_keys=True)

    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    with open('Data/sleepify_data.json','w') as sleepify_json:
        sleepify_json.write(json_data)
        print("File Data/sleepify_data.json created/updated!")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
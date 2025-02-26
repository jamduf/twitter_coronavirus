#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True)
parser.add_argument('--output_path', required=True)
args = parser.parse_args()

# imports
import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

#manually inputting days in each month since it would break otherwise
days_in_month = {
    "01": 31, "02": 29, "03": 31, "04": 30, "05": 31, "06": 30,
    "07": 31, "08": 31, "09": 30, "10": 31, "11": 30, "12": 31
}

# Month labels for x-axis
month_labels = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun",
    "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
}

# helper function to convert month and day to day of the year via datetime
def get_day_of_year(month, day):
    try:
        day = int(day)
        #checking if files are not valid dates
        if day < 1 or day > days_in_month.get(month, 31):
            #throws error instead of stopping process
            raise ValueError(f"Invalid day {day} for month {month}")
        
        date_str = f"2023-{month}-{day:02d}"
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.timetuple().tm_yday
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

# initialize data structure
hashtag_counts = defaultdict(lambda: defaultdict(int))

# scan through output files
for filename in os.listdir('outputs'):
    if filename.endswith('.lang') or filename.endswith('.country'):
        filepath = os.path.join('outputs', filename)
        with open(filepath,encoding='utf-8-sig') as f:
            data = json.load(f)
            month = filename.split('-')[1]
            day = filename.split('-')[2][:2]  
            day_of_year = get_day_of_year(month,day)
            if day_of_year is None:
                continue
            for hashtag in args.hashtags:
                if hashtag in data:
                    hashtag_counts[hashtag][day_of_year] += sum(data[hashtag].values())

# sort days and prepare plot data
days = sorted(set(day for counts in hashtag_counts.values() for day in counts))

# plot
plt.figure(figsize=(10, 6))
for hashtag, counts in hashtag_counts.items():
    counts_by_day = [counts.get(day, 0) for day in days]
    plt.plot(days, counts_by_day, label=hashtag)

# Set x-axis to be months, otherwise not readable / rational
month_ticks = [get_day_of_year(month, "01") for month in days_in_month.keys()]
month_names = [month_labels[month] for month in days_in_month.keys()]
plt.xticks(month_ticks, month_names)

#Labelling
plt.xlabel('Month')
plt.ylabel('Tweet Count')
plt.title('Hashtag Usage Over Time')
plt.legend()
plt.savefig(args.output_path)
print(f"Saved plot as {args.output_path}")

#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
#items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
#for k,v in items:
#    print(k,':',v)

#sort and get top 10
items = sorted(counts[args.key].items(), key=lambda item: (item[1], item[0]), reverse=True)[:10]

#separate
keys = [k for k, v in items]
values = [v for k, v in items]

if "lang" in args.input_path:
    data_type = "lang"
elif "country" in args.input_path:
    data_type = "country"
else:
    data_type = "unknown"
    
#plot
plt.figure(figsize=(10,6))
plt.bar(keys, values)
plt.gca().invert_xaxis()
plt.xlabel(f'Keys ({args.key})')
plt.ylabel(f'Values ({data_type})')
plt.title(f'Top 10 for {args.key} ({data_type})' )

# save the plot
output_filename = f"{args.key.strip('#')}_{data_type}.png"
plt.savefig(output_filename)
print(f"Saved plot as {output_filename}")

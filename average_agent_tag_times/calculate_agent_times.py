import json
import pandas as pd
import os
import csv

#load the tags and agent ids
tags = []
with open('tags2.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		tags.append(row[0])


agent_ids = []
with open('agent_ids.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		agent_ids.append(float(row[0]))
agent_ids.append(float('nan'))		

#load all the data into a df
folder = 'data'

i = 0
for file in os.listdir(folder):
    print(file)
    path = 'data/'+file
    if i == 0:
        df = pd.read_json(path)[['metric_sets_first_resolution_time_in_minutes_calendar',
                                  'tickets_tags', 'tickets_assignee_id', 'tickets_subject', 'tickets_group_id']]
    else:
        temp = pd.read_json(path)[['metric_sets_first_resolution_time_in_minutes_calendar',
                                      'tickets_tags', 'tickets_assignee_id', 'tickets_subject', 'tickets_group_id']]
        df = pd.concat([df,temp], ignore_index = True)
    i += 1


agent_times = pd.DataFrame(index = agent_ids, columns = tags)
agent_times = agent_times.fillna(0)

agent_counts = pd.DataFrame(index = agent_ids, columns = tags)
agent_counts = agent_counts.fillna(0)

for index, row in df.iterrows():
    row_tags = row['tickets_tags'].split()
    for tag in row_tags:
        print(row['tickets_assignee_id'])
        agent_times.loc[(row['tickets_assignee_id']), tag] = row['metric_sets_first_resolution_time_in_minutes_calendar']
        agent_counts.loc[(row['tickets_assignee_id']), tag] += 1

with open('agent_times2.csv', 'w') as f:
    agent_times.to_csv(f)
    
with open('agent_counts2.csv', 'w') as f:
    agent_counts.to_csv(f)        

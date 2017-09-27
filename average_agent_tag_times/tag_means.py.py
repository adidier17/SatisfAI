import json
import pandas as pd

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

#create a list of all the unique tags
tag_str = ''
for i in range(0, len(df)):
    tag_str = tag_str + df.loc[i]['tickets_tags']
temp = tag_str.split(' ')
tags = set(temp)
print(tags)    


import csv
with open('tags.csv', 'w') as f:
    writer = csv.writer(f)
    for tag in tags:
        writer.writerow([tag])
		
#tag: [resolution time, number of appearance]
tag_counts = {word:[0,0] for word in tags}

print(tag_counts)

#in each row of the df, tokenize the tags and add them to the tags list if they don't already exist, then increment each word's count
for i in range(0, len(df)):
    tag_list = df.loc[i]['tickets_tags'].split() #tokenize the tags column
    for word in tag_list:
        if word not in tag_counts:
            tag_counts[word] = [0,0]
        tag_counts[word][0] += df.loc[i]['metric_sets_first_resolution_time_in_minutes_calendar']
        tag_counts[word][1] += 1


#calculate mean resolution time and sort
print(tag_counts['i_need_to_edit_or_cancel_an_order'])	


for key, value in tag_counts.items():
    if counts[key][1] != 0:
        avg = tag_counts[key][0]/tag_counts[key][1]
        tag_counts[key].append(avg)
    else tag_counts[key].append(0) ####BUT EVERY WORD SHOULD HAVE A COUNT OF AT LEAST 1
	
	
	
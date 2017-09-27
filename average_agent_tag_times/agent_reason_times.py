import os
import pandas as pd
import csv
#load all the data into a df
folder = 'data'
i = 0
for file in os.listdir(folder):
    print(file)
    path = 'data/'+file
    if i == 0:
        df = pd.read_json(path)
    else:
        temp = pd.read_json(path)
        df = pd.concat([df,temp], ignore_index = True)
    i += 1


#load agent ids
agent_ids = []
with open('agent_ids.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		agent_ids.append(float(row[0]))
agent_ids.append(float('nan'))	

#load contact reasons
contact_reasons = []
with open('contact_reasons.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        contact_reasons.append(row[0])

agent_times = pd.DataFrame(index = agent_ids, columns = contact_reasons)
agent_times = agent_times.fillna(0)        
agent_counts = pd.DataFrame(index = agent_ids, columns = contact_reasons)
agent_counts = agent_counts.fillna(0)


import multiprocessing

# create as many processes as there are CPUs on your machine
num_processes = multiprocessing.cpu_count()

# calculate the chunk size as an integer
chunk_size = int(df.shape[0]/num_processes)

# will work even if the length of the dataframe is not evenly divisible by num_processes
chunks = [df.iloc[df.index[i:i + chunk_size]] for i in range(0, df.shape[0], chunk_size)]

def calc_times(df):
    for index, row in df.iterrows():
        reason = row['tickets_custom_field_22526998']
        print(reason)
        if isinstance(reason,str):
            #== 'float' or not math.isnan(reason):
            print(row['tickets_assignee_id'])
            print(reason)
            try:
                agent_times.loc[row['tickets_assignee_id'],reason] =  row['metric_sets_first_resolution_time_in_minutes_calendar']
                agent_counts.loc[row['tickets_assignee_id'], reason] += 1
            except Exception as e:
                pass

# create our pool with `num_processes` processes
pool = multiprocessing.Pool(processes=num_processes)

# apply our function to each chunk in the list
pool.map(calc_times, chunks)
pool.close()
pool.join()

#write results to file
with open('agent_reason_times.csv', 'w') as f:
	agent_times.to_csv(f)

with open('agent_reason_counts.csv', 'w') as f:
	agent_counts.to_csv(f)

#calculate agent means and differences from the tag mean

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
#load agent times and counts 

with open('agent_times2.csv', 'r') as f:
	agent_times = pd.read_csv(f, index_col = 0)

with open('agent_counts2.csv', 'r') as f:
	agent_counts = pd.read_csv(f, index_col = 0)


#replace 0's with nan so we don't get a divide by 0 error
def replace0(x):
	if x == 0:
		return float('nan')
	else:
		return x 

agent_counts.applymap(replace0)

#compute agent means
agent_means = agent_times.divide(agent_counts)

with open('agent_means.csv', 'w') as f:
	agent_means.to_csv(f)

#load tag means and compute agent difference from each tag mean
import ast
generic = lambda x: ast.literal_eval(x)
conv = {'means': generic}

with open('tag_means.csv', 'r') as f:
	tag_means = pd.read_csv(f, index_col = 0, names = ['tags', 'means'], converters = conv)

tag_means['means'] = tag_means['means'].apply(lambda x: x[2])

tag_means_series = tag_means.transpose().squeeze()

agent_diffs = agent_means.sub(tag_means_series, 1)

with open('agent_diffs.csv', 'w') as f:
	agent_diffs.to_csv(f)

#heatmap of agents/tags
subset = agent_diffs.iloc[0:50,0:50]
sns.heatmap(agent_diffs, xticklabels = False, yticklabels = False)
heatmap = plt.gcf()
plt.show()
heatmap.savefig('agent_diffs.png')
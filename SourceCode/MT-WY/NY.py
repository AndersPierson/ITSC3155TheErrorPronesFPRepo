import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import re

# Load CSV file from Datasets folder
df = pd.read_csv('Datasets/alldata.csv')
df.head()

# Drop column Review from the data
df.drop(columns = 'reviews', inplace = True)

# Filtered the data set to remove the rest of the rows containing NaNs value
df.drop(index = df[df['position'].isnull()].index, inplace = True)
df.isnull().any()

# Create city and state columns to better aggregate the data
df['location'] = df.location.apply(lambda x: re.sub('\d*','',str(x)))
df['city'] = df.location.apply(lambda x: x.split(',')[0].strip())
df['state'] = df.location.apply(lambda x: x.split(',')[1].strip())
df['location'] = df['city']+ ', ' + df['state']
df.head()

# Filtering to correct state
filtered_df = df[df['state'] == 'NY']

# Creating sum of number of cases group by city
new_df = filtered_df.groupby(['city'])['position'].count().reset_index()

# Sorting values and select first 20 states
new_df = new_df.sort_values(by=['position'], ascending=[False])

# Preparing data
data = [go.Bar(x=new_df['city'], y=new_df['position'])]

# Preparing layout
layout = go.Layout(title='Available Positions in New York by City', xaxis_title="Cities",
                   yaxis_title="Number of Positions")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='Ny.html')
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import re

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/alldata.csv')

app = dash.Dash()

# Drop column Review from the data
df.drop(columns = 'reviews', inplace = True)

# Filtered the data set to remove the rest of the rows containing NaNs value
df.drop(index = df[df['position'].isnull()].index, inplace = True)
df.isnull().any()

# Create city and state columns to better aggregate the data
df['location'] = df.location.apply(lambda x: re.sub('\d*','',str(x)))
df['city'] = df.location.apply(lambda x: x.split(',')[0].strip())
df['state'] = df.location.apply(lambda x: x.split(',')[1].strip())
df['location'] = df['city'] + ', ' + df['state']

# Bar chart data
barchart_df = df.groupby(['state'])['position'].count().reset_index()
barchart_df = barchart_df.sort_values(by=['position'], ascending=[False])
data_barchart = [go.Bar(x=barchart_df['state'], y=barchart_df['position'])]

# Bar chart data2
barchart2_df = df.groupby(['location'])['position'].count().reset_index()
barchart2_df = barchart2_df.sort_values(by=['position'], ascending=[False]).head(20)
data_barchart2 = [go.Bar(x=barchart2_df['location'], y=barchart2_df['position'])]

# Layout
app.layout = html.Div(style={'background-color': '#64485C'}, children=[
    html.Br(),
    html.H1(children='Data Scientist Job Availability Visualization',
            style={
                'textAlign': 'center',
                'color': '#ffffff'
            }
            ),
    html.Br(),
    html.Hr(style={'color': '#64485C'}),
    html.H3('Overview', style={'color': '#ffffff', 'textAlign': 'center', 'margin': '10px', 'font-size': '26px'}),
    html.Div('Data science jobs can be a pain to track down. This is why we have compiled and visualized an easy'
             ' to understand data-set that tracks data science positions all over the U.S. Our goal is to help '
             'data scientist easily locate employment hot-spots in the data science field. '
             'The various graphs below will give you a great understanding on where the best places to look for '
             'employment are.', style={'color': '#ffffff', 'margin':'10px', 'font-size': '18px'}),
    html.Br(),
    html.H3('Positions by State', style={'color': '#ffffff', 'textAlign': 'left', 'margin': '10px', 'font-size': '26px'}),
    html.Div('Number of available positions by state in the U.S.', style={'color': '#ffffff', 'margin':'10px', 'font-size': '18px'}),
    dcc.Graph(id='graph1',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Positions by State',
                                      xaxis={'title': 'States'}, yaxis={'title': 'Number of Positions'})
              }
              ),
    html.Br(),
    html.H3('Top Cities', style={'color': '#ffffff', 'textAlign': 'left', 'margin': '10px', 'font-size': '26px'}),
    html.Div('The top 20 cities in the country offering the most data science positions.', style={'color': '#ffffff',
                                                                                                  'margin': '10px',
                                                                                                  'font-size': '18px'}),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart2,
                  'layout': go.Layout(title='Top 20 Cities',
                                      xaxis={'title': 'Cities'}, yaxis={'title': 'Number of Positions'})
              }
              ),
    html.Br(),
    html.H3('Positions by City', style={'color': '#ffffff', 'textAlign': 'left', 'font-size': '26px'}),
    html.Div('This interactive bar chart holds data for the amount of available data science positions in '
             'any given state of your choice, organized by city. By selecting a'
             ' state and hovering over a city, you can view the amount of open positions. These positions vary in'
             ' job description, however, they all fall under the data science category.'
             ' If there is a state you are looking for that is not an option on the drop-down menu. That means we had'
             ' very little data for those locations and they most likely do not offer a lot of job opportunities',
             style={'color': '#ffffff', 'margin': '10px', 'font-size': '18px'}),
    html.Br(),
    dcc.Graph(id='graph3'),
    html.Div('Please select a State', style={'color': '#ffffff', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-state',
        options=[
            {'label': 'California', 'value': 'CA'},
            {'label': 'Colorado', 'value': 'CO'},
            {'label': 'Georgia', 'value': 'GA'},
            {'label': 'Illinois', 'value': 'IL'},
            {'label': 'Massachusetts', 'value': 'MA'},
            {'label': 'District of Columbia', 'value': 'DC'},
            {'label': 'Washington', 'value': 'WA'},
            {'label': 'New York', 'value': 'NY'},
            {'label': 'Texas', 'value': 'TX'},
            {'label': 'New Jersey', 'value': 'NJ'},
        ],
        value='CA'
    ),
    html.Br(),
    html.Br()
])


@app.callback(Output('graph3', 'figure'),
              [Input('select-state', 'value')])
def update_figure(selected_state):
    filtered_df = df[df['state'] == selected_state]

    new_df = filtered_df.groupby(['city'])['position'].count().reset_index()
    new_df = new_df.sort_values(by=['position'], ascending=[False])
    data = [go.Bar(x=new_df['city'], y=new_df['position'], width=.5)]
    return {'data': data, 'layout': go.Layout(title='Positions in ' + selected_state + ' by City', xaxis_title="Cities",
                                              yaxis_title="Number of Positions")}


if __name__ == '__main__':
    app.run_server()
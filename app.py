import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('ProcessedTweets.csv')

# Create Dash app
app = dash.Dash(__name__)
server = app.server
# Define app layout
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': month, 'value': month} for month in df['Month'].unique()],
                value=df['Month'].unique()[0]
            ),
        ], style={'width': '33%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label('Sentiment Score'),
            dcc.RangeSlider(
                id='sentiment-slider',
                min=df['Sentiment'].min(),
                max=df['Sentiment'].max(),
                step=0.1,
                value=[df['Sentiment'].min(), df['Sentiment'].max()],
                marks={i: str(i) for i in range(-1, 2)}
            ),
        ], style={'width': '33%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label('Subjectivity Score'),
            dcc.RangeSlider(
                id='subjectivity-slider',
                min=df['Subjectivity'].min(),
                max=df['Subjectivity'].max(),
                step=0.1,
                value=[df['Subjectivity'].min(), df['Subjectivity'].max()],
                marks={i/10: str(i/10) for i in range(11)}
            ),
        ], style={'width': '33%', 'display': 'inline-block'}),
        
    ], style={'margin-bottom': '20px'}),
    
    dcc.Graph(id='scatter-plot', config={'editable': True, 'toImageButtonOptions': {'filename': 'scatter-plot', 'height': None, 'width': None, 'scale': 2}}),
    
    html.Div([
        html.Div([
            html.Label('Raw Tweets', style={'text-align': 'center', 'background-color': 'rgba(169, 169, 169, 0.5)', 'padding': '5px'})
        ], style={'width': '100%', 'text-align': 'center'})
    ]),
    
    html.Table(id='tweet-table', style={'text-align': 'center'})
])

# Define callback to update scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('sentiment-slider', 'value'),
     Input('subjectivity-slider', 'value')]
)
def update_scatter_plot(selected_month, sentiment_range, subjectivity_range):
    filtered_df = df[(df['Month'] == selected_month) &
                     (df['Sentiment'] >= sentiment_range[0]) &
                     (df['Sentiment'] <= sentiment_range[1]) &
                     (df['Subjectivity'] >= subjectivity_range[0]) &
                     (df['Subjectivity'] <= subjectivity_range[1])]
    
    fig = px.scatter(filtered_df, x='Dimension 1', y='Dimension 2', hover_data=['RawTweet'])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      xaxis_title='',
                      yaxis_title='')
    return fig

# Define callback to update tweet table
@app.callback(
    Output('tweet-table', 'children'),
    [Input('scatter-plot', 'selectedData')]
)
def update_tweet_table(selected_data):
    if selected_data is None:
        return []
    else:
        selected_indices = [point['pointIndex'] for point in selected_data['points']]
        selected_tweets = df.iloc[selected_indices]['RawTweet']
        table_rows = [html.Tr([html.Td(tweet)]) for tweet in selected_tweets]
        return table_rows

if __name__ == '__main__':
    app.run_server(debug=True)

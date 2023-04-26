import dash
from dash import dcc
from dash import html
import requests
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)

# Data from New York Times API
url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key=y4M9uNWA5lFsGGFZshCNGfgJgAkwsGva"
#  For the lab I used an API key, Which I have deleted now to recreate just replace API_KEY_NYT with your API key according to line below
# url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key=API_KEY_NYT"
response = requests.get(url)
data = response.json()
df = pd.json_normalize(data['results']['books'])
print(df.columns)

# Plotly bar chart for top 7 bestsellers
fig = px.bar(df.head(7), x='title', y='weeks_on_list', color='rank',
             title='New York Times Best Sellers - Hardcover Fiction',
             text='rank', hover_data=['author', 'publisher', 'description'],
             width=1300, height=700, color_continuous_scale='viridis',
             labels = {'title':'Title', 'weeks_on_list':'Weeks on List', 'rank':'Rank', 'author':'Author', 'publisher':'Publisher', 'description':'Description'})

fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.8)

app.layout = html.Div(children=[
    
    
    html.H1(children='Book Details'),
    
    dcc.Dropdown(
        id='book-dropdown',
        options=[{'label': book['title'], 'value': book['title']} for book in data['results']['books']],
        value='The Four Winds'
    ),
    
    html.Div(id='book-details'),

    html.H2(children='New York Times Best Sellers'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
])

@app.callback(
    dash.dependencies.Output('book-details', 'children'),
    [dash.dependencies.Input('book-dropdown', 'value')])
def update_book_details(value):
    book = next(book for book in data['results']['books'] if book['title'] == value)
    return html.Table([
        html.Tr([html.Th('Title'), html.Td(book['title'])]),
        html.Tr([html.Th('Author'), html.Td(book['author'])]),
        html.Tr([html.Th('Publisher'), html.Td(book['publisher'])]),
        html.Tr([html.Th('Weeks on List'), html.Td(book['weeks_on_list'])]),
        html.Tr([html.Th('Description'), html.Td(book['description'])])
    ])

if __name__ == '__main__':
    app.run_server(debug=True)

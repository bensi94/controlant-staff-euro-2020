from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

app = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash_app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    server=app,
    url_base_pathname='/'
)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

dash_app.layout = html.Div(children=[
    html.H1(children='Controlant Euro 2020', style={'textAlign': 'center'}),
    html.Div(children='Betting competition statistics', style={'textAlign': 'center'}),
    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])


@app.route('/')
def euro_site():
    return dash_app.index()


if __name__ == '__main__':
    app.run()

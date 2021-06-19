import json

import dash
import dash_html_components as html
import dash_table


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
#
# def build_dash():
#     # assume you have a "long-form" data frame
#     # see https://plotly.com/python/px-arguments/ for more options
#
#
#     return html.Div(
#         children=[
#             html.H1(children="Hello Dash"),
#             html.Div(
#                 children=f"Dash: A web application framework for Python. {datetime.now()}"
#             ),
#             table
#         ]
#     )
#
#
with open('data.json', 'r') as f:
    data = json.loads(f.read())
    formatted_data = sorted([
        {
            **{'Name': key},
            **{
                inner_key: (', '.join(inner_value) if isinstance(inner_value, list) else inner_value)
                for inner_key, inner_value in value.items()
            }
        }
        for key, value in data.items()
    ], key=lambda k: k['Name'])


app.layout = html.Div(
    [
        dash_table.DataTable(
            id='table',
            columns=[{"name": column, "id": column} for column in formatted_data[0].keys()],
            data=formatted_data,
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left',
                'font-family': 'sans-serif'
            },
        )
    ]
)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)

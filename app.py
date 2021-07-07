import json

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

from utils import format_table_data, get_points_table

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

with open("data.json", "r") as f:
    data = json.loads(f.read())


def build_dash():
    formatted_data = format_table_data(data)
    points_table = get_points_table(data)

    df = pd.DataFrame(points_table)

    fig = px.bar(df, x="Name", y="Total points", color="Name")

    return html.Div(
        [
            html.Br(),
            dbc.Container(
                [
                    dbc.Row(
                        [
                            html.H1(
                                children="Controlant staff, Euro 2020 competition "
                            ),
                            html.Div(
                                children="Warning: The points shown are not final and "
                                "will change if and when competition results change"
                            ),
                        ],
                        justify="center",
                        align="center",
                    ),
                    html.Br(),
                    dcc.Graph(id="points-graph", figure=fig),
                    html.Br(),
                    html.H3(
                        children="Last updated 7/07 13:50 after Italy - Spain match"
                    ),
                    html.Br(),
                    html.Br(),
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th(column)
                                        for column in points_table[0].keys()
                                    ]
                                )
                            )
                        ]
                        + [
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td(value)
                                            for value in point_dict.values()
                                        ]
                                    )
                                    for point_dict in points_table
                                ]
                            )
                        ],
                        bordered=True,
                        striped=True,
                        responsive=True,
                        hover=True,
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th(column)
                                        for column in formatted_data[0].keys()
                                    ]
                                )
                            )
                        ]
                        + [
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td(value)
                                            for value in choose_dict.values()
                                        ]
                                    )
                                    for choose_dict in formatted_data
                                ]
                            )
                        ],
                        bordered=True,
                        striped=True,
                        responsive=True,
                        hover=True,
                    ),
                ]
            ),
        ]
    )


app.layout = build_dash
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)

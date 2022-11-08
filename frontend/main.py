import requests
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, State, Output


API = "http://127.0.0.1:8000"

BC = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"
app = Dash(__name__, external_stylesheets=[BC])

form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Longtitude", html_for="longtitude"),
                        dbc.Input(
                            type="number",
                            step="0.01",
                            id="longtitude",
                            required=True,
                            value="-115.73",
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dbc.Label("Latitude", html_for="latitude"),
                        dbc.Input(
                            type="number",
                            step="0.01",
                            id="latitude",
                            required=True,
                            value="33.35",
                        ),
                    ],
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            [
                dbc.Label("Housing median age", html_for="housing-median-age"),
                dbc.Input(
                    type="number", id="housing-median-age", required=True, value="23"
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Total rooms", html_for="total-rooms"),
                        dbc.Input(
                            type="number", id="total-rooms", required=True, value="1586"
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dbc.Label("Total bedrooms", html_for="total-bedrooms"),
                        dbc.Input(
                            type="number",
                            id="total-bedrooms",
                            required=True,
                            value="448",
                        ),
                    ],
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            [
                dbc.Label("Population", html_for="population"),
                dbc.Input(type="number", id="population", required=True, value="338"),
            ],
            className="mb-3",
        ),
        html.Div(
            [
                dbc.Label("Households", html_for="households"),
                dbc.Input(type="number", id="households", required=True, value="182"),
            ],
            className="mb-3",
        ),
        html.Div(
            [
                dbc.Label("Median income", html_for="median-income"),
                dbc.Input(
                    type="number", id="median-income", required=True, value="1.2132"
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            [
                dbc.Label("Ocean proximity", html_for="dropdown"),
                dcc.Dropdown(
                    id="ocean-proximity",
                    options=[
                        {"label": "Inland", "value": 1},
                        {"label": "Near ocean", "value": 2},
                        {"label": "Near bay", "value": 3},
                        {"label": "Less than 1 hour", "value": 0},
                        {"label": "Island", "value": 4},
                    ],
                    value=1,
                    clearable=False,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Strong("Predicted price:"),
                    ],
                ),
                dbc.Col([html.P("", id="price", className="text-end h3")]),
            ],
            className="d-grid gap-2 d-md-flex justify-content-md-end mb-4",
        ),
        html.Div(
            [
                dbc.Button(
                    "Predict price", color="primary", className="me-1", id="predict"
                )
            ],
            className="d-grid gap-2",
        ),
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(),
                dbc.Col(
                    [html.H1("House prices", className="mb-4 mt-3"), form], width=3
                ),
            ]
        )
    ],
    fluid=True,
)


@app.callback(
    Output(component_id="price", component_property="children"),
    Input(component_id="predict", component_property="n_clicks"),
    {
        "longtitude": State(component_id="longtitude", component_property="value"),
        "latitude": State(component_id="latitude", component_property="value"),
        "housing_median_age": State(
            component_id="housing-median-age", component_property="value"
        ),
        "total_rooms": State(component_id="total-rooms", component_property="value"),
        "total_bedrooms": State(
            component_id="total-bedrooms", component_property="value"
        ),
        "population": State(component_id="population", component_property="value"),
        "households": State(component_id="households", component_property="value"),
        "median_income": State(
            component_id="median-income", component_property="value"
        ),
        "ocean_proximity": State(
            component_id="ocean-proximity", component_property="value"
        ),
    },
)
def predict_price(n_clicks, params):
    if n_clicks:
        response = requests.get(f"{API}/predict", params=params).json()
        predicted_price = response["price"]

        return f"$ {predicted_price:.2f}"

    return "$ NaN"


if __name__ == "__main__":
    app.run_server(debug=True)

import requests
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, html, dcc, Input, State, Output, dash_table, ctx


API = "http://127.0.0.1:8000"

app = Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"
    ],
)

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

model_request_table = html.Div(
    dash_table.DataTable(
        id="history",
        style_cell={
            "overflow": "hidden",
            "textOverflow": "ellipsis",
            "maxWidth": 0,
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}],
        columns=[
            {"id": "id", "name": "id"},
            {"id": "predicted_at", "name": "predicted at"},
            {"id": "longtitude", "name": "longtitude"},
            {"id": "latitude", "name": "latitude"},
            {"id": "housing_median_age", "name": "housing median age"},
            {"id": "total_rooms", "name": "total rooms"},
            {"id": "total_bedrooms", "name": "total bedrooms"},
            {"id": "population", "name": "population"},
            {"id": "households", "name": "households"},
            {"id": "median_income", "name": "median income"},
            {"id": "ocean_proximity", "name": "ocean proximity"},
            {
                "id": "predicted_price",
                "name": "price",
                "type": "numeric",
                "format": dash_table.FormatTemplate.money(2),
            },
        ],
        hidden_columns=["id"],
        page_current=0,
        page_size=10,
        page_action="custom",
    )
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.H1("House prices", className="mb-4 mt-3"), form], width=3
                ),
                dbc.Col(
                    [
                        html.H4("Prediction history", className="mt-4"),
                        dcc.Graph(id="plot"),
                        html.H4("Last model requests", className="mb-4"),
                        model_request_table,
                    ]
                ),
            ]
        )
    ],
    fluid=True,
)


@app.callback(
    [
        Output("price", "children"),
        Output("history", "data"),
        Output("plot", "figure"),
    ],
    Input("predict", "n_clicks"),
    Input("history", "page_current"),
    Input("history", "page_size"),
    {
        "longtitude": State("longtitude", "value"),
        "latitude": State("latitude", "value"),
        "housing_median_age": State("housing-median-age", "value"),
        "total_rooms": State("total-rooms", "value"),
        "total_bedrooms": State("total-bedrooms", "value"),
        "population": State("population", "value"),
        "households": State("households", "value"),
        "median_income": State("median-income", "value"),
        "ocean_proximity": State("ocean-proximity", "value"),
    },
)
def predict_price(n_clicks, page_current, page_size, params):
    if ctx.triggered_id == "predict" and n_clicks > 0:
        response = requests.get(f"{API}/predict", params=params).json()
        predicted_price = response["price"]

        price = f"$ {predicted_price:.2f}"
    else:
        price = "$ NaN"

    response_table = requests.get(
        f"{API}/model_requests",
        params={"skip": page_current * page_size, "limit": page_size},
    ).json()

    response_plot = requests.get(
        f"{API}/price_prediction_history",
        params={"limit": 1000},
    ).json()

    fig = px.line(response_plot, x="predicted_at", y="predicted_price")

    return price, response_table, fig


if __name__ == "__main__":
    app.run_server(debug=True)

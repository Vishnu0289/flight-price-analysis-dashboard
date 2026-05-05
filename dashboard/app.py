import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned", "cleaned_flights.csv")

# --------------------------------------------------
# LOAD DATA (NO RE-CLEANING HERE ❗)
# --------------------------------------------------

def load_data():
    try:
        df = pd.read_csv(DATA_PATH)

        print("Loaded Data Shape:", df.shape)

        if df.empty:
            raise ValueError("Dataset is EMPTY!")

        return df

    except Exception as e:
        print("Error:", e)
        return pd.DataFrame()

df = load_data()

# --------------------------------------------------
# DASH APP
# --------------------------------------------------

app = dash.Dash(__name__)
app.title = "Flight Analytics Dashboard"

# --------------------------------------------------
# DROPDOWN OPTIONS
# --------------------------------------------------

def get_options(col):
    return [{"label": str(i), "value": i} for i in df[col].dropna().unique()]

airline_options = get_options("airline")
source_options = get_options("source_city")
destination_options = get_options("destination_city")

# --------------------------------------------------
# LAYOUT
# --------------------------------------------------

app.layout = html.Div([

    html.H1("✈ Flight Analytics Dashboard", style={"textAlign": "center"}),

    html.Div([
        dcc.Dropdown(id="airline", options=airline_options, multi=True, placeholder="Airline"),
        dcc.Dropdown(id="source", options=source_options, multi=True, placeholder="Source"),
        dcc.Dropdown(id="destination", options=destination_options, multi=True, placeholder="Destination"),
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "10px"}),

    html.Br(),

    html.Div(id="kpis", style={"display": "flex", "gap": "20px"}),

    html.Br(),

    # 15 GRAPHS
    dcc.Graph(id="q1"),
    dcc.Graph(id="q2"),
    dcc.Graph(id="q3"),
    dcc.Graph(id="q4"),
    dcc.Graph(id="q5"),
    dcc.Graph(id="q6"),
    dcc.Graph(id="q7"),
    dcc.Graph(id="q8"),
    dcc.Graph(id="q9"),
    dcc.Graph(id="q10"),
    dcc.Graph(id="q11"),
    dcc.Graph(id="q12"),
    dcc.Graph(id="q13"),
    dcc.Graph(id="q14"),
    dcc.Graph(id="q15"),
])

# --------------------------------------------------
# CALLBACK
# --------------------------------------------------

@app.callback(
    [Output(f"q{i}", "figure") for i in range(1,16)] +
    [Output("kpis", "children")],

    [Input("airline", "value"),
     Input("source", "value"),
     Input("destination", "value")]
)
def update(airline, source, destination):

    dff = df.copy()

    if airline:
        dff = dff[dff["airline"].isin(airline)]
    if source:
        dff = dff[dff["source_city"].isin(source)]
    if destination:
        dff = dff[dff["destination_city"].isin(destination)]

    if dff.empty:
        empty = px.scatter(title="No Data")
        return [empty]*15 + [[html.Div("No Data Available")]]

    # KPI
    kpis = [
        html.Div(f"Avg Price: {round(dff['price'].mean(),2)}"),
        html.Div(f"Max Price: {round(dff['price'].max(),2)}"),
        html.Div(f"Flights: {len(dff)}")
    ]

    # Q1
    q1 = px.bar(dff.groupby("airline")["price"].mean().reset_index(),
                x="airline", y="price", title="Cheapest Airline")

    # Q2
    q2 = px.scatter(dff, x="days_left", y="price",
                    title="Days Left vs Price")

    # Q3
    dff["route"] = dff["source_city"] + "-" + dff["destination_city"]
    q3 = px.bar(dff.groupby("route")["price"].mean().nlargest(10).reset_index(),
                x="route", y="price", title="Expensive Routes")

    # Q4
    q4 = px.box(dff, x="class", y="price", title="Class Price Difference")

    # Q5
    q5 = px.bar(dff.groupby("departure_time")["price"].mean().reset_index(),
                x="departure_time", y="price", title="Departure Impact")

    # Q6
    q6 = px.bar(dff.groupby("airline")["price"].std().reset_index(),
                x="airline", y="price", title="Price Variability")

    # Q7
    q7 = px.bar(dff.groupby("source_city")["duration_minutes"].mean().reset_index(),
                x="source_city", y="duration_minutes", title="Duration by Source")

    # Q8
    q8 = px.box(dff, x="stops", y="price", title="Stops vs Price")

    # Q9
    q9 = px.scatter(dff, x="duration_minutes", y="price",
                    title="Duration vs Price")

    # Q10
    q10 = px.bar(dff.groupby("destination_city")["price"].mean().reset_index(),
                 x="destination_city", y="price", title="Price by Destination")

    # Q11
    q11 = px.bar(dff.groupby("arrival_time")["price"].mean().reset_index(),
                 x="arrival_time", y="price", title="Arrival Impact")

    # Q12
    q12 = px.bar(dff[dff["class"]=="Business"]
                 .groupby("airline")["price"].mean().reset_index(),
                 x="airline", y="price", title="Business Price by Airline")

    # Q13
    q13 = px.bar(dff[dff["class"]=="Business"]
                 .groupby("airline").size().reset_index(name="count"),
                 x="airline", y="count", title="Business Flights Count")

    # Q14
    q14 = px.bar(dff.groupby("route")["price"].std().nlargest(10).reset_index(),
                 x="route", y="price", title="Price Fluctuation")

    # Q15
    q15 = px.bar(dff.groupby(["route","airline"]).size()
                 .reset_index(name="count").nlargest(10,"count"),
                 x="route", y="count", color="airline",
                 title="Route Dominance")

    return [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15] + [kpis]


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
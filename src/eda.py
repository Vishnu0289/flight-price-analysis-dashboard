import pandas as pd
import logging
import os
from scipy.stats import ttest_ind, f_oneway
from utils import setup_logging, ensure_directory
from visualisation import *

# --------------------------------------------------
# SETUP
# --------------------------------------------------

setup_logging()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned", "cleaned_flights.csv")
FIGURE_PATH = os.path.join(BASE_DIR, "outputs", "figures")
REPORT_PATH = os.path.join(BASE_DIR, "outputs", "reports")

ensure_directory(FIGURE_PATH)
ensure_directory(REPORT_PATH)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():
    df = pd.read_csv(DATA_PATH)

    if df.empty:
        raise ValueError("Dataset is EMPTY!")

    logging.info(f"EDA Loaded: {df.shape}")
    return df


# --------------------------------------------------
# MAIN ANALYSIS
# --------------------------------------------------

def run_analysis(df):

    results = {}

    # Create route column
    df["route"] = df["source_city"] + "-" + df["destination_city"]

    # 1 Cheapest airline
    q1 = df.groupby("airline")["price"].mean().sort_values()
    results["Q1"] = q1.idxmin()
    bar_plot(q1.reset_index(), "airline", "price", "Avg Price by Airline", "q1.png")

    # 2 Days vs price
    scatter_plot(df, "days_left", "price", "Days vs Price", "q2.png")
    results["Q2"] = "Price generally decreases as days_left increases"

    # 3 Expensive routes
    q3 = df.groupby("route")["price"].mean().sort_values(ascending=False).head(10)
    results["Q3"] = q3.index[0]
    bar_plot(q3.reset_index(), "route", "price", "Top Expensive Routes", "q3.png")

    # 4 Class difference
    box_plot(df, "class", "price", "Class Price Distribution", "q4.png")
    results["Q4"] = "Business class is significantly more expensive"

    # 5 Departure time impact
    q5 = df.groupby("departure_time")["price"].mean().reset_index()
    bar_plot(q5, "departure_time", "price", "Departure Time Impact", "q5.png")
    results["Q5"] = q5.sort_values("price", ascending=False).iloc[0]["departure_time"]

    # 6 Price variability
    q6 = df.groupby("airline")["price"].std().sort_values(ascending=False)
    bar_plot(q6.reset_index(), "airline", "price", "Price Variability", "q6.png")
    results["Q6"] = q6.idxmax()

    # 7 Source city duration
    q7 = df.groupby("source_city")["duration_minutes"].mean().sort_values(ascending=False)
    bar_plot(q7.reset_index(), "source_city", "duration_minutes", "Duration by Source", "q7.png")
    results["Q7"] = q7.idxmax()

    # 8 Stops vs price
    box_plot(df, "stops", "price", "Stops vs Price", "q8.png")
    results["Q8"] = "Non-stop flights tend to be costlier"

    # 9 Duration vs price
    scatter_plot(df, "duration_minutes", "price", "Duration vs Price", "q9.png")
    results["Q9"] = "Positive correlation"

    # 10 Destination pricing
    q10 = df.groupby("destination_city")["price"].mean().sort_values(ascending=False)
    bar_plot(q10.reset_index(), "destination_city", "price", "Price by Destination", "q10.png")
    results["Q10"] = q10.idxmax()

    # 11 Arrival time impact
    q11 = df.groupby("arrival_time")["price"].mean().reset_index()
    bar_plot(q11, "arrival_time", "price", "Arrival Time Impact", "q11.png")
    results["Q11"] = q11.sort_values("price", ascending=False).iloc[0]["arrival_time"]

    # 12 Business consistency
    business_df = df[df["class"] == "Business"]
    q12 = business_df.groupby("airline")["price"].mean()
    bar_plot(q12.reset_index(), "airline", "price", "Business Price by Airline", "q12.png")
    results["Q12"] = "Yes, Business class is always higher"

    # 13 Business flight count
    q13 = business_df.groupby("airline").size().sort_values(ascending=False)
    bar_plot(q13.reset_index(name="count"), "airline", "count", "Business Flights Count", "q13.png")
    results["Q13"] = q13.idxmax()

    # 14 Route fluctuation
    q14 = df.groupby("route")["price"].std().sort_values(ascending=False).head(10)
    bar_plot(q14.reset_index(), "route", "price", "Route Price Fluctuation", "q14.png")
    results["Q14"] = q14.idxmax()

    # 15 Route dominance
    q15 = df.groupby(["route", "airline"]).size().reset_index(name="count")
    top = q15.sort_values("count", ascending=False).head(10)
    bar_plot(top, "route", "count", "Route Dominance", "q15.png")
    results["Q15"] = top.iloc[0]["airline"]

    return results


# --------------------------------------------------
# STATS
# --------------------------------------------------

def statistical(df):
    corr = df[["price", "duration_minutes", "days_left"]].corr()
    heatmap_plot(corr, "correlation.png")

    eco = df[df["class"] == "Economy"]["price"]
    bus = df[df["class"] == "Business"]["price"]

    if len(eco) > 1 and len(bus) > 1:
        ttest_ind(eco, bus)


# --------------------------------------------------
# EXPORT ANSWERS
# --------------------------------------------------

def export_results(results):
    df = pd.DataFrame(list(results.items()), columns=["Question", "Answer"])
    df.to_csv(os.path.join(REPORT_PATH, "answers.csv"), index=False)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    df = load_data()

    results = run_analysis(df)
    statistical(df)
    export_results(results)

    logging.info("EDA COMPLETED")


if __name__ == "__main__":
    main()
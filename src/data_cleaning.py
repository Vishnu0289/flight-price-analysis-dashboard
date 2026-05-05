import pandas as pd
import numpy as np
import logging
import os
from utils import setup_logging, ensure_directory

# --------------------------------------------------
# SETUP
# --------------------------------------------------

setup_logging()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "airlines_flights_data.csv")

CLEANED_PATH = os.path.join(BASE_DIR, "data", "cleaned", "cleaned_flights.csv")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():
    df = pd.read_csv(RAW_PATH)
    logging.info(f"Loaded data shape: {df.shape}")

    if df.empty:
        raise ValueError("Raw dataset is EMPTY!")

    return df


# --------------------------------------------------
# HANDLE MISSING VALUES (SAFE)
# --------------------------------------------------

def handle_missing_values(df):

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["days_left"] = pd.to_numeric(df["days_left"], errors="coerce")

    df["price"] = df["price"].fillna(df["price"].median())
    df["days_left"] = df["days_left"].fillna(df["days_left"].median())

    df["duration"] = df["duration"].fillna("0h 0m")

    df = df.dropna(subset=["airline", "source_city", "destination_city"])

    logging.info(f"After missing handling: {df.shape}")
    return df


# --------------------------------------------------
# REMOVE DUPLICATES
# --------------------------------------------------

def remove_duplicates(df):
    before = df.shape[0]
    df = df.drop_duplicates()
    logging.info(f"Duplicates removed: {before - df.shape[0]}")
    return df


# --------------------------------------------------
# CONVERT DURATION
# --------------------------------------------------

def convert_duration(df):

    def convert(val):
        try:
            if pd.isna(val):
                return 0

            val = str(val)
            h = int(val.split("h")[0]) if "h" in val else 0
            m = int(val.split("m")[0].split()[-1]) if "m" in val else 0
            return h * 60 + m
        except:
            return 0

    df["duration_minutes"] = df["duration"].apply(convert)

    return df


# --------------------------------------------------
# ENCODE STOPS
# --------------------------------------------------

def encode_stops(df):
    mapping = {"non-stop": 0, "1-stop": 1, "2+-stop": 2}

    df["stops_encoded"] = df["stops"].map(mapping)
    df["stops_encoded"] = df["stops_encoded"].fillna(0)

    return df


# --------------------------------------------------
# CATEGORICALS
# --------------------------------------------------

def convert_categoricals(df):
    cols = ["airline", "source_city", "destination_city", "class"]

    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df


# --------------------------------------------------
# REMOVE OUTLIERS (SAFE VERSION)
# --------------------------------------------------

def remove_outliers(df):

    if df.shape[0] < 100:
        logging.warning("Skipping outliers (too few rows)")
        return df

    Q1 = df["price"].quantile(0.25)
    Q3 = df["price"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    filtered = df[(df["price"] >= lower) & (df["price"] <= upper)]

    # 🚨 CRITICAL FIX
    if filtered.empty:
        logging.warning("Outlier removal removed ALL data. Skipping step.")
        return df

    logging.info(f"Outliers removed: {df.shape[0] - filtered.shape[0]}")
    return filtered


# --------------------------------------------------
# SAVE
# --------------------------------------------------

def save_cleaned_data(df):

    ensure_directory(os.path.dirname(CLEANED_PATH))
    df.to_csv(CLEANED_PATH, index=False)

    logging.info(f"Saved cleaned data: {df.shape}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    df = load_data()
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = convert_duration(df)
    df = encode_stops(df)
    df = convert_categoricals(df)
    df = remove_outliers(df)

    if df.empty:
        raise ValueError("Final dataset is EMPTY after cleaning!")

    save_cleaned_data(df)


if __name__ == "__main__":
    main()
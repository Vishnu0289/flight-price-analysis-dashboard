import os
import subprocess
import sys
import logging
from datetime import datetime

# --------------------------------------------------
# BASE PATH (IMPORTANT FIX)
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.join(BASE_DIR, "src")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "reports")

os.makedirs(OUTPUT_DIR, exist_ok=True)

LOG_PATH = os.path.join(OUTPUT_DIR, "pipeline_log.txt")

# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg):
    print(msg)
    logging.info(msg)

# --------------------------------------------------
# RUN SCRIPT SAFELY
# --------------------------------------------------

def run_script(script_path):
    try:
        log(f"\n🚀 Running: {script_path}")
        
        subprocess.run(
            [sys.executable, script_path],
            check=True
        )

        log(f"✅ Completed: {script_path}")

    except subprocess.CalledProcessError as e:
        log(f"❌ Error in {script_path}: {e}")
        sys.exit(1)

# --------------------------------------------------
# CHECK CLEANED DATA EXISTS
# --------------------------------------------------

def validate_cleaned_data():
    path = os.path.join(BASE_DIR, "data", "cleaned", "cleaned_flights.csv")

    if not os.path.exists(path):
        log("❌ Cleaned data file NOT found!")
        sys.exit(1)

    import pandas as pd
    df = pd.read_csv(path)

    if df.empty:
        log("❌ Cleaned dataset is EMPTY!")
        sys.exit(1)

    log(f"✅ Cleaned data validated: {df.shape}")

# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def main():

    log("=" * 50)
    log("✈ FLIGHT DATA PIPELINE STARTED")
    log("=" * 50)

    start = datetime.now()

    # -------------------------
    # STEP 1: DATA CLEANING
    # -------------------------
    run_script(os.path.join(SRC_DIR, "data_cleaning.py"))

    # Validate output
    validate_cleaned_data()

    # -------------------------
    # STEP 2: EDA
    # -------------------------
    run_script(os.path.join(SRC_DIR, "eda.py"))

    # -------------------------
    # STEP 3: DASHBOARD
    # -------------------------
    log("\n🌐 Starting Dashboard...")

    subprocess.run([
        sys.executable,
        os.path.join(DASHBOARD_DIR, "app.py")
    ])

    end = datetime.now()

    log(f"\n⏱ Pipeline finished in: {end - start}")
    log("🎯 ALL STEPS COMPLETED SUCCESSFULLY")

# --------------------------------------------------

if __name__ == "__main__":
    main()
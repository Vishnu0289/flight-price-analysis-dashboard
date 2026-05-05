import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging

# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURE_PATH = os.path.join(BASE_DIR, "outputs", "figures")

os.makedirs(FIGURE_PATH, exist_ok=True)

# --------------------------------------------------
# SAFE CHECKS
# --------------------------------------------------

def is_empty(data):
    return data is None or (hasattr(data, "empty") and data.empty)

def has_columns(data, cols):
    return all(col in data.columns for col in cols)

# --------------------------------------------------
# SAVE FUNCTION
# --------------------------------------------------

def save_plot(filename):
    try:
        path = os.path.join(FIGURE_PATH, filename)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        logging.info(f"Saved plot: {filename}")
    except Exception as e:
        logging.error(f"Error saving plot {filename}: {e}")

# --------------------------------------------------
# BAR PLOT
# --------------------------------------------------

def bar_plot(data, x, y, title, filename):
    try:
        if is_empty(data) or not has_columns(data, [x, y]):
            logging.warning(f"Skipping {filename} (invalid data)")
            return

        if data[y].dropna().empty:
            logging.warning(f"Skipping {filename} (empty values)")
            return

        plt.figure(figsize=(10, 6))
        sns.barplot(data=data, x=x, y=y)
        plt.title(title)
        plt.xticks(rotation=45)

        save_plot(filename)

    except Exception as e:
        logging.error(f"Error in bar_plot {filename}: {e}")

# --------------------------------------------------
# SCATTER PLOT
# --------------------------------------------------

def scatter_plot(data, x, y, title, filename):
    try:
        if is_empty(data) or not has_columns(data, [x, y]):
            logging.warning(f"Skipping {filename}")
            return

        if data[x].dropna().empty or data[y].dropna().empty:
            logging.warning(f"Skipping {filename} (empty values)")
            return

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=data, x=x, y=y)
        plt.title(title)

        save_plot(filename)

    except Exception as e:
        logging.error(f"Error in scatter_plot {filename}: {e}")

# --------------------------------------------------
# BOX PLOT
# --------------------------------------------------

def box_plot(data, x, y, title, filename):
    try:
        if is_empty(data) or not has_columns(data, [x, y]):
            logging.warning(f"Skipping {filename}")
            return

        if data[y].dropna().empty:
            logging.warning(f"Skipping {filename} (empty values)")
            return

        plt.figure(figsize=(10, 6))
        sns.boxplot(data=data, x=x, y=y)
        plt.title(title)

        save_plot(filename)

    except Exception as e:
        logging.error(f"Error in box_plot {filename}: {e}")

# --------------------------------------------------
# HEATMAP
# --------------------------------------------------

def heatmap_plot(corr, filename):
    try:
        if corr is None or corr.empty:
            logging.warning(f"Skipping heatmap (empty)")
            return

        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm")

        save_plot(filename)

    except Exception as e:
        logging.error(f"Error in heatmap_plot {filename}: {e}")
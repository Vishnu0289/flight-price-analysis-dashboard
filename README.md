# ✈️ Flight Price Analysis & Interactive Dashboard

A complete **Data Analytics Project** that analyzes airline flight pricing trends and presents insights through **EDA, visualizations, and an interactive dashboard**.

---

## 📌 Project Overview

This project explores flight pricing data to answer key business questions such as:

- Which airline is the cheapest?
- How does price change with days left before departure?
- Are business class flights always expensive?
- Which routes are most costly?

The project follows a **complete data pipeline**:
> Raw Data → Data Cleaning → EDA → Dashboard

---

## 🧠 Business Questions Solved

1. Cheapest airline overall  
2. Price vs days left before departure  
3. Most expensive routes  
4. Economy vs Business price difference  
5. Departure time impact on pricing  
6. Airline price variability  
7. Source cities with longest duration  
8. Non-stop vs stop flight pricing  
9. Duration vs price correlation  
10. Price variation by destination  
11. Arrival time impact  
12. Business class pricing consistency  
13. Airlines with most business flights  
14. Routes with highest price fluctuation  
15. Airline dominance on routes  

---

## 🛠️ Tech Stack

- **Python**
- **Pandas, NumPy**
- **Matplotlib, Seaborn**
- **Plotly**
- **Dash (for interactive dashboard)**

---

## 📂 Project Structure


flight_price_analysis/
│
├── data/
│ ├── raw/
│ └── cleaned/
│
├── src/
│ ├── data_cleaning.py
│ ├── eda.py
│ ├── visualization.py
│ └── utils.py
│
├── dashboard/
│ └── app.py
│
├── outputs/
│ ├── figures/
│ └── reports/
│
├── run_pipeline.py
├── requirements.txt
└── README.md


---

## ⚙️ How to Run the Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/flight-price-analysis.git
cd flight-price-analysis
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Data Pipeline
python src/data_cleaning.py
python src/eda.py
5️⃣ Run Dashboard
python dashboard/app.py

Then open:

http://127.0.0.1:8050/
📊 Dashboard Features
Interactive filters (Airline, Source, Destination)
KPI cards (Average price, Max price, Total flights)
15+ dynamic charts
Real-time filtering
📸 Screenshots

Add screenshots here after running dashboard

![Dashboard](screenshots/dashboard.png)
🚀 Key Highlights
End-to-end data analytics pipeline
Real-world dataset (300k+ rows)
Business-focused insights
Interactive dashboard for decision making
Production-ready folder structure
📌 Future Improvements
Deploy dashboard online (Render / Railway)
Add machine learning model for price prediction
Improve UI with advanced styling
Add real-time data integration


🤝 Contributing

Feel free to fork this repo and improve it!
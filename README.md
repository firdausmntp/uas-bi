# 🛒 Super Store Sales Dashboard (Streamlit + Plotly)

Web dashboard (Live Demo): https://retailsuperstoresales.streamlit.app/

Interactive Business Intelligence dashboard built with **Streamlit** and **Plotly** on a simple star-schema dataset (fact + dimensions). Includes KPIs, trends, regional insights, forecasting, and exportable reports.

---

## ✨ Key Features

- **KPI Overview**: total sales, average sale, customers, products, orders, and more
- **Filters (Sidebar)**: explore data dynamically
- **Visual Analytics**:
  - Category / Segment / Region distribution (pie)
  - Sales trends (monthly / quarterly / yearly)
  - Top states & cities by sales (bar)
  - **USA Sales Map** (choropleth by state)
- **Forecasting**: simple **Linear Regression** forecasting for next periods
- **Export**:
  - **Excel report (.xlsx)** with multiple sheets (formatted)
  - CSV exports for quick stats

---

## 🗂️ Project Structure

```
.
├─ app.py
├─ requirements.txt
├─ fact_sales.csv
├─ dim_customer.csv
├─ dim_date.csv
├─ dim_product.csv
├─ dim_region.csv
├─ components/
│  ├─ charts.py
│  ├─ icons.py
│  ├─ kpi_cards.py
│  ├─ sidebar.py
│  ├─ styles.py
│  └─ __init__.py
├─ utils/
│  ├─ data_loader.py
│  ├─ export_utils.py
│  └─ __init__.py
└─ config/
   ├─ settings.py
   └─ __init__.py
```

---

## 🚀 Run Locally (Windows)

### 1) Create & activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2) Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3) Start Streamlit

```bash
streamlit run app.py
```

---

## 📦 Requirements

All dependencies are listed in `requirements.txt`. Main libraries:

- `streamlit`
- `pandas`, `numpy`
- `plotly`
- `scikit-learn` (forecasting)
- `openpyxl` (Excel export)

---

## 📊 Data Model (Star Schema)

This project uses CSV tables:

- `fact_sales.csv` (transactions)
- `dim_customer.csv`
- `dim_date.csv`
- `dim_product.csv`
- `dim_region.csv`

The loader merges them into a single analytics dataset used across charts and KPIs.

---

## 🧰 Troubleshooting

### Plotly import error (`ModuleNotFoundError: No module named 'plotly'`)
This usually means Streamlit/terminal is using a different Python interpreter.

Make sure you:

1. Activate the venv: `venv\Scripts\activate`
2. Install with the same interpreter: `python -m pip install -r requirements.txt`
3. Run Streamlit from the same venv: `streamlit run app.py`

### Map not showing some states
The choropleth requires US state names that match the standard mapping (e.g., `California`, `Texas`). Any unknown labels are skipped.

---

## 🔗 Live Demo

- https://retailsuperstoresales.streamlit.app/

---

## 👤 Author

Business Intelligence Project (UAS) — Semester 5

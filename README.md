# Retail Store Transactions Dashboard

This project is a Streamlit dashboard for analyzing retail store transactions. It includes automatic data cleaning, interactive filters, KPI cards, and charts for sales analysis.

## Features
- Automatic data cleaning from Excel.
- Interactive filters for date, location, product, payment type, cashier, and store manager.
- KPI cards for transactions, total sales, average order value, and total quantity.
- Visualizations for sales over time, product sales, location sales, payment distribution, quantity by day, and store-product heatmap.
- Download button for filtered data.

## Dataset Columns
The dataset contains:
- Date
- Time
- StoreID
- Location
- Product
- Quantity
- UnitPrice
- PaymentType
- TransactionID
- Cashier
- StoreManager
- TimeOfDay
- DayOfWeek
- TotalPrice

These fields are suitable for cleaning, filtering, and dashboard analysis [file:1].

## Project Files
- `app.py` → Streamlit dashboard application.
- `data_cleaning.py` → Automatic data cleaning script.
- `visualizations.py` → Plotly chart functions.
- `requirements.txt` → Required Python packages.
- `data/` → Folder containing the Excel file and cleaned CSV.

## How to Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Put the dataset in the data folder
Place your Excel file here:
```text
data/Retail-Store-Transactions_Dashboard.xlsx
```

### 3. Clean the data
```bash
python data_cleaning.py
```

### 4. Start the app
```bash
streamlit run app.py
```

## Dashboard Workflow
1. The app checks whether the cleaned CSV exists.
2. If not, it runs the cleaning script automatically.
3. The cleaned dataset is loaded into Streamlit.
4. Sidebar filters refine the data.
5. Charts and KPI cards update based on the selected filters.

## Notes
- The cleaning script handles duplicates, missing values, type conversion, and total-price validation.
- The dashboard is built to work directly with the dataset structure already present in the file [file:1].

## Deployment
See the deployment steps below for Streamlit Cloud hosting.

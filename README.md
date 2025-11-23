# Crypto ETL & Dashboard Walkthrough

## Overview
This project is a real-time cryptocurrency monitor that fetches data from the CoinGecko API, processes it, and visualizes it in an interactive Streamlit dashboard.

## Project Structure
- `etl/main.py`: The core ETL script.
    - **Extracts** data from CoinGecko (including 7-day price history).
    - **Transforms** it (cleaning, renaming, timestamping).
    - **Loads** it into `data/crypto_market.csv`.
- `app/dashboard.py`: The Streamlit application.
    - Reads the CSV file.
    - Displays KPIs, Charts, and a Data Table.
    - **[NEW]** Sidebar filters to select specific coins.
    - **[NEW]** **Market Overview Treemap**: Visualizes market cap and performance (Red/Green).
    - **[NEW]** **Market Dominance Donut Chart**: Shows market share of selected coins.
    - **[NEW]** **7-Day Trend Chart**: Compare performance over the last week.
    - **[NEW]** **Dynamic Theme Switcher**: Toggle between **Mocha**, **Macchiato**, **Frappe**, and **Latte** instantly from the sidebar.
    - Includes a "Refresh" button to trigger the ETL script on demand.
- `data/`: Directory where the processed data is stored.
- `.streamlit/config.toml`: Configuration file for the default theme (Mocha).

## How to Run Locally

### 1. Run the ETL Process (Optional)
The dashboard can trigger this, but you can run it manually to test:
```bash
python etl/main.py
```

### 2. Launch the Dashboard
Run the following command in your terminal:
```bash
streamlit run app/dashboard.py
```
This will open the dashboard in your default web browser (usually at `http://localhost:8501`).

## How to Deploy to Streamlit Community Cloud

1.  **Push to GitHub**: Upload this entire project folder to a new GitHub repository.
2.  **Sign up/Login**: Go to [share.streamlit.io](https://share.streamlit.io/).
3.  **New App**: Click "New App" and select your GitHub repository.
4.  **Settings**:
    *   **Main file path**: `app/dashboard.py`
5.  **Deploy**: Click "Deploy!" and wait for it to build.

Streamlit Cloud will automatically install dependencies from `requirements.txt` and run your app. The code includes a fix (`sys.path.append`) to ensure imports work correctly in the cloud environment.

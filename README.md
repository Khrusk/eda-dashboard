# 📊 Universal EDA Dashboard

An interactive exploratory data analysis (EDA) tool built with **Streamlit**. 
Upload any CSV file and instantly explore it — dynamic filters, auto-detected column types, and a chart builder that lets you generate histograms, bar charts, pie charts, scatter plots, box plots, and correlation heatmaps without writing a single line of code.

🔗 **Live demo:** _[add your Streamlit Cloud link here once deployed]_

---

## Features

- **Drag-and-drop CSV upload** — analyze any dataset, not just one hardcoded file
- **Automatic column type detection** — numeric vs categorical columns are detected on load, so the app only offers chart options that make sense for the data
- **Dynamic sidebar filters** — auto-generated from low-cardinality categorical columns
- **Interactive chart builder** — pick a chart type, then pick the columns to plot:
  - Histogram
  - Bar Chart
  - Pie Chart
  - Scatter Plot
  - Box Plot
  - Line Chart
  - Correlation Heatmap
- **Auto-generated insight** — automatically surfaces the strongest correlation found in the dataset
- **Filtered data export** — download the currently filtered view as a CSV
- **Graceful fallbacks** — if a dataset lacks numeric or categorical columns, the relevant chart options are disabled with a clear message instead of crashing

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io/) | Web app framework |
| [Pandas](https://pandas.pydata.org/) | Data loading, filtering, aggregation |
| [NumPy](https://numpy.org/) | Numeric operations |
| [Matplotlib](https://matplotlib.org/) | Chart rendering |
| [Seaborn](https://seaborn.pydata.org/) | Correlation heatmap styling |

---

## Screenshots

<img width="1907" height="862" alt="filtered_data" src="https://github.com/user-attachments/assets/8ef44c61-34fa-418f-8d0f-8d5567a29ce2" />

<img width="1918" height="872" alt="char_builder" src="https://github.com/user-attachments/assets/4e02f919-b827-4058-b147-f9d83c8153a6" />

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/eda-dashboard.git
cd eda-dashboard
pip install -r requirements.txt
```

### Run locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`. Upload any CSV via the sidebar, or leave it as-is to explore the bundled demo dataset.

---

## Project Structure

```
eda-dashboard/
├── app.py              # Main Streamlit application
├── data.csv            # Demo dataset (used if no file is uploaded)
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## How It Works

1. **Data loading** — `st.file_uploader()` accepts a user-uploaded CSV, falling back to a bundled demo dataset if none is provided. Results are cached with `@st.cache_data` to avoid re-reading the file on every interaction.
2. **Column detection** — `df.select_dtypes()` splits columns into numeric and categorical groups, which drives every dynamic element downstream (filters, chart options).
3. **Filtering** — categorical columns with ≤30 unique values are automatically turned into sidebar multiselect filters; all charts and the data table respond to the active filters.
4. **Chart builder** — a single chart-type selector reveals context-specific follow-up controls (e.g. bins for a histogram, x/y axes for a scatter plot), then renders the chart with Matplotlib/Seaborn.
5. **Insight generation** — the app computes the full numeric correlation matrix and surfaces the strongest pairwise relationship automatically.

---

## Demo Dataset

The included `data.csv` contains player-level match statistics from a football tournament (54,600 rows × 75 columns) — covering player info, match context, raw performance stats (goals, assists, passes), and advanced metrics (expected goals, player ratings). It's used as the default view; upload your own CSV to explore different data.

---

## Future Improvements

- [ ] Add support for Excel (`.xlsx`) file uploads
- [ ] Add date-range filtering for time-series datasets
- [ ] Add a "data quality report" section (duplicate rows, outlier detection)
- [ ] Persist uploaded datasets across sessions

---

## Author

Built by **Khrus** — B.Tech CSE student, MNIT Jaipur. Part of learning ML.
[GitHub](https://github.com/Khrusk) · [LinkedIn](www.linkedin.com/in/khrusk)

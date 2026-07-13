import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Universal EDA Dashboard", layout="wide")

st.title("📊 Universal EDA Dashboard")
st.caption("Upload any CSV and explore it interactively")

# ---------- Data source: upload or fallback demo ----------
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])


@st.cache_data
def load_data(source):
    return pd.read_csv(source)


if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success(f"Loaded: {uploaded_file.name}")
else:
    df = load_data("data.csv")
    st.sidebar.info("Using default demo dataset — upload your own CSV to replace it")

# ---------- Detect column types ----------
numeric_cols = df.select_dtypes(include='number').columns.tolist()
categorical_cols = df.select_dtypes(include='object').columns.tolist()

st.write("### Raw data preview")
st.dataframe(df.head())

# ---------- Overview stats ----------
st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows", f"{df.shape[0]:,}")
col2.metric("Columns", df.shape[1])
col3.metric("Numeric Columns", len(numeric_cols))
col4.metric("Missing Values", f"{df.isnull().sum().sum():,}")

# ---------- Dynamic sidebar filters ----------
st.sidebar.header("🔎 Filters")
filterable_cols = [c for c in categorical_cols if df[c].nunique() <= 30]

filtered_df = df.copy()
for col in filterable_cols[:5]:
    selected = st.sidebar.multiselect(col, options=sorted(df[col].dropna().unique()))
    if selected:
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

st.sidebar.write(f"Showing **{len(filtered_df):,}** of {len(df):,} rows")

# ---------- Chart builder ----------
st.divider()
st.write("### Build Your Own Chart")

chart_type = st.selectbox(
    "Chart type",
    ["Histogram", "Bar Chart", "Pie Chart", "Scatter Plot", "Box Plot", "Line Chart", "Correlation Heatmap"]
)

if chart_type == "Histogram":
    if numeric_cols:
        col = st.selectbox("Numeric column", numeric_cols)
        bins = st.slider("Number of bins", 5, 100, 30)
        fig, ax = plt.subplots()
        ax.hist(filtered_df[col].dropna(), bins=bins, color='#2563eb', edgecolor='white')
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.info("No numeric columns found in this dataset.")

elif chart_type == "Bar Chart":
    if categorical_cols:
        cat_col = st.selectbox("Category column", categorical_cols)
        agg_choice = st.selectbox("Value to plot", ["Count"] + numeric_cols)
        if agg_choice == "Count":
            data = filtered_df[cat_col].value_counts().head(20)
        else:
            data = filtered_df.groupby(cat_col)[agg_choice].sum().sort_values(ascending=False).head(20)
        fig, ax = plt.subplots()
        ax.bar(data.index.astype(str), data.values, color='#16a34a')
        ax.set_ylabel(agg_choice)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    else:
        st.info("No categorical columns found in this dataset.")

elif chart_type == "Pie Chart":
    if categorical_cols:
        cat_col = st.selectbox("Category column", categorical_cols)
        top_n = st.slider("Show top N categories", 3, 15, 8)
        data = filtered_df[cat_col].value_counts().head(top_n)
        fig, ax = plt.subplots()
        ax.pie(data.values, labels=data.index, autopct='%1.1f%%')
        st.pyplot(fig)
    else:
        st.info("No categorical columns found in this dataset.")

elif chart_type == "Scatter Plot":
    if len(numeric_cols) >= 2:
        x_col = st.selectbox("X-axis", numeric_cols, key='scatter_x')
        y_col = st.selectbox("Y-axis", numeric_cols, key='scatter_y')
        fig, ax = plt.subplots()
        ax.scatter(filtered_df[x_col], filtered_df[y_col], alpha=0.3, color='#dc2626')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        st.pyplot(fig)
    else:
        st.info("Need at least 2 numeric columns for a scatter plot.")

elif chart_type == "Box Plot":
    if numeric_cols:
        num_col = st.selectbox("Numeric column", numeric_cols, key='box_num')
        group_col = st.selectbox("Group by (optional)", ["None"] + categorical_cols, key='box_group')
        fig, ax = plt.subplots()
        if group_col == "None":
            ax.boxplot(filtered_df[num_col].dropna())
            ax.set_xticklabels([num_col])
        else:
            groups = filtered_df.groupby(group_col)[num_col].apply(list)
            ax.boxplot(groups.values, tick_labels=groups.index)
            plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    else:
        st.info("No numeric columns found in this dataset.")

elif chart_type == "Line Chart":
    x_col = st.selectbox("X-axis", df.columns.tolist(), key='line_x')
    if numeric_cols:
        y_col = st.selectbox("Y-axis (numeric)", numeric_cols, key='line_y')
        data = filtered_df.groupby(x_col)[y_col].mean().sort_index()
        fig, ax = plt.subplots()
        ax.plot(data.index.astype(str), data.values, marker='o', color='#7c3aed')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    else:
        st.info("No numeric columns found in this dataset.")

elif chart_type == "Correlation Heatmap":
    if len(numeric_cols) >= 2:
        default_cols = numeric_cols[:6]
        selected_cols = st.multiselect("Columns to include", numeric_cols, default=default_cols)
        if len(selected_cols) >= 2:
            corr = filtered_df[selected_cols].corr()
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax)
            st.pyplot(fig)
        else:
            st.info("Select at least 2 columns.")
    else:
        st.info("Need at least 2 numeric columns for a correlation heatmap.")

# ---------- Auto-generated insight ----------
st.divider()
st.write("### Auto-Generated Insight")
if len(numeric_cols) >= 2:
    corr_matrix = filtered_df[numeric_cols].corr().abs()
    arr = corr_matrix.to_numpy(copy=True)
    np.fill_diagonal(arr, 0)
    corr_matrix = pd.DataFrame(arr, index=corr_matrix.index, columns=corr_matrix.columns)
    max_pair = corr_matrix.stack().idxmax()
    max_val = corr_matrix.stack().max()
    st.markdown(f"- Strongest correlation found: **{max_pair[0]}** and **{max_pair[1]}** (r = {max_val:.2f})")
else:
    st.markdown("- Not enough numeric columns to compute correlations.")

# ---------- Filtered data table + download ----------
st.divider()
st.write("### Filtered Data")
st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download filtered data as CSV", csv, "filtered_data.csv", "text/csv")
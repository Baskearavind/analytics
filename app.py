import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Dataset Analyzer", layout="wide")

# Title
st.markdown("<h1 style='color:#FF4B4B;'>📊 Dataset Analyzer & Visualizer</h1>", unsafe_allow_html=True)
st.markdown("Upload a CSV file and explore it with rich visualizations.")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.markdown("### 🧾 Data Preview")
    st.dataframe(df, use_container_width=True)

    # Basic info
    st.markdown("### 🔍 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    st.markdown("### 🧬 Column Data Types")
    st.write(df.dtypes)

    st.markdown("### 📈 Statistical Summary")
    st.write(df.describe())

    # Visualizations
    st.markdown("---")
    st.markdown("## 🎨 Visualizations")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    with st.expander("📌 Histogram (Numeric Columns)", expanded=True):
        col = st.selectbox("Select column", numeric_cols)
        fig = px.histogram(df, x=col, nbins=30, color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📌 Box Plot", expanded=True):
        col = st.selectbox("Select column for box plot", numeric_cols, key="box")
        fig = px.box(df, y=col, color_discrete_sequence=['#EF553B'])
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📌 Correlation Heatmap", expanded=False):
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, color_continuous_scale='Plasma', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📌 Scatter Plot", expanded=False):
        x_col = st.selectbox("X Axis", numeric_cols, key="xscatter")
        y_col = st.selectbox("Y Axis", numeric_cols, key="yscatter")
        color_col = st.selectbox("Color (optional)", categorical_cols + [None], index=0)
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col if color_col else None,
                         color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📌 Pie Chart (Categorical)", expanded=False):
        if categorical_cols:
            pie_col = st.selectbox("Select a categorical column", categorical_cols)
            pie_data = df[pie_col].value_counts().reset_index()
            pie_data.columns = [pie_col, "Count"]
            fig = px.pie(pie_data, names=pie_col, values="Count",
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No categorical columns available for pie chart.")
else:
    st.info("Please upload a CSV file to begin.")

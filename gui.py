import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------
# Page Configuration
# -------------------------------------

st.set_page_config(
    page_title="Restaurant Tips Analysis",
    page_icon="🍽️",
    layout="wide"
)

# -------------------------------------
# Title
# -------------------------------------

st.title("🍽️ Restaurant Tips Analysis Dashboard")
st.markdown("---")

# -------------------------------------
# Load Dataset
# -------------------------------------

tips = sns.load_dataset("tips")

# -------------------------------------
# Sidebar
# -------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose Section",
    [
        "🏠 Home",
        "📋 Dataset",
        "📊 Statistics",
        "🔍 Filtering",
        "📈 Charts",
        "ℹ️ About"
    ]
)

# =====================================
# HOME
# =====================================

if page == "🏠 Home":

    st.header("Restaurant Tips Dataset")

    st.write("""
Welcome to the **Restaurant Tips Analysis Dashboard**.

This application analyzes the famous **Tips Dataset**
provided by Seaborn.

The dashboard includes:

- Dataset Preview
- Statistical Analysis
- Filtering
- NumPy Analysis
- GroupBy Analysis
- Interactive Charts
    """)

    st.image(
        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200",
        use_container_width=True
    )

# =====================================
# DATASET
# =====================================

elif page == "📋 Dataset":

    st.header("Dataset Preview")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Show First 10 Rows"):

            st.subheader("First 10 Rows")

            st.dataframe(
                tips.head(10),
                use_container_width=True
            )

    with col2:

        if st.button("Show Last 10 Rows"):

            st.subheader("Last 10 Rows")

            st.dataframe(
                tips.tail(10),
                use_container_width=True
            )

    st.markdown("---")

    if st.button("Show Entire Dataset"):

        st.dataframe(
            tips,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("Dataset Shape")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Rows",
            tips.shape[0]
        )

    with col2:
        st.metric(
            "Columns",
            tips.shape[1]
        )

    st.markdown("---")

    if st.checkbox("Show Columns"):

        st.write(list(tips.columns))

    if st.checkbox("Show Data Types"):

        st.dataframe(
            tips.dtypes.astype(str),
            use_container_width=True
        )

# =====================================
# STATISTICS
# =====================================

elif page == "📊 Statistics":

    st.header("Dataset Statistics")

    if st.button("Show Statistical Summary"):

        st.dataframe(
            tips.describe(),
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("NumPy Analysis")

    total_bill = tips["total_bill"].to_numpy()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Maximum Bill",
            f"${np.max(total_bill):.2f}"
        )

        st.metric(
            "Mean Bill",
            f"${np.mean(total_bill):.2f}"
        )

    with col2:

        st.metric(
            "Minimum Bill",
            f"${np.min(total_bill):.2f}"
        )

        st.metric(
            "Total Revenue",
            f"${np.sum(total_bill):.2f}"
        )

    st.markdown("---")

    st.subheader("GroupBy Analysis")

    option = st.selectbox(

        "Choose Analysis",

        [

            "Average Total Bill by Day",

            "Average Tip by Gender",

            "Maximum Total Bill by Day",

            "Minimum Tip by Day",

            "Number of Customers per Day"

        ]

    )

    if option == "Average Total Bill by Day":

        result = tips.groupby("day")["total_bill"].mean()

        st.dataframe(result)

    elif option == "Average Tip by Gender":

        result = tips.groupby("sex")["tip"].mean()

        st.dataframe(result)

    elif option == "Maximum Total Bill by Day":

        result = tips.groupby("day")["total_bill"].max()

        st.dataframe(result)

    elif option == "Minimum Tip by Day":

        result = tips.groupby("day")["tip"].min()

        st.dataframe(result)

    elif option == "Number of Customers per Day":

        result = tips.groupby("day").size()

        st.dataframe(result)
# =====================================
# FILTERING
# =====================================

elif page == "🔍 Filtering":

    st.header("Filter Restaurant Data")

    gender = st.selectbox(
        "Select Gender",
        ["All"] + list(tips["sex"].unique())
    )

    smoker = st.selectbox(
        "Select Smoker",
        ["All"] + list(tips["smoker"].unique())
    )

    day = st.selectbox(
        "Select Day",
        ["All"] + list(tips["day"].unique())
    )

    min_bill = st.slider(
        "Minimum Total Bill",
        float(tips["total_bill"].min()),
        float(tips["total_bill"].max()),
        0.0
    )

    filtered = tips.copy()

    if gender != "All":
        filtered = filtered[
            filtered["sex"] == gender
        ]

    if smoker != "All":
        filtered = filtered[
            filtered["smoker"] == smoker
        ]

    if day != "All":
        filtered = filtered[
            filtered["day"] == day
        ]

    filtered = filtered[
        filtered["total_bill"] >= min_bill
    ]

    st.success(f"Number of Records : {len(filtered)}")

    st.dataframe(
        filtered,
        use_container_width=True
    )

# =====================================
# CHARTS
# =====================================

elif page == "📈 Charts":

    st.header("Restaurant Charts")

    chart = st.selectbox(

        "Choose Chart",

        [

            "Bar Chart",

            "Histogram",

            "Scatter Plot",

            "Average Tip",

            "Histogram with KDE"

        ]

    )
    # -----------------------------
    # Bar Chart
    # -----------------------------
    if chart == "Bar Chart":

        avg_bill = tips.groupby("day")["total_bill"].mean()

        fig, ax = plt.subplots(figsize=(8,5))

        ax.bar(avg_bill.index, avg_bill.values)

        ax.set_title("Average Total Bill by Day")
        ax.set_xlabel("Day")
        ax.set_ylabel("Average Total Bill")

        st.pyplot(fig)

    # -----------------------------
    # Histogram
    # -----------------------------
    elif chart == "Histogram":

        fig, ax = plt.subplots(figsize=(8,5))

        ax.hist(tips["total_bill"], bins=20)

        ax.set_title("Histogram of Total Bill")
        ax.set_xlabel("Total Bill")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)

    # -----------------------------
    # Scatter Plot
    # -----------------------------
    elif chart == "Scatter Plot":

        fig, ax = plt.subplots(figsize=(8,5))

        sns.scatterplot(
            data=tips,
            x="total_bill",
            y="tip",
            ax=ax
        )

        ax.set_title("Total Bill vs Tip")

        st.pyplot(fig)

    # -----------------------------
    # Average Tip
    # -----------------------------
    elif chart == "Average Tip":

        fig, ax = plt.subplots(figsize=(8,5))

        sns.barplot(
            data=tips,
            x="day",
            y="tip",
            ax=ax
        )

        ax.set_title("Average Tip by Day")

        st.pyplot(fig)

    # -----------------------------
    # Histogram with KDE
    # -----------------------------
    elif chart == "Histogram with KDE":

        fig, ax = plt.subplots(figsize=(8,5))

        sns.histplot(
            data=tips,
            x="total_bill",
            kde=True,
            ax=ax
        )

        ax.set_title("Histogram of Total Bill with KDE")

        st.pyplot(fig)

        fig.savefig(
            "restaurant_tips_histogram.png",
            dpi=300
        )

        with open(
            "restaurant_tips_histogram.png",
            "rb"
        ) as file:

            st.download_button(
                label="📥 Download Histogram",
                data=file,
                file_name="restaurant_tips_histogram.png",
                mime="image/png"
            )
            
# =====================================
# ABOUT
# =====================================

elif page == "ℹ️ About":

    # st.title("🍽️ Restaurant Tips Analysis")

    # st.markdown("---")

    st.subheader("About This Project")

    st.write(" 🛠 Technologies Used")

    st.write("✅ Python")
    st.write("✅ NumPy")
    st.write("✅ Pandas")
    st.write("✅ Matplotlib")
    st.write("✅ Seaborn")
    st.write("✅ Streamlit")

    st.markdown("---")

    st.write("** 📊 Dataset:** Tips Dataset from Seaborn")

    st.markdown("---")

    st.write("** ✨Features**")

    st.write("✔ Dataset Preview")
    st.write("✔ Statistical Analysis")
    st.write("✔ NumPy Analysis")
    st.write("✔ GroupBy Analysis")
    st.write("✔ Interactive Filtering")
    st.write("✔ Interactive Charts")
    st.write("✔ Download Histogram")

    st.markdown("---")

    st.markdown(
        """
        <div style='text-align:center;'>

        <b>Developed by Coding Hub</b>

        <br><br>

        © 2026 All Rights Reserved

        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(
        "Thank you for using Restaurant Tips Analysis Dashboard 💙"
    )    


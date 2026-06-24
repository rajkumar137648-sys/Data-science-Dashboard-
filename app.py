import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Data
df = pd.read_csv("employee_data.csv")

# --------------------
# DATA CLEANING
# --------------------

df["Name"] = df["Name"].str.strip()

# Gender Standardization
df["Gender"] = df["Gender"].replace({
    "M":"Male",
    "F":"Female",
    "male":"Male",
    "female":"Female"
})

# City Standardization
df["City"] = df["City"].replace({
    "london":"London",
    "New york":"New York",
    "NewYork":"New York"
})

# Department Standardization
df["Department"] = df["Department"].str.title()

# Salary Cleaning
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

# Age Cleaning
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df.loc[(df["Age"] < 18) | (df["Age"] > 70), "Age"] = None

# Remove Duplicates
df = df.drop_duplicates()

# --------------------
# TITLE
# --------------------

st.title("📊 Employee Analytics Dashboard")

# --------------------
# KPI CARDS
# --------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Employees", len(df))
col2.metric("Average Age", round(df["Age"].mean(),1))
col3.metric("Average Salary", f"₹{df['Salary'].mean():,.0f}")
col4.metric("Departments", df["Department"].nunique())

st.divider()

# --------------------
# FILTER
# --------------------

city = st.sidebar.selectbox(
    "Select City",
    ["All"] + list(df["City"].dropna().unique())
)

if city != "All":
    df = df[df["City"] == city]

# --------------------
# CHARTS
# --------------------

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        df.groupby("Department")["Salary"].mean().reset_index(),
        x="Department",
        y="Salary",
        title="Average Salary by Department"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        df,
        names="Department",
        title="Department Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------
# CITY DISTRIBUTION
# --------------------

fig = px.histogram(
    df,
    x="City",
    title="Employees by City"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# AGE DISTRIBUTION
# --------------------

fig = px.box(
    df,
    y="Age",
    title="Age Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# DATA TABLE
# --------------------

st.subheader("Employee Data")

st.dataframe(
    df,
    use_container_width=True
)

# --------------------
# AI INSIGHTS
# --------------------

st.subheader("🤖 AI Insights")

highest_salary = df.loc[df["Salary"].idxmax()]

st.success(
    f"Highest salary employee: "
    f"{highest_salary['Name']} "
    f"(₹{highest_salary['Salary']:,.0f})"
)

st.info(
    f"Average employee age is "
    f"{round(df['Age'].mean(),1)} years."
)
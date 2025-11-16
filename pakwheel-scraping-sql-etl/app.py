import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import streamlit as st
import os
import pandas as pd

# ---------------- Data Loader ----------------
@st.cache_data
def load_data():
    # First, check if file exists in the same folder
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_path, "cleaned_car_data.csv")
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        st.warning("Local CSV not found! Upload CSV manually.")
        uploaded_file = st.file_uploader("Upload cleaned_car_data.csv", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            st.stop()  # Stop execution if CSV not available
    return df

# ---------------- Load Data ----------------
df = load_data()

st.title("Car Dataset EDA & Visualization")
st.dataframe(df.head(50))


# Show raw data
st.subheader("Raw Data")
st.dataframe(df.head(50))

# Show dataset info
st.subheader("Dataset Info")
st.write(df.info())
st.write(df.describe())


# ---------------- Numeric Distribution ----------------
st.subheader("Distribution of Numeric Columns")
numeric_cols = ['price','mileage','engine','year']
fig, axes = plt.subplots(2, 2, figsize=(12,8))
axes = axes.flatten()
for i, col in enumerate(numeric_cols):
    sns.histplot(df[col], bins=20, ax=axes[i])
    axes[i].set_title(f'{col} Distribution')
    if col == 'price':
        axes[i].yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
st.pyplot(fig)


# ---------------- Scatter Plots ----------------
st.subheader("Scatter Plots")
# Price vs Mileage
fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(x='mileage', y='price', data=df, ax=ax)
ax.set_title('Price vs Mileage')
ax.set_xlabel('Mileage (km)')
ax.set_ylabel('Price (PKR)')
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
st.pyplot(fig)

# Price vs Engine
fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(x='engine', y='price', data=df, ax=ax)
ax.set_title('Price vs Engine Capacity')
ax.set_xlabel('Engine (cc or kWh)')
ax.set_ylabel('Price (PKR)')
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
st.pyplot(fig)

# ---------------- Top Brands ----------------
st.subheader("Top 10 Car Brands")
df['brand'] = df['title'].str.split(' ').str[0]
top_brands = df['brand'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x=top_brands.index, y=top_brands.values, palette='magma', ax=ax)
ax.set_ylabel('Number of Cars')
st.pyplot(fig)

# ---------------- Correlation Heatmap ----------------
st.subheader("Correlation Between Numeric Features")
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import streamlit as st
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "cleaned_car_data.csv")

df = pd.read_csv(csv_path)

st.title("Car Dataset EDA & Visualization")

# Streamlit cache
@st.cache_data
def load_data():
    df = pd.read_csv('./cleaned_car_data.csv')
    return df

df = load_data()

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
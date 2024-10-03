import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Fungsi untuk membuat DataFrame harian
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "instant": "rental_count",
        "cnt": "total_rentals"
    }, inplace=True)
    return daily_rentals_df

# Fungsi untuk analisis jumlah transaksi berdasarkan suhu
def create_temperature_analysis_df(df):
    temperature_analysis_df = df.groupby("temp_category")['cnt'].sum().reset_index()
    return temperature_analysis_df

# Fungsi untuk analisis jumlah transaksi berdasarkan waktu
def create_time_of_day_analysis_df(df):
    byday_of_time_df = df.groupby(by="time_of_day").instant.nunique().reset_index()
    byday_of_time_df.rename(columns={"instant": "cnt"}, inplace=True)
    byday_of_time_df = byday_of_time_df.sort_values(by='cnt', ascending=False)
    return byday_of_time_df

# Memuat data
main_df = pd.read_csv("main_data.csv")
main_df['dteday'] = pd.to_datetime(main_df['dteday'])

# Mengatur urutan kategori suhu
temp_order = ["Dingin", "Sejuk", "Hangat", "Panas", "Sangat Panas"]  # Ganti dengan nama kategori yang sesuai
main_df['temp_category'] = pd.Categorical(main_df['temp_category'], categories=temp_order, ordered=True)

# Mendapatkan rentang tanggal
min_date = main_df['dteday'].min()
max_date = main_df['dteday'].max()

with st.sidebar:
    # Menambahkan logo
    st.image("https://github.com/reihanalif/bike-logo/blob/main/Bike_logo.png?raw=true")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal
filtered_df = main_df[(main_df["dteday"] >= str(start_date)) & 
                       (main_df["dteday"] <= str(end_date))]

# Menghitung DataFrame yang diperlukan
daily_rentals_df = create_daily_rentals_df(filtered_df)
temperature_analysis_df = create_temperature_analysis_df(filtered_df)
time_of_day_analysis_df = create_time_of_day_analysis_df(filtered_df)

# Judul Dashboard
st.header('Dashboard Sewa Sepeda :bicyclist:')

# Menampilkan total penyewaan
total_rentals = daily_rentals_df.total_rentals.sum()
total_string = str(total_rentals) + " Record"
st.metric("Total Penyewaan Sepeda", value=total_string)

# Visualisasi penyewaan harian
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["total_rentals"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Analisis transaksi sepeda berdasarkan kategori suhu
st.subheader("Analisis Penyewaan Sepeda Berdasarkan Kategori Suhu")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="temp_category", y="cnt", data=temperature_analysis_df, palette="Blues", ax=ax)
ax.set_title("Total Penyewaan Sepeda Berdasarkan Kategori Suhu", fontsize=20)
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_xlabel("Kategori Suhu")
st.pyplot(fig)

# Analisis transaksi sepeda berdasarkan waktu
st.subheader("Analisis Penyewaan Sepeda Berdasarkan Waktu")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="time_of_day", y="cnt", data=time_of_day_analysis_df, palette="Greens", ax=ax)
ax.set_title("Total Penyewaan Sepeda Berdasarkan Waktu", fontsize=20)
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_xlabel("Waktu")
st.pyplot(fig)

# Footer
st.caption('Copyright (c) 2024 Sewa Sepeda Dashboard')
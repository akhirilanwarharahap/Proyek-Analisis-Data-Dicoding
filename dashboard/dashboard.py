import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

# Load data from CSV
all_df = pd.read_csv("/workspaces/Proyek-Analisis-Data-Dicoding/dashboard/all_data.csv")

# Konversi kolom 'dteday' menjadi datetime jika diperlukan
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

main_df = all_df[
    (all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))
]

# Visualisasi Monthly Count of Rental
st.header("Dicoding Collection Dashboard :sparkles:")
st.subheader("Monthly Count of Rental")

# Resample data by month and sum the counts
monthly_orders_df = main_df.resample(rule="M", on="dteday").agg({"cnt": "sum"})
monthly_orders_df.index = monthly_orders_df.index.strftime("%Y-%m")
monthly_orders_df = monthly_orders_df.reset_index()
monthly_orders_df.rename(columns={"cnt": "revenue"}, inplace=True)

fig, ax = plt.subplots(figsize=(10, 6))  # Mengatur ukuran plot
sns.lineplot(x="dteday", y="revenue", data=monthly_orders_df, marker="o", ax=ax)
ax.set_title("Monthly Count of Rental")  # Judul plot
ax.set_xlabel("Month")  # Label sumbu x
ax.set_ylabel("Count of Rental")  # Label sumbu y
plt.xticks(rotation=45)  # Memutar label sumbu x agar tidak bertabrakan
plt.tight_layout()  # Menyesuaikan layout agar tidak tumpang tindih

st.pyplot(fig)

# Visualisasi Total Orders by Season
st.subheader("Total Orders by Season")

# Grup berdasarkan season, menjumlahkan cnt
season_counts = main_df.groupby("season").agg({"cnt": "sum"})

fig, ax = plt.subplots(figsize=(4, 6))  # Mengatur ukuran plot
bars = ax.bar(season_counts.index, season_counts["cnt"], color="skyblue")
ax.set_title("Total Orders by Season")  # Judul plot
ax.set_xlabel("Season")  # Label sumbu x
ax.set_ylabel("Total Orders")  # Label sumbu y
plt.xticks(rotation=0)  # Memutar label sumbu x agar tidak bertabrakan
plt.tight_layout()  # Menyesuaikan layout agar tidak tumpang tindih

# Menambahkan label nilai di atas setiap bar
for bar in bars:
    yval = bar.get_height()  # Mendapatkan tinggi bar
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        int(yval),
        va="bottom",
        ha="center",
        fontsize=11,
    )

st.pyplot(fig)

st.caption("Copyright © Dicoding 2023")

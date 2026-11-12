from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.container import BarContainer
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

SEASON_ORDER = ["Spring", "Summer", "Fall", "Winter"]
WEATHER_ORDER = ["Cerah", "Berkabut/Berawan", "Hujan/Salju Ringan"]
DAY_TYPE_ORDER = ["Hari Kerja", "Hari Libur/Akhir Pekan"]
TEMP_ORDER = ["Dingin (<10 C)", "Sejuk (10 to <20 C)", "Hangat (20 to <30 C)", "Panas (>=30 C)"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


@st.cache_data
def load_data():
    df = pd.read_csv(Path(__file__).parent / "main_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


def highlight_bar(series, title, ylabel):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = ["#1f77b4" if v == series.max() else "#c7c7c7" for v in series]
    bars = ax.bar(series.index, series.values, color=colors)
    ax.bar_label(bars, fmt="%.0f", padding=3)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", labelrotation=10)
    sns.despine()
    plt.tight_layout()
    return fig


df = load_data()

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🚲 Bike Sharing")
    st.caption("Filter data yang ditampilkan")
    min_date, max_date = df["date"].min().date(), df["date"].max().date()
    date_range = st.date_input("Rentang tanggal", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)
    seasons = st.multiselect("Musim", SEASON_ORDER, default=SEASON_ORDER)
    weathers = st.multiselect("Kondisi cuaca", WEATHER_ORDER, default=WEATHER_ORDER)

if len(date_range) != 2:
    st.info("Pilih tanggal akhir pada filter rentang tanggal.")
    st.stop()

start, end = date_range
filtered = df[
    (df["date"].dt.date >= start) & (df["date"].dt.date <= end)
    & df["season"].isin(seasons) & df["weather"].isin(weathers)
]
if filtered.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()

# ---------- Header & Metrics ----------
st.title("Dashboard Analisis Penyewaan Sepeda (2011–2012)")

total = filtered["total_rentals"].sum()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Penyewaan", f"{total:,.0f}")
c2.metric("Rata-rata per Hari", f"{filtered['total_rentals'].mean():,.0f}")
c3.metric("Porsi Casual", f"{filtered['casual_users'].sum() / total * 100:.1f}%")
c4.metric("Porsi Registered", f"{filtered['registered_users'].sum() / total * 100:.1f}%")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Musim & Cuaca", "Tipe Pengguna", "Tren Bulanan", "Suhu & Permintaan"])

# ---------- Tab 1 ----------
with tab1:
    st.subheader("Musim dan cuaca apa yang paling ramai?")
    left, right = st.columns(2)
    season_avg = (filtered.groupby("season")["total_rentals"].mean()
                  .reindex(SEASON_ORDER).dropna())
    weather_avg = (filtered.groupby("weather")["total_rentals"].mean()
                   .reindex(WEATHER_ORDER).dropna())
    with left:
        st.pyplot(highlight_bar(season_avg, "Rata-rata Penyewaan per Musim",
                                "Penyewaan per hari"))
    with right:
        st.pyplot(highlight_bar(weather_avg, "Rata-rata Penyewaan per Cuaca",
                                "Penyewaan per hari"))

# ---------- Tab 2 ----------
with tab2:
    st.subheader("Casual vs Registered: hari kerja dan hari libur")
    avg = (filtered.groupby("day_type")[["casual_users", "registered_users"]]
           .mean().reindex(DAY_TYPE_ORDER).dropna(how="all"))
    avg.columns = ["Casual", "Registered"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    avg.plot(kind="bar", stacked=True, color=["#ff7f0e", "#1f77b4"], rot=0, ax=ax)
    for container in ax.containers:
        if isinstance(container, BarContainer):
            ax.bar_label(container, fmt="%.0f", label_type="center",
                         color="white", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Rata-rata penyewaan per hari")
    ax.legend(title="Tipe pengguna")
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig)

# ---------- Tab 3 ----------
with tab3:
    st.subheader("Tren penyewaan bulanan 2011 vs 2012")
    monthly = filtered.groupby(["month", "year"])["total_rentals"].sum().unstack()
    fig, ax = plt.subplots(figsize=(10, 4.5))
    palette = {"2011": "#c7c7c7", "2012": "#1f77b4"}
    for yr in monthly.columns:
        year = str(yr)
        ax.plot(monthly.index, monthly[yr], marker="o", linewidth=2.5,
                color=palette[year], label=year)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(MONTHS)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total penyewaan")
    ax.legend(title="Tahun")
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig)

# ---------- Tab 4 ----------
with tab4:
    st.subheader("Analisis lanjutan: kategori suhu vs tingkat permintaan")
    ct = pd.crosstab(filtered["temp_category"], filtered["demand_category"], normalize="index") * 100
    ct = ct.reindex(index=[t for t in TEMP_ORDER if t in ct.index],
                    columns=[d for d in ["Rendah", "Sedang", "Tinggi"] if d in ct.columns])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ct.plot(kind="bar", stacked=True, rot=0, ax=ax,
            color=["#d9d9d9", "#9ecae1", "#08519c"][: ct.shape[1]])
    for container in ax.containers:
        if isinstance(container, BarContainer):
            ax.bar_label(container, fmt="%.0f%%", label_type="center", fontsize=9)
    ax.set_xlabel("Kategori suhu")
    ax.set_ylabel("Persentase hari (%)")
    ax.legend(title="Permintaan", bbox_to_anchor=(1.02, 1), loc="upper left")
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig)
    st.caption("Binning suhu: Dingin <10 C, Sejuk 10 to <20 C, Hangat 20 to <30 C, Panas >=30 C. "
               "Permintaan: Rendah <3.000, Sedang 3.000–5.999, Tinggi >=6.000 sewa/hari.")

st.caption("Dibuat oleh [Nama kamu] • Sumber data: Bike Sharing Dataset")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis Bike Sharing", layout="wide")

# ==========================================
# 1. LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Langsung cari di folder yang sama (dashboard/)
    main_path = os.path.join(current_dir, 'main_data.csv')
    hour_path = os.path.join(current_dir, 'hour.csv') # Ubah bagian ini

    if not os.path.exists(main_path) or not os.path.exists(hour_path):
        st.error("File data tidak ditemukan! Pastikan main_data.csv dan hour.csv ada di folder dashboard.")
        return None, None

    day_df = pd.read_csv(main_path)
    hour_df = pd.read_csv(hour_path)
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df, hour_df
   
day_df, hour_df = load_data()

if day_df is not None:
    # ==========================================
    # 2. SIDEBAR
    # ==========================================
    with st.sidebar:
        st.title("🚲 Bike Sharing")
        st.image("https://raw.githubusercontent.com/dicodingacademy/dicoding-colors/main/logo.png")
        
        # Filter Tahun (Fokus pada 2012 sesuai permintaan)
        selected_year = st.selectbox("Pilih Tahun", [2012, 2011])
        yr_val = 1 if selected_year == 2012 else 0
        
        st.info("Dashboard ini menampilkan visualisasi berdasarkan temuan eksplorasi data 2012.")

    # Filter Data Utama
    main_2012 = day_df[day_df['yr'] == (2012 if selected_year == 2012 else 2011)]
    hour_2012 = hour_df[hour_df['yr'] == yr_val]

    # ==========================================
    # 3. MAIN PAGE
    # ==========================================
    st.title(f"Bike Sharing Analysis Dashboard ({selected_year}) ✨")

    # METRICS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Penyewaan", f"{main_2012['cnt'].sum():,}")
    with col2:
        st.metric("Rerata Kelembapan", f"{main_2012['hum'].mean():.2f}")
    with col3:
        st.metric("Korelasi Suhu-Sewa", f"{main_2012[['temp', 'cnt']].corr().iloc[0,1]:.2f}")

    st.divider()

    # --- VISUALISASI 1: POLA JAM-AN (REGISTERED VS CASUAL) ---
    st.subheader("1. Pola Penggunaan: Komuter (Registered) vs Wisata (Casual)")
    
    hourly_melted = hour_2012.groupby(['hr', 'workingday'])[['casual', 'registered']].mean().reset_index()
    hourly_melted['workingday_label'] = hourly_melted['workingday'].map({1: 'Hari Kerja', 0: 'Akhir Pekan'})

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=hourly_melted, x='hr', y='registered', hue='workingday_label',
                 palette=['#1f77b4', '#aec7e8'], linewidth=3, marker='o', ax=ax1)
    sns.lineplot(data=hourly_melted, x='hr', y='casual', hue='workingday_label',
                 palette=['#ff7f0e', '#ffbb78'], linewidth=3, marker='s', linestyle='--', ax=ax1)
    
    ax1.set_xlabel('Jam (00:00 - 23:00)')
    ax1.set_ylabel('Rata-rata Penyewaan')
    ax1.set_xticks(range(0, 24))
    ax1.legend(['Registered (Akhir Pekan)', 'Registered (Hari Kerja)', 
                'Casual (Akhir Pekan)', 'Casual (Hari Kerja)'], title='Tipe Pengguna')
    st.pyplot(fig1)
    st.write("**Insight:** Pengguna Registered (Komuter) mendominasi jam 8 pagi dan 5 sore, sedangkan Casual meningkat di siang hari pada akhir pekan.")

    st.divider()

    # --- VISUALISASI 2: DAMPAK LINGKUNGAN (BAR + LINE TWINX) ---
    st.subheader("2. Dampak Lingkungan: Korelasi Suhu & Cuaca")
    
    # Persiapan data bulanan
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    main_2012['mnth'] = pd.Categorical(main_2012['mnth'], categories=month_order, ordered=True)
    
    fig2, ax_bar = plt.subplots(figsize=(12, 6))
    weather_colors = {'Clear': '#f1c40f', 'Misty/Cloudy': '#3498db', 'Light Snow/Rain': '#9b59b6'}

    # Bar Chart
    sns.barplot(data=main_2012, x='mnth', y='cnt', hue='weathersit', 
                estimator=sum, palette=weather_colors, ax=ax_bar, errorbar=None, alpha=0.7)
    
    # Line Chart (TwinX)
    ax_line = ax_bar.twinx()
    monthly_temp = main_2012.groupby('mnth')['temp'].mean()
    sns.lineplot(x=monthly_temp.index, y=monthly_temp.values, color='#e74c3c', 
                 marker='D', linewidth=3, ax=ax_line, label='Suhu')
    
    ax_bar.set_ylabel('Total Penyewaan')
    ax_line.set_ylabel('Suhu (Normalized)', color='#e74c3c')
    st.pyplot(fig2)
    st.write("**Insight:** Permintaan memuncak saat suhu naik dan cuaca cerah (Clear), terutama di pertengahan tahun.")

    st.divider()

    # --- ANALISIS LANJUTAN: CLUSTERING ---
    st.subheader("3. Analisis Lanjutan: Cluster Suhu terhadap Intensitas Permintaan")
    
    # Binning Suhu
    bins_temp = [0, 0.3, 0.6, 0.8, 1]
    labels_temp = ['Cold', 'Moderate', 'Warm', 'Hot']
    main_2012['temp_cluster'] = pd.cut(main_2012['temp'], bins=bins_temp, labels=labels_temp)

    # Logic Clustering Permintaan
    q1, q3 = main_2012['cnt'].quantile(0.25), main_2012['cnt'].quantile(0.75)
    main_2012['demand_cluster'] = main_2012['cnt'].apply(
        lambda x: 'Low Demand' if x <= q1 else ('High Demand' if x > q3 else 'Medium Demand')
    )

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.countplot(data=main_2012, x='temp_cluster', hue='demand_cluster', palette='magma', ax=ax3)
    ax3.set_title('Hubungan Cluster Suhu terhadap Intensitas Permintaan')
    st.pyplot(fig3)
    
                               
    st.caption("Copyright © 2026 | Analisis Data Bike Sharing")

import streamlit as st
import numpy as np
import joblib

# ===============================
# Konfigurasi Halaman & State
# ===============================
st.set_page_config(
    page_title="Simulator Risiko Mesin",
    page_icon="🤎",
    layout="wide", # Menggunakan wide agar 2 kolom tampil sempurna
    initial_sidebar_state="collapsed"
)

# Inisialisasi Session State untuk sinkronisasi Slider & Number Input
if "suhu_num" not in st.session_state: st.session_state.suhu_num = 85.0
if "suhu_slider" not in st.session_state: st.session_state.suhu_slider = 85.0
if "get_num" not in st.session_state: st.session_state.get_num = 7.0
if "get_slider" not in st.session_state: st.session_state.get_slider = 7.0
if "hasil_simulasi" not in st.session_state: st.session_state.hasil_simulasi = 73.58 # Nilai awal mockup

def sync_suhu(key_source):
    if key_source == 'num': st.session_state.suhu_slider = st.session_state.suhu_num
    else: st.session_state.suhu_num = st.session_state.suhu_slider

def sync_getaran(key_source):
    if key_source == 'num': st.session_state.get_slider = st.session_state.get_num
    else: st.session_state.get_num = st.session_state.get_slider

# ===============================
# Load Model (Dengan Fallback UI)
# ===============================
try:
    loaded_model = joblib.load("model_risiko_v1.joblib")
    loaded_scaler = joblib.load("scaler_risiko_v1.joblib")
    model_loaded = True
except:
    model_loaded = False

# ===============================
# CSS Kustom
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Nunito:wght@400;500;600;700&display=swap');

/* Latar belakang aplikasi */
.stApp {
    background: linear-gradient(180deg, #FDF8F2 0%, #F4ECE2 100%);
    font-family: 'Nunito', sans-serif;
}

/* Modifikasi kontainer kolom menjadi Card */
div[data-testid="column"] {
    background-color: #FEFCFA;
    padding: 35px;
    border-radius: 16px;
    box-shadow: 0 4px 25px rgba(90, 62, 43, 0.05);
    border: 1px solid #F0E8DF;
}

/* Kustomisasi Tombol Utama */
div.stButton > button {
    background-color: #936952;
    color: white;
    border-radius: 12px;
    border: none;
    height: 54px;
    font-size: 16px;
    font-weight: 700;
    width: 100%;
    margin-top: 10px;
    transition: background-color 0.3s;
}
div.stButton > button:hover {
    background-color: #7A5230;
    color: white;
}

/* Kustomisasi Input Angka */
div[data-testid="stNumberInput"] input {
    background-color: #FCFAF8;
    border: 1px solid #EAE0D8;
    border-radius: 8px;
    color: #4A2E1B;
    font-weight: 600;
    padding-top: 12px;
    padding-bottom: 12px;
}

/* Kustomisasi Slider Tema Coklat */
div[data-testid="stSlider"] > div > div > div > div {
    background-color: #936952 !important;
}
div[data-testid="stSlider"] > div > div > div > div > div {
    background-color: #7A5230 !important;
    border-color: #7A5230 !important;
    box-shadow: none !important;
}

/* Spasi margin block-container atas/bawah */
div.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# Header Visual HTML
# ===============================
st.markdown("""
<div style="text-align: center; margin-bottom: 40px; margin-top: 10px;">
    <svg width="80" height="40" viewBox="0 0 80 40" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 20 H30 L35 5 L45 35 L50 20 H60" stroke="#4A2E1B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="60" cy="20" r="5" stroke="#4A2E1B" stroke-width="2"/>
        <path d="M60 13 V11 M60 29 V27 M53 20 H51 M69 20 H67 M55 15 L53.5 13.5 M65 25 L66.5 26.5 M55 25 L53.5 26.5 M65 15 L66.5 13.5" stroke="#4A2E1B" stroke-width="2" stroke-linecap="round"/>
    </svg>
    
    <h1 style="font-family: 'Playfair Display', serif; color: #4A2E1B; font-size: 46px; margin-bottom: 0px; font-weight: 600;">Simulator Risiko</h1>
    <h3 style="font-family: 'Nunito', sans-serif; color: #8F7260; font-size: 24px; font-weight: 400; margin-top: 5px;">Kegagalan Sistem</h3>
    
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin: 25px 0 15px 0;">
        <hr style="width: 60px; border-top: 1px solid #D5C2B3;">
        <div style="width: 6px; height: 6px; border-radius: 50%; background-color: #D5C2B3;"></div>
        <hr style="width: 60px; border-top: 1px solid #D5C2B3;">
    </div>
    
    <p style="color: #4A2E1B; font-size: 15px; font-weight: 500;">Masukkan kondisi mesin untuk menghitung skor risiko kegagalan sistem.</p>
</div>
""", unsafe_allow_html=True)


# ===============================
# Layout Kolom Utama
# ===============================
# Mengatur spacer (gap kosong di sisi luar agar konten berada di tengah)
_, col1, col2, _ = st.columns([0.2, 1.2, 1.3, 0.2], gap="large")


# --- KOLOM KIRI: INPUT SENSOR ---
with col1:
    st.markdown('<h4 style="color: #4A2E1B; font-weight: 700; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 25px;"><span style="margin-right: 10px; font-size: 16px;">🧪</span> INPUT SENSOR</h4>', unsafe_allow_html=True)

    # Widget Suhu Mesin
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
        <div style="background-color: #936952; width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 16px;">🌡️</div>
        <span style="font-weight: 600; color: #4A2E1B; font-size: 15px;">Suhu Mesin (°C)</span>
    </div>
    ''', unsafe_allow_html=True)
    st.number_input("Suhu Num", min_value=0.0, max_value=200.0, key="suhu_num", on_change=sync_suhu, args=('num',), label_visibility="collapsed")
    st.slider("Suhu Slider", 0.0, 200.0, key="suhu_slider", on_change=sync_suhu, args=('slider',), label_visibility="collapsed")

    st.write("") # Spacer

    # Widget Getaran Mesin
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
        <div style="background-color: #936952; width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 16px;">📉</div>
        <span style="font-weight: 600; color: #4A2E1B; font-size: 15px;">Getaran Mesin (mm/s)</span>
    </div>
    ''', unsafe_allow_html=True)
    st.number_input("Getaran Num", min_value=0.0, max_value=50.0, key="get_num", on_change=sync_getaran, args=('num',), label_visibility="collapsed")
    st.slider("Getaran Slider", 0.0, 50.0, key="get_slider", on_change=sync_getaran, args=('slider',), label_visibility="collapsed")

    st.write("") # Spacer

    # Tombol Prediksi
    prediksi = st.button("✨ Simulasikan Risiko")

    # Info Box Bawah
    st.markdown("""
    <div style="background-color: #FDF9F5; border: 1px solid #EAE0D8; padding: 15px; border-radius: 8px; display: flex; gap: 12px; align-items: flex-start; margin-top: 25px;">
        <div style="font-size: 16px; color: #4A2E1B; font-weight: bold; border: 1.5px solid #4A2E1B; border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px;">i</div>
        <span style="font-size: 13px; color: #4A2E1B; font-weight: 500; line-height: 1.4;">Pastikan nilai berada dalam rentang data pelatihan untuk hasil terbaik.</span>
    </div>
    """, unsafe_allow_html=True)


# ===============================
# Logika Pemrosesan & Prediksi
# ===============================
if prediksi:
    if model_loaded:
        data_baru = np.array([[st.session_state.suhu_num, st.session_state.get_num]])
        data_scaled = loaded_scaler.transform(data_baru)
        hasil = loaded_model.predict(data_scaled)
        st.session_state.hasil_simulasi = float(hasil[0])
    else:
        # Fallback dummy jika joblib file belum ada agar UI tetap bisa diuji (menyesuaikan input)
        mock_val = (st.session_state.suhu_num * 0.4) + (st.session_state.get_num * 6)
        st.session_state.hasil_simulasi = min(max(mock_val, 0.0), 100.0)


# --- KOLOM KANAN: HASIL SIMULASI ---
with col2:
    st.markdown('<h4 style="color: #4A2E1B; font-weight: 700; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 25px;"><span style="margin-right: 10px; font-size: 16px;">📄</span> HASIL SIMULASI</h4>', unsafe_allow_html=True)

    nilai = st.session_state.hasil_simulasi
    suhu = st.session_state.suhu_num
    getaran = st.session_state.get_num
    
    # 1. Logika Status Risiko
    if nilai < 30:
        status = "Risiko Rendah"
        bg_status = "#E8F4EC"
        dot_status = "#4CAF50"
    elif nilai < 70:
        status = "Risiko Sedang"
        bg_status = "#FFF4E5"
        dot_status = "#FF9800"
    else:
        status = "Risiko Tinggi"
        bg_status = "#FAECEB"
        dot_status = "#F44336"
        
    # 2. Logika Monitoring Warning
    if suhu > 120 or suhu < 10:
        warning_msg = "Input berada di luar jangkauan data latihan.<br>Hasil simulasi mungkin tidak akurat."
        warning_icon = "⚠️"
        warning_bg = "#F8EFEA"
    else:
        warning_msg = "Sistem Stabil. Data masih sesuai dengan<br>rentang data pelatihan model."
        warning_icon = "✅"
        warning_bg = "#E8F4EC"

    # Menyusun & Merender HTML Card Hasil (Menggantikan st.success / st.progress standar)
    st.markdown(f"""
    <div style="background-color: #FDF9F5; padding: 25px; border-radius: 12px; border: 1px solid #EAE0D8; text-align: center; margin-bottom: 20px;">
        <p style="color: #4A2E1B; font-size: 16px; margin-bottom: 5px; font-weight: 500;">Skor Risiko</p>
        <h1 style="color: #4A2E1B; font-size: 64px; font-family: 'Playfair Display', serif; margin: 0; line-height: 1.2;">{nilai:.2f}</h1>
        
        <div style="background-color: #EAE0D8; border-radius: 10px; height: 12px; width: 100%; margin-top: 15px; position: relative; overflow: hidden;">
            <div style="background-color: #936952; border-radius: 10px; height: 100%; width: {min(nilai, 100)}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #8F7260; margin-top: 8px; font-weight: 700;">
            <span>0</span><span>100</span>
        </div>
    </div>

    <div style="background-color: #FDF9F5; padding: 20px; border-radius: 12px; border: 1px solid #EAE0D8; margin-bottom: 20px;">
        <p style="color: #4A2E1B; font-size: 13px; margin-top: 0; margin-bottom: 12px; font-weight: 700;">Status Risiko</p>
        <div style="background-color: {bg_status}; padding: 10px 18px; border-radius: 8px; display: inline-flex; align-items: center; gap: 10px;">
            <div style="width: 14px; height: 14px; border-radius: 50%; background-color: {dot_status};"></div>
            <span style="font-size: 15px; font-weight: 600; color: #4A2E1B;">{status}</span>
        </div>
    </div>

    <div style="background-color: #FDF9F5; padding: 20px; border-radius: 12px; border: 1px solid #EAE0D8; margin-bottom: 20px;">
        <p style="color: #4A2E1B; font-size: 13px; margin-top: 0; margin-bottom: 12px; font-weight: 700;">
            <span style="margin-right: 5px; font-size:16px;">🛡️</span> Monitoring Sistem
        </p>
        <div style="background-color: {warning_bg}; padding: 15px; border-radius: 8px; display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 20px;">{warning_icon}</span>
            <span style="font-size: 13px; color: #4A2E1B; line-height: 1.5; font-weight: 500;">
                {warning_msg}
            </span>
        </div>
    </div>

    <div style="background-color: #FDF9F5; padding: 20px; border-radius: 12px; border: 1px solid #EAE0D8;">
        <p style="color: #4A2E1B; font-size: 13px; margin-top: 0; margin-bottom: 12px; font-weight: 700;">Ringkasan Input</p>
        <div style="display: flex; flex-direction: column; gap: 0;">
            <div style="display: flex; justify-content: space-between; padding: 12px 15px; background-color: #FAF4EF; border-bottom: 1px solid #EAE0D8; border-radius: 8px 8px 0 0;">
                <span style="color: #4A2E1B; font-size: 13.5px; font-weight: 500;"><span style="color: #936952; margin-right: 8px;">🌡️</span> Suhu Mesin</span>
                <span style="color: #4A2E1B; font-size: 13.5px; font-weight: 600;">{suhu:.2f} °C</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 12px 15px; background-color: #FAF4EF; border-radius: 0 0 8px 8px;">
                <span style="color: #4A2E1B; font-size: 13.5px; font-weight: 500;"><span style="color: #936952; margin-right: 8px;">📉</span> Getaran Mesin</span>
                <span style="color: #4A2E1B; font-size: 13.5px; font-weight: 600;">{getaran:.2f} mm/s</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# Footer Global
# ===============================
# Spacer dan Footer di tengah
_, col_footer, _ = st.columns([0.2, 2.5, 0.2])
with col_footer:
    st.markdown("""
    <div style="margin-top: 35px; padding: 20px 30px; background-color: #EFE6DD; border-radius: 12px; display: flex; align-items: center; justify-content: center; gap: 15px; border: 1px solid #E5D8CC;">
        <span style="font-size: 32px; color: #936952;">⚙️</span>
        <div>
            <p style="margin: 0; font-size: 14px; font-weight: 700; color: #4A2E1B;">Simulator Risiko Kegagalan Sistem</p>
            <p style="margin: 0; font-size: 12.5px; color: #765A46; margin-top: 3px;">Gunakan dengan bijak untuk pengambilan keputusan.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
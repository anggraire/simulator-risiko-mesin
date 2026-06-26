import streamlit as st
import numpy as np
import joblib

# ===============================
# Konfigurasi Halaman
# ===============================
st.set_page_config(
    page_title="Simulator Risiko Mesin",
    page_icon="🤎",
    layout="centered"
)

# ===============================
# CSS
# ===============================
st.markdown("""
<style>

.stApp{
    background: linear-gradient(180deg,#FDF8F2,#F4ECE2);
}

.main{
    padding-top:20px;
}

.title{
    text-align:center;
    color:#5A3E2B;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#8A6B56;
    font-size:18px;
    margin-bottom:30px;
}

.box{

    background:#FFFDFB;

    padding:35px;

    border-radius:20px;

    box-shadow:0px 8px 25px rgba(0,0,0,0.08);

}

label{
    color:#5A3E2B !important;
}

div[data-testid="stNumberInput"]{
    margin-bottom:20px;
}

div.stButton > button{

    width:100%;

    height:55px;

    border-radius:15px;

    border:none;

    background:#8B6B4A;

    color:white;

    font-size:18px;

    font-weight:bold;

}

div.stButton > button:hover{

    background:#6F4E37;

    color:white;

}

.result-card{

    background:#FFF6EA;

    padding:20px;

    border-radius:15px;

    margin-top:25px;

    text-align:center;

}

.footer{

    text-align:center;

    color:#8A6B56;

    margin-top:40px;

    font-size:14px;

}

</style>
""", unsafe_allow_html=True)

# ===============================
# Load Model
# ===============================

loaded_model = joblib.load("model_risiko_v1.joblib")
loaded_scaler = joblib.load("scaler_risiko_v1.joblib")

# ===============================
# Header
# ===============================

st.markdown(
"""
<div class="title">
🤎 Simulator Risiko Kegagalan Sistem
</div>

<div class="subtitle">
Machine Learning Deployment • MLOps • Streamlit
</div>
""",
unsafe_allow_html=True
)

# ===============================
# Card
# ===============================

st.markdown('<div class="box">', unsafe_allow_html=True)

suhu = st.number_input(
    "🌡 Suhu Mesin",
    min_value=0.0,
    value=85.0
)

getaran = st.number_input(
    "⚙ Getaran Mesin",
    min_value=0.0,
    value=7.0
)

prediksi = st.button("✨ Simulasikan Risiko")

st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# Prediksi
# ===============================

if prediksi:

    data_baru = np.array([[suhu,getaran]])

    data_scaled = loaded_scaler.transform(data_baru)

    hasil = loaded_model.predict(data_scaled)

    st.markdown(
    f"""
    <div class="result-card">

    <h2 style="color:#5A3E2B;">📊 Hasil Simulasi</h2>

    <h1 style="color:#7A5230;">
    {hasil[0]:.2f}
    </h1>

    </div>
    """,
    unsafe_allow_html=True
    )

    nilai = hasil[0]

    if nilai < 30:

        st.success("🟢 Risiko Rendah")

    elif nilai < 70:

        st.warning("🟠 Risiko Sedang")

    else:

        st.error("🔴 Risiko Tinggi")

    st.progress(min(float(nilai)/100,1.0))

    if suhu > 120 or suhu < 10:
        st.warning("⚠ Input berada di luar jangkauan data latihan. Hasil simulasi mungkin tidak akurat.")

    else:
        st.info("✅ Sistem Stabil. Data masih sesuai dengan data latihan.")

st.markdown("""
<div class="footer">
Made with 🤎 using Streamlit
</div>
""",unsafe_allow_html=True)
import streamlit as st
import numpy as np
import joblib

# =====================================
# Konfigurasi Halaman
# =====================================
st.set_page_config(
    page_title="Simulator Risiko Mesin",
    page_icon="🤎",
    layout="centered"
)

# =====================================
# Load Model
# =====================================
loaded_model = joblib.load("model_risiko_v1.joblib")
loaded_scaler = joblib.load("scaler_risiko_v1.joblib")

# =====================================
# CSS
# =====================================
st.markdown("""
<style>

.stApp{
    background-color:#F7F1EE;
}

/* Hilangkan menu & footer bawaan */
#MainMenu{
    visibility:hidden;
}
footer{
    visibility:hidden;
}
header{
    visibility:hidden;
}

.title{
    text-align:center;
    color:#51362F;
    font-size:42px;
    font-weight:700;
    margin-top:10px;
    margin-bottom:5px;
}

.subtitle{
    text-align:center;
    color:#92674D;
    font-size:17px;
    margin-bottom:35px;
}

.box{

    background:#FFFFFF;

    padding:35px;

    border-radius:25px;

    border:1px solid #EED6C7;

    box-shadow:0 10px 30px rgba(81,54,47,.12);

}

label{
    color:#51362F !important;
    font-weight:600;
}

div[data-testid="stNumberInput"]{

    margin-bottom:18px;

}

div.stButton>button{

    width:100%;

    height:55px;

    background:#92674D;

    color:white;

    border:none;

    border-radius:15px;

    font-size:18px;

    font-weight:bold;

}

div.stButton>button:hover{

    background:#704B39;

    color:white;

}

.result{

    margin-top:30px;

    background:#EED6C7;

    border-radius:20px;

    padding:25px;

    text-align:center;

    border-left:8px solid #92674D;

}

.result h2{

    color:#51362F;

}

.result h1{

    color:#704B39;

    font-size:52px;

}

.footer{

    margin-top:40px;

    text-align:center;

    color:#92674D;

    font-size:14px;

}

</style>
""", unsafe_allow_html=True)

# =====================================
# Header
# =====================================

st.markdown("""
<div class="title">
🤎 Simulator Risiko Kegagalan Sistem
</div>

<div class="subtitle">
Prediksi Risiko Berdasarkan Data Sensor Mesin
</div>
""", unsafe_allow_html=True)

# =====================================
# Input Card
# =====================================

st.markdown('<div class="box">', unsafe_allow_html=True)

suhu = st.number_input(
    "🌡️ Suhu Mesin",
    min_value=0.0,
    value=85.0,
    step=1.0
)

getaran = st.number_input(
    "⚙️ Getaran Mesin",
    min_value=0.0,
    value=7.0,
    step=1.0
)

prediksi = st.button("✨ Simulasikan Risiko")

st.markdown("</div>", unsafe_allow_html=True)

# =====================================
# Prediksi
# =====================================

if prediksi:

    data_baru = np.array([[suhu, getaran]])

    data_scaled = loaded_scaler.transform(data_baru)

    hasil = loaded_model.predict(data_scaled)

    nilai = float(hasil[0])

    st.markdown(f"""
    <div class="result">
        <h2>📊 Hasil Prediksi Risiko</h2>
        <h1>{nilai:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if nilai < 30:
        st.success("🟢 **Kategori : Risiko Rendah**")

    elif nilai < 70:
        st.warning("🟠 **Kategori : Risiko Sedang**")

    else:
        st.error("🔴 **Kategori : Risiko Tinggi**")

    st.progress(min(nilai/100,1.0))

    if suhu > 120 or suhu < 10:
        st.warning("⚠️ Input berada di luar jangkauan data latihan. Hasil simulasi mungkin tidak akurat.")
    else:
        st.info("✅ Data masih sesuai dengan data latihan.")

st.markdown("""
<div class="footer">
© 2026 • Simulator Risiko Mesin
</div>
""", unsafe_allow_html=True)
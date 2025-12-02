import streamlit as st

st.title("👥 Profil Pembuat Aplikasi")
st.write("Berikut adalah profil lengkap anggota penyusun aplikasi ini:")

# --- Styling global agar lebih rapi ---
st.markdown("""
<style>
.card {
    display: flex;
    align-items: center;
    background: #f8f9fa;
    padding: 15px;
    border-radius: 12px;
    border: 2px solid #ddd;
    margin-bottom: 25px;
}
.card img {
    width: 270px;
    height: auto;
    border-radius: 12px;
    margin-right: 25px;
}
.card .info {
    flex: 1;
}
.card h3 {
    margin: 0;
    padding: 0;
}
.card p {
    margin: 4px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Konten Profil ---
profiles = [
    {
        "name": "Moh. Trisbintang A. Menu",
        "sid": "004202400102",
        "asal": "Gorontalo",
        "tugas": "Survei, pembersihan data, pembuatan dashboard Streamlit (menu & navigasi)",
        "img": "images/tris.jpeg"
    },
    {
        "name": "Dwi Anfia Putri Wulandari",
        "sid": "004202400034",
        "asal": "Bogor",
        "tugas": "Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik",
        "img": "images/fia.jpeg"
    },
    {
        "name": "Gina Sonia",
        "sid": "004202400076",
        "asal": "Cikampek",
        "tugas": "Pembuatan laporan & bantuan olah data",
        "img": "images/gina.jpeg"
    },
    {
        "name": "Ananda Fasya Wiratama Putri",
        "sid": "004202400107",
        "asal": "Depok",
        "tugas": "Analisis hubungan variabel, penjelasan pengaruh media sosial terhadap mental, Streamlit bagian analisis",
        "img": "images/fasya.jpeg"
    }
]

# --- Render semua card ---
for p in profiles:
    st.markdown(
        f"""
        <div class="card">
            <img src="{p['img']}">
            <div class="info">
                <h3>{p['name']}</h3>
                <p><b>SID:</b> {p['sid']}</p>
                <p><b>Asal daerah:</b> {p['asal']}</p>
                <p><b>Distribusi tugas:</b> {p['tugas']}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

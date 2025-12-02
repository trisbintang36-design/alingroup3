import streamlit as st

st.title("👥 Profil Pembuat Aplikasi")

st.markdown("""
Aplikasi ini dibuat oleh kelompok yang beranggotakan empat orang.  
Berikut adalah profil lengkap beserta peran masing-masing anggota.  
""")

# Fungsi membuat kartu profil
def profile_card(name, sid, daerah, role, img):
    st.markdown(
        f"""
        <div style="
            display: flex; 
            align-items: center; 
            gap: 20px; 
            padding: 15px; 
            border-radius: 12px; 
            margin-bottom: 20px;
            border: 2px solid #dddddd;
            background-color: #f7f7f7;">
            
            <img src="{img}" width="120" style="border-radius: 10px;">

            <div>
                <h3 style="margin: 0; padding:0;">{name}</h3>
                <p style="margin: 0; padding:0;"><b>SID:</b> {sid}</p>
                <p style="margin: 0; padding:0;"><b>Asal daerah:</b> {daerah}</p>
                <p style="margin: 0; padding:0;"><b>Distribusi tugas:</b> {role}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ===============================
#         DATA ANGGOTA
# ===============================

profile_card(
    name="Moh. Trisbintang A. Menu",
    sid="004202400102",
    daerah="Gorontalo",
    role="Survei, pembersihan data, pembuatan dashboard Streamlit (menu & navigasi)",
    img="images/tris.jpeg"
)

profile_card(
    name="Dwi Anfia Putri Wulandari",
    sid="004202400034",
    daerah="Bogor",
    role="Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik",
    img="images/fia.jpeg"
)

profile_card(
    name="Gina Sonia",
    sid="004202400076",
    daerah="Cikampek",
    role="Pembuatan laporan & bantuan olah data",
    img="images/gina.jpeg"
)

profile_card(
    name="Ananda Fasya Wiratama Putri",
    sid="004202400107",
    daerah="Depok",
    role="Analisis hubungan variabel, penjelasan pengaruh media sosial terhadap mental, Streamlit bagian analisis",
    img="images/fasya.jpeg"
)

st.markdown("---")
st.info("Halaman ini menampilkan profil lengkap seluruh anggota pembuat aplikasi.")

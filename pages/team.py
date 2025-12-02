import streamlit as st

st.title("👥 Profil Pembuat Aplikasi")

st.markdown(
    """
    <h4>Berikut profil lengkap anggota penyusun aplikasi ini:</h4>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="padding:15px; border:2px solid #ddd; border-radius:10px; background:#fafafa; margin-bottom:20px;">
        <img src="images/tris.jpeg" width="120" style="border-radius: 10px; float:left; margin-right:20px;">
        <h3>Moh. Trisbintang A. Menu</h3>
        <p><b>SID:</b> 004202400102</p>
        <p><b>Asal daerah:</b> Gorontalo</p>
        <p><b>Distribusi tugas:</b> Survei, pembersihan data, pembuatan dashboard Streamlit (menu & navigasi)</p>
        <div style="clear: both;"></div>
    </div>

    <div style="padding:15px; border:2px solid #ddd; border-radius:10px; background:#fafafa; margin-bottom:20px;">
        <img src="images/fia.jpeg" width="120" style="border-radius: 10px; float:left; margin-right:20px;">
        <h3>Dwi Anfia Putri Wulandari</h3>
        <p><b>SID:</b> 004202400034</p>
        <p><b>Asal daerah:</b> Bogor</p>
        <p><b>Distribusi tugas:</b> Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik</p>
        <div style="clear: both;"></div>
    </div>

    <div style="padding:15px; border:2px solid #ddd; border-radius:10px; background:#fafafa; margin-bottom:20px;">
        <img src="images/gina.jpeg" width="120" style="border-radius: 10px; float:left; margin-right:20px;">
        <h3>Gina Sonia</h3>
        <p><b>SID:</b> 004202400076</p>
        <p><b>Asal daerah:</b> Cikampek</p>
        <p><b>Distribusi tugas:</b> Pembuatan laporan & bantuan olah data</p>
        <div style="clear: both;"></div>
    </div>

    <div style="padding:15px; border:2px solid #ddd; border-radius:10px; background:#fafafa; margin-bottom:20px;">
        <img src="images/fasya.jpeg" width="120" style="border-radius: 10px; float:left; margin-right:20px;">
        <h3>Ananda Fasya Wiratama Putri</h3>
        <p><b>SID:</b> 004202400107</p>
        <p><b>Asal daerah:</b> Depok</p>
        <p><b>Distribusi tugas:</b> Analisis hubungan variabel, penjelasan pengaruh media sosial terhadap mental, Streamlit bagian analisis</p>
        <div style="clear: both;"></div>
    </div>
    """,
    unsafe_allow_html=True
)

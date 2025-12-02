import streamlit as st

st.title("Tim Pembuat Aplikasi")
st.write("Berikut anggota tim beserta biodata dan distribusi tugas:")

# Data anggota tim
team_members = [
    {
        "name": "Moh. Trisbintang A. Menu",
        "sid": "004202400102",
        "origin": "Gorontalo",
        "tasks": "Survei, pembersihan data, pembuatan dashboard Streamlit (menu & navigasi)",
        "image": "images/tris.jpeg"
    },
    {
        "name": "Dwi Anfia Putri Wulandari",
        "sid": "004202400034",
        "origin": "Bogor",
        "tasks": "Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik",
        "image": "images/fia.jpeg"
    },
    {
        "name": "Gina Sonia",
        "sid": "004202400076",
        "origin": "Cikampek",
        "tasks": "Pembuatan laporan & bantuan olah data",
        "image": "images/gina.jpeg"
    },
    {
        "name": "Ananda Fasya Wiratama Putri",
        "sid": "004202400107",
        "origin": "Depok",
        "tasks": "Analisis hubungan variabel, penjelasan pengaruh media sosial terhadap mental, Streamlit bagian analisis",
        "image": "images/fasya.jpeg"
    },
]

# Tampilkan anggota tim
for member in team_members:
    st.image(member["image"], width=270)
    st.subheader(member["name"])
    st.write(f"**SID:** {member['sid']}")
    st.write(f"**Asal daerah:** {member['origin']}")
    st.write(f"**Distribusi tugas:** {member['tasks']}")
    
    # Spasi atau garis pemisah antar profil
    st.markdown("---")  # garis horizontal
    st.write("\n")      # jarak vertikal tambahan

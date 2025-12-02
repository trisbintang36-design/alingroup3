import streamlit as st

# ========================
# Sidebar Bahasa
# ========================
language = st.sidebar.selectbox(
    "Pilih Bahasa / Select Language / 选择语言",
    ("Indonesia", "English", "中文")
)

menu_items = {
    "Indonesia": ["Home", "Image Tools", "Team"],
    "English": ["Home", "Image Tools", "Team"],
    "中文": ["主页", "图像工具", "团队"]
}

selected_menu = st.sidebar.radio(
    "Menu" if language=="English" else "菜单" if language=="中文" else "Menu",
    menu_items[language]
)

# ========================
# Team Page
# ========================
if selected_menu == menu_items[language][2]:
    st.title("Team Members" if language=="English" else
             "团队成员" if language=="中文" else
             "Tim")

    members = [
        {"name":"Moh. Trisbintang A. Menu","sid":"004202400102","region":"Gorontalo",
         "role":"Survei, pembersihan data, dashboard Streamlit (menu & navigasi)","img":"images/tris.jpeg"},
        {"name":"Dwi Anfia Putri Wulandari","sid":"004202400034","region":"Bogor",
         "role":"Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik","img":"images/fia.jpeg"},
        {"name":"Gina Sonia","sid":"004202400076","region":"Cikampek",
         "role":"Pembuatan laporan & bantuan olah data","img":"images/gina.jpeg"},
        {"name":"Ananda Fasya Wiratama Putri","sid":"004202400107","region":"Depok",
         "role":"Analisis hubungan variabel, penjelasan pengaruh media sosial terhadap mental, Streamlit bagian analisis","img":"images/fasya.jpeg"}
    ]

    for member in members:
        cols = st.columns([1,2])
        with cols[0]:
            st.image(member["img"], width=270)
        with cols[1]:
            st.markdown(f"**{member['name']}**")
            st.markdown(f"- SID: {member['sid']}")
            st.markdown(f"- Asal daerah: {member['region']}")
            st.markdown(f"- Distribusi tugas: {member['role']}")
        st.markdown("---")

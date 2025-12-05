import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Set page config early (before any Streamlit UI calls)
st.set_page_config(page_title="Team Members", layout="wide", initial_sidebar_state="expanded")

# --- Language selection ---
LANG_OPTIONS = {"English": "en", "Bahasa Indonesia": "id"}
lang_choice = st.sidebar.selectbox("Language / Bahasa", list(LANG_OPTIONS.keys()), index=0)
lang = LANG_OPTIONS[lang_choice]

# --- Translations ---
TEXT = {
    "en": {
        "page_title": "Team Members",
        "title": "Team Members",
        "lead": "This page shows team biodata and photos. The app searches for photos in the 'images' folder. If a photo is not found, a initials avatar will be shown.",
        "sid": "SID",
        "origin": "Origin",
        "distribution": "Task distribution",
        "contrib_short": "Contributed to survey, cleaning, analysis, visualization, and building the Streamlit dashboard."
    },
    "id": {
        "page_title": "Anggota Tim",
        "title": "Anggota Tim",
        "lead": "Halaman ini menampilkan biodata tim dan foto. Aplikasi mencari foto di folder 'images'. Jika foto tidak ditemukan, avatar inisial akan ditampilkan.",
        "sid": "SID",
        "origin": "Asal daerah",
        "distribution": "Distribusi tugas",
        "contrib_short": "Berkontribusi dalam survei, pembersihan data, analisis, visualisasi, dan pembuatan dashboard Streamlit."
    }
}

t = TEXT[lang]



# Use st.markdown with HTML for styled title (st.title does not accept unsafe HTML)
st.markdown(f"<h1 style='color:#00ffe1'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='neon-box'>{t['lead']}</div>", unsafe_allow_html=True)

# --- Team biodata ---
team = [
    {
        "short": "tris",
        "full_name": "Moh. Trisbintang A. Menu",
        "distribution": "Survei, bersihkan data, dashboard Streamlit (menu & navigasi)",
        "sid": "004202400102",
        "origin": "Gorontalo",
        "photo_file": "tris.jpg",
    },
    {
        "short": "fia",
        "full_name": "Dwi Anfia Putri Wulandari",
        "distribution": "Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik",
        "sid": "004202400034",
        "origin": "Bogor",
        "photo_file": "fia.jpg",
    },
    {
        "short": "gina",
        "full_name": "Gina Sonia",
        "distribution": "Fokus laporan & bantu olah data",
        "sid": "004202400076",
        "origin": "Cikampek",
        "photo_file": "gina.jpg",
    },
    {
        "short": "fasya",
        "full_name": "Ananda Fasya Wiratama Putri",
        "distribution": "Analisis hubungan variabel, penjelasan pengaruh medsos ke mental, Streamlit bagian analisis",
        "sid": "004202400107",
        "origin": "Depok",
        "photo_file": "fasya.jpg",
    },
]

PHOTO_DIRS = ["images"]

def generate_avatar(name, size=270, bgcolor=(70,130,180)):
    initials = "".join([part[0].upper() for part in name.split()[:2]])
    img = Image.new("RGB", (size, size), bgcolor)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size // 3)
    except Exception:
        font = ImageFont.load_default()
    w, h = draw.textsize(initials, font=font)
    draw.text(((size - w) / 2, (size - h) / 2), initials, fill="white", font=font)
    return img

def find_photo_path(member, dirs):
    candidates = []
    if member.get("photo_file"):
        candidates.append(member["photo_file"])
    name_parts = [member["short"]] + member["full_name"].lower().split()
    for part in name_parts:
        candidates.append(f"{part}.jpg")
        candidates.append(f"{part}.jpeg")
        candidates.append(f"{part}.png")
    for d in dirs:
        p = Path(d)
        if not p.exists() or not p.is_dir():
            continue
        for cand in candidates:
            fpath = p / cand
            if fpath.exists():
                return str(fpath)
        for f in p.iterdir():
            if f.is_file() and member["short"].lower() in f.name.lower() and f.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                return str(f)
    return None

# Display members
for member in team:
    cols = st.columns([1, 3])
    with cols[0]:
        photo_path = find_photo_path(member, PHOTO_DIRS)
        if photo_path:
            try:
                img = Image.open(photo_path).convert("RGB")
                st.image(img, width=270)
            except Exception:
                st.warning(f"File {photo_path} found but cannot be opened. Showing avatar.")
                st.image(generate_avatar(member["full_name"]), width=270)
        else:
            st.image(generate_avatar(member["full_name"]), width=270)
    with cols[1]:
        st.markdown(f"### {member['full_name']}")
        st.markdown(f"- **{t['sid']}:** {member['sid']}")
        st.markdown(f"- **{t['origin']}:** {member['origin']}")
        st.markdown(f"- **{t['distribution']}:** {member['distribution']}")
        st.markdown(t["contrib_short"])
    st.markdown("---")


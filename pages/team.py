import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

st.set_page_config(page_title="Team Members", layout="wide")

st.title("Team Members")
st.markdown(
    "Halaman ini memuat biodata tim dan foto anggota.\n"
    "Aplikasi mencari foto di folder 'images' (relative path dari root proyek). "
    "Jika foto tidak ditemukan, avatar inisial akan ditampilkan."
)

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

# Fixed photo directory
PHOTO_DIRS = ["images"]

# Helper: generate initials avatar if photo missing
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

# Helper: try to find a photo file for a member in configured dirs
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

# Display team members (no uploader / no extra folder text)
for member in team:
    cols = st.columns([1, 3])
    with cols[0]:
        photo_path = find_photo_path(member, PHOTO_DIRS)
        if photo_path:
            try:
                img = Image.open(photo_path).convert("RGB")
                st.image(img, width=270)
            except Exception:
                st.warning(f"File {photo_path} ditemukan tapi gagal dibuka. Menampilkan avatar.")
                st.image(generate_avatar(member["full_name"]), width=270)
        else:
            st.image(generate_avatar(member["full_name"]), width=270)
    with cols[1]:
        st.markdown(f"### {member['full_name']}")
        st.markdown(f"- **SID:** {member['sid']}")
        st.markdown(f"- **Asal daerah:** {member['origin']}")
        st.markdown(f"- **Distribusi tugas:** {member['distribution']}")
        st.markdown("Singkat: Berkontribusi dalam proyek survei, pembersihan data, analisis, visualisasi, dan pembuatan dashboard Streamlit.")
    st.markdown("---")

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

st.set_page_config(page_title="Team Members", layout="wide")

st.title("Team Members")
st.markdown(
    "Halaman ini memuat biodata tim dan foto anggota.\n"
    "Secara default aplikasi mencari foto di folder 'images' (jika Anda meletakkan foto di folder lain, sebutkan path di bawah)."
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

# By default prefer 'images' folder, fallback to 'team_photos'
default_dirs = ["images", "team_photos"]

st.subheader("Pengaturan folder foto")
photo_dir_input = st.text_input(
    "Folder foto (relative path). Kosong = mencari otomatis di 'images' lalu 'team_photos'.",
    value=""
)
if photo_dir_input.strip() != "":
    PHOTO_DIRS = [photo_dir_input.strip()]
else:
    PHOTO_DIRS = default_dirs

st.markdown(
    f"- Mencari foto di (urutan): {', '.join(PHOTO_DIRS)}\n"
    "- Didukung ekstensi: .jpg, .jpeg, .png\n"
    "- Anda juga bisa mengunggah foto individu lewat uploader di bawah (akan menimpa file dari folder)."
)

# Helper: generate initials avatar if photo missing
def generate_avatar(name, size=320, bgcolor=(70,130,180)):
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
    # explicit filename first
    if member.get("photo_file"):
        candidates.append(member["photo_file"])
    # fallback patterns: short name, parts of full name
    name_parts = [member["short"]] + member["full_name"].lower().split()
    for part in name_parts:
        candidates.append(f"{part}.jpg")
        candidates.append(f"{part}.jpeg")
        candidates.append(f"{part}.png")
    # also look for any file containing short name
    for d in dirs:
        p = Path(d)
        if not p.exists() or not p.is_dir():
            continue
        for cand in candidates:
            fpath = p / cand
            if fpath.exists():
                return str(fpath)
        # pattern search: any file in dir that contains short name
        for f in p.iterdir():
            if f.is_file() and member["short"].lower() in f.name.lower() and f.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                return str(f)
    return None

st.markdown("---")
st.subheader("Upload foto per anggota (opsional)")
uploaded_photos = {}
for i, member in enumerate(team):
    key = f"upload_{member['short']}"
    uploaded = st.file_uploader(f"Upload foto untuk {member['full_name']} (opsional)", type=["jpg","jpeg","png"], key=key)
    if uploaded:
        try:
            img = Image.open(uploaded).convert("RGB")
            uploaded_photos[member["short"]] = img
        except Exception:
            st.warning(f"Gagal membuka file upload untuk {member['full_name']}. Lewati file ini.")

st.markdown("---")
st.header("Anggota Tim")
for member in team:
    cols = st.columns([1, 3])
    with cols[0]:
        # priority: uploaded override -> search in PHOTO_DIRS -> avatar
        if member["short"] in uploaded_photos:
            st.image(uploaded_photos[member["short"]], width=220)
        else:
            photo_path = find_photo_path(member, PHOTO_DIRS)
            if photo_path:
                try:
                    img = Image.open(photo_path).convert("RGB")
                    st.image(img, width=220)
                except Exception:
                    st.warning(f"File {photo_path} ditemukan tapi gagal dibuka. Menampilkan avatar.")
                    st.image(generate_avatar(member["full_name"]), width=220)
            else:
                st.image(generate_avatar(member["full_name"]), width=220)
    with cols[1]:
        st.markdown(f"### {member['full_name']}")
        st.markdown(f"- **SID:** {member['sid']}")
        st.markdown(f"- **Asal daerah:** {member['origin']}")
        st.markdown(f"- **Distribusi tugas:** {member['distribution']}")
        st.markdown("Singkat: Berkontribusi dalam proyek survei, pembersihan data, analisis, visualisasi, dan pembuatan dashboard Streamlit.")
    st.markdown("---")

st.markdown(
    "Catatan:\n"
    "- Jika Anda menaruh foto di folder `images/`, pastikan nama file sesuai (mis. tris.jpg, fia.jpg, gina.jpg, fasya.jpg) atau mengandung short name (tris, fia, gina, fasya).\n"
    "- Anda dapat mengisi field 'Folder foto' di atas untuk menunjuk folder berbeda (relative path dari root proyek).\n"
    "- Upload foto lewat uploader akan menimpa tampilan file yang ada di folder."
)

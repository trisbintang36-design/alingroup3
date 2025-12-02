import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="Matrix & Convolution — Team", layout="wide")

st.title("Team Members")
st.markdown("Daftar anggota tim dan peran mereka. Upload foto setiap anggota atau gunakan avatar default yang dibuat otomatis.")

# Default daftar tim — silakan ganti sesuai anggota Anda
team = [
    {"name": "Nama Anggota 1", "role": "Project Lead / UI"},
    {"name": "Nama Anggota 2", "role": "Image Processing / Kernels"},
    {"name": "Nama Anggota 3", "role": "Dokumentasi / Contoh"},
]

def generate_avatar(name, size=240, bgcolor=(70,130,180)):
    initials = "".join([part[0].upper() for part in name.split()][:2])
    img = Image.new("RGB", (size, size), bgcolor)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size // 3)
    except Exception:
        font = ImageFont.load_default()
    w, h = draw.textsize(initials, font=font)
    draw.text(((size-w)/2, (size-h)/2), initials, fill="white", font=font)
    return img

st.subheader("Upload foto anggota (opsional)")
uploaded = {}
for i, member in enumerate(team):
    f = st.file_uploader(f"Foto untuk {member['name']}", type=["jpg","jpeg","png"], key=f"photo_{i}")
    if f:
        uploaded[member['name']] = Image.open(f).convert("RGB")

st.markdown("---")
for member in team:
    cols = st.columns([1, 3])
    with cols[0]:
        if member['name'] in uploaded:
            st.image(uploaded[member['name']], width=200)
        else:
            st.image(generate_avatar(member['name']), width=200)
    with cols[1]:
        st.markdown(f"### {member['name']}")
        st.markdown(f"**Peran / Kontribusi:** {member['role']}")
        st.markdown("Singkat: Berkontribusi pada pengembangan aplikasi demonstrasi transformasi matrix dan konvolusi. Menguji dan menyiapkan contoh.")
st.markdown("---")
st.header("Bagaimana aplikasi bekerja (singkat)")
st.markdown(
    "1. Anda upload citra atau menggunakan citra demo.\n"
    "2. Pilih transformasi / filter di halaman Tools.\n"
    "3. Transformasi menggunakan matriks affine (rotasi, skala, shear, translasi) dan konvolusi menggunakan kernel 2D.\n"
    "4. Hasil ditampilkan berdampingan untuk dibandingkan."
)


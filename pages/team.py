import streamlit as st
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Team Members", layout="centered")
PAGE_DIR = Path(__file__).parent

# Sidebar top: Home title + Language with flags
st.sidebar.title("Home")
LANG_OPTIONS = [
    ("id", "🇮🇩 Bahasa Indonesia"),
    ("en", "🇺🇸 English"),
    ("zh", "🇨🇳 中文"),
    ("ko", "🇰🇷 한국어"),
]
lang_keys = [k for k, _ in LANG_OPTIONS]
lang_labels = {k: label for k, label in LANG_OPTIONS}
lang = st.sidebar.selectbox("Language", options=lang_keys, index=1, format_func=lambda k: lang_labels[k])

TEXT = {
    "title": {"en":"Team Members","id":"Anggota Tim","zh":"团队成员","ko":"팀원"},
    "how_it_works": {
        "en":"How the app works (short)",
        "id":"Cara kerja aplikasi (singkat)",
        "zh":"应用如何工作（简短）",
        "ko":"앱 작동 방식 (간단히)"
    },
    "note_photos": {
        "en":"Photos are loaded from assets/; replace files if you want to use different images.",
        "id":"Foto dimuat dari folder assets/; ganti file jika ingin menggunakan gambar lain.",
        "zh":"照片从 assets/ 加载；如需使用其他图像请替换文件。",
        "ko":"사진은 assets/에서 로드됩니다; 다른 이미지를 사용하려면 파일을 교체하세요."
    }
}
def t(k): return TEXT[k][lang]

st.title(t("title"))
st.markdown(t("note_photos"))

# Candidate asset directories to search for images
candidates = [
    PAGE_DIR / "assets",               # pages/assets
    PAGE_DIR.parent / "assets",        # pages/../assets
    Path.cwd() / "assets",             # project-root/assets
]

def find_image(name_base: str):
    name_base = name_base.lower()
    for d in candidates:
        if d and d.exists():
            for f in d.iterdir():
                if f.is_file() and f.name.lower().startswith(name_base):
                    return f
    return None

members = [
    {
        "name": "Moh. Trisbintang A. ⚙️",
        "photo_key": "tris",
        "role": "Menu ⚙️\nDistribusi: Survei, bersihkan data, dashboard Streamlit (menu & navigasi)",
        "sid": "004202400102",
        "origin": "Gorontalo",
    },
    {
        "name": "Dwi Anfia Putri Wulandari ⚙️",
        "photo_key": "fia",
        "role": "🛠️ Distribusi: Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik",
        "sid": "004202400034",
        "origin": "Bogor",
    },
    {
        "name": "Gina Sonia ⚙️",
        "photo_key": "gina",
        "role": "🔧 Distribusi: Fokus laporan & bantu olah data",
        "sid": "004202400076",
        "origin": "Cikampek",
    },
    {
        "name": "Ananda Fasya Wiratama Putri ⚙️",
        "photo_key": "fasya",
        "role": "⚡ Distribusi: Analisis hubungan variabel, penjelasan pengaruh medsos ke mental, Streamlit bagian analisis",
        "sid": "004202400107",
        "origin": "Depok",
    },
]

for m in members:
    cols = st.columns([1,3])
    with cols[0]:
        found = find_image(m["photo_key"])
        if found:
            st.image(Image.open(found), width=130)
        else:
            st.warning(f"Foto tidak ditemukan untuk '{m['photo_key']}' — pastikan file (contoh: {m['photo_key']}.jpeg) ada di salah satu folder: {', '.join(str(p) for p in candidates)}")
            st.image("https://via.placeholder.com/130x130.png?text=No+Photo", width=130)
    with cols[1]:
        st.subheader(m["name"])
        st.markdown(f"**SID:** {m['sid']}  \n**Asal daerah:** {m['origin']}")
        st.write(m["role"])
        st.markdown("---")

st.header(t("how_it_works"))
st.write(
    """
- Halaman Home: menjelaskan matematika di balik matriks affine dan kernel konvolusi, plus contoh visual berupa teks.
- Halaman Image Processing Tools: unggah gambar, pilih parameter transformasi (translate/rotate/scale/shear) atau pilih/edit kernel konvolusi dan lihat preview.
- Affine transforms dirangkai menjadi matriks 3x3 dan diterapkan menggunakan inverse mapping (PIL expects inverse).
- Konvolusi diterapkan per-channel menggunakan scipy.ndimage.convolve, ada opsi normalisasi kernel.
"""
)
st.info(TEXT["note_photos"]["en"] + " / " + TEXT["note_photos"]["id"])

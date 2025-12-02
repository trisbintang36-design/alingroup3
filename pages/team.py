import streamlit as st
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Team Members", layout="centered")
PAGE_DIR = Path(__file__).parent

# --- Language selector: MUST be at the very top of the sidebar ---
LANG_OPTIONS = [
    ("id", "🇮🇩 Bahasa Indonesia"),
    ("en", "🇺🇸 English"),
    ("zh", "🇨🇳 中文"),
    ("ko", "🇰🇷 한국어"),
]
lang_keys = [k for k, _ in LANG_OPTIONS]
lang_labels = {k: label for k, label in LANG_OPTIONS}
lang = st.sidebar.selectbox("Language", options=lang_keys, index=1, format_func=lambda k: lang_labels[k])

# After language selector, Home title (capitalized)
st.sidebar.title("Home")

TEXT = {
    "title": {"en":"Team Members","id":"Anggota Tim","zh":"团队成员","ko":"팀원"},
    "note_photos": {
        "en":"Photos are loaded from assets/ (recommended) or repo root. Replace files if you want to use different images.",
        "id":"Foto dimuat dari folder assets/ (direkomendasikan) atau root repo. Ganti file jika ingin menggunakan gambar lain.",
        "zh":"照片从 assets/（推荐）或仓库根目录加载。要使用其他图像请替换文件。",
        "ko":"사진은 assets/ (권장) 또는 리포지토리 루트에서 로드됩니다. 다른 이미지를 사용하려면 파일을 교체하세요."
    },
    "emoji_css_note": {
        "en":"If flag emoji do not show, custom CSS/fonts may be overriding emoji rendering. Try removing custom CSS or use image flags in assets.",
        "id":"Jika emoji bendera tidak muncul, CSS/ font kustom mungkin menimpa rendering emoji. Coba hapus CSS kustom atau gunakan gambar bendera di assets.",
        "zh":"如果旗帜表情符号未显示，自定义 CSS/字体可能覆盖了表情符号的呈现。尝试删除自定义 CSS 或在 assets 中使用图像旗帜。",
        "ko":"깃발 이모지가 표시되지 않으면 맞춤 CSS/글꼴이 이모지 렌더링을 덮어쓸 수 있습니다. 사용자 CSS를 제거하거나 assets에 이미지 깃발을 사용해보세요."
    }
}
def t(k): return TEXT[k]["en"] if lang not in TEXT[k] else TEXT[k][lang]

st.title(t("title"))
st.markdown(t("note_photos"))

# Candidate asset directories to search for images (now includes repo root and pages root)
candidates = [
    PAGE_DIR / "assets",               # pages/assets
    PAGE_DIR.parent / "assets",        # repo_root/assets
    Path.cwd() / "assets",             # project-root/assets
    Path.cwd(),                        # project root (where your screenshots show images)
    PAGE_DIR,                          # pages/  (in case images placed there)
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
        "role": "Menu ⚙️ — Distribusi: Survei, bersihkan data, dashboard Streamlit (menu & navigasi)",
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
            st.warning(f"Foto tidak ditemukan untuk '{m['photo_key']}' — periksa folders: {', '.join(str(p) for p in candidates)}")
            st.image("https://via.placeholder.com/130x130.png?text=No+Photo", width=130)
    with cols[1]:
        st.subheader(m["name"])
        st.markdown(f"**SID:** {m['sid']}  \n**Asal daerah:** {m['origin']}")
        st.write(m["role"])
        st.markdown("---")

st.info(t("emoji_css_note"))

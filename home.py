import streamlit as st
import numpy as np
from pathlib import Path

# --- Config & style ---
st.set_page_config(page_title="Matrix & Convolution Playground", layout="wide")
BASE_DIR = Path(__file__).parent

# Simple futuristic CSS
FUTURE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
.main {
    background: linear-gradient(135deg, rgba(10,10,30,0.95) 0%, rgba(18,11,43,0.9) 40%, rgba(6,12,34,0.92) 100%);
    color: #E6F0FF;
    padding: 1rem 2rem;
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
}
h1, .stTitle {
    font-family: 'Orbitron', sans-serif;
    color: #D7F0FF;
    text-shadow: 0 2px 10px rgba(0,200,255,0.08);
}
.section {
    background: rgba(255,255,255,0.03);
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 12px;
}
.small-muted {color: #bcd6ff; font-size:0.95rem;}
</style>
"""
st.markdown(FUTURE_CSS, unsafe_allow_html=True)

# --- Sidebar top: Home title + Language selector with flags ---
st.sidebar.title("Home")  # perbaikan kapitalisasi seperti permintaan
LANG_OPTIONS = [
    ("id", "🇮🇩 Bahasa Indonesia"),
    ("en", "🇺🇸 English"),
    ("zh", "🇨🇳 中文"),
    ("ko", "🇰🇷 한국어"),
]
lang_keys = [k for k, _ in LANG_OPTIONS]
lang_labels = {k: label for k, label in LANG_OPTIONS}
# Use selectbox but show flags in the display
default_index = 1 if "en" in lang_keys else 0
lang = st.sidebar.selectbox("Language", options=lang_keys, index=default_index, format_func=lambda k: lang_labels[k])

# --- Translations small table ---
T = {
    "title": {
        "en": "Matrix & Convolution Playground",
        "id": "Ruang Latihan Matriks & Konvolusi",
        "zh": "矩阵与卷积演示",
        "ko": "행렬 및 컨볼루션 실습장",
    },
    "desc": {
        "en": "Try affine matrix transforms and convolutional filters on images. Use the Image Processing Tools page to upload and experiment.",
        "id": "Coba transformasi matriks affine dan filter konvolusi pada gambar. Gunakan halaman 'Image Processing Tools' untuk mengunggah dan bereksperimen.",
        "zh": "在图像上尝试仿射矩阵变换和卷积滤波。使用“图像处理工具”页面上传并试验。",
        "ko": "이미지에서 어파인 행렬 변환과 컨볼루션 필터를 시험해 보세요. 'Image Processing Tools' 페이지에서 업로드하고 실험하세요.",
    },
    "quick_primer": {
        "en": "Quick visual primer",
        "id": "Primer visual singkat",
        "zh": "快速视觉入门",
        "ko": "빠른 시각 소개",
    },
    "mat_affine": {
        "en": "1) Matrix transformations (affine)",
        "id": "1) Transformasi matriks (affine)",
        "zh": "1）矩阵变换（仿射）",
        "ko": "1) 행렬 변환 (어파인)",
    },
    "conv": {
        "en": "2) Convolution",
        "id": "2) Konvolusi",
        "zh": "2）卷积",
        "ko": "2) 컨볼루션",
    },
    "goto_tools": {
        "en": "Go to 'Image Processing Tools' to try these kernels and transforms on your own images.",
        "id": "Pergi ke 'Image Processing Tools' untuk mencoba kernel dan transformasi ini pada gambar Anda.",
        "zh": "前往“图像处理工具”在您自己的图像上尝试这些核和变换。",
        "ko": "'Image Processing Tools'로 이동하여 자신의 이미지에서 이러한 커널과 변환을 시도하세요.",
    }
}
get = lambda k: T[k][lang]

# --- Page content ---
st.markdown(f"<div class='main'><h1>{get('title')}</h1><p class='small-muted'>{get('desc')}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='section'><h3>{get('quick_primer')}</h3></div>", unsafe_allow_html=True)

# Transform explanation only (removed arrow image as requested)
st.markdown(f"<div class='section'><h4>{get('mat_affine')}</h4>"
            "<p class='small-muted'>"
            "An affine transform is represented by a 3×3 matrix that maps coordinates [x, y, 1] → [x', y', 1]. "
            "It composes translation, rotation, scaling, and shear. In practice we build a single matrix by composing these components and apply it to image coordinates using an inverse mapping (PIL/other libraries expect the inverse affine coefficients)."
            "</p></div>", unsafe_allow_html=True)

st.markdown(f"<div class='section'><h4>{get('conv')}</h4><p class='small-muted'>Convolution applies a small kernel across an image to blur, sharpen, or detect edges. Try kernels in the Image Processing Tools page.</p></div>", unsafe_allow_html=True)

kernels = {
    "Identity": np.array([[0,0,0],[0,1,0],[0,0,0]]),
    "Box blur (3x3)": np.ones((3,3))/9.0,
    "Sharpen": np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]),
    "Sobel X (edge)": np.array([[-1,0,1],[-2,0,2],[-1,0,1]]),
}
st.markdown("<div class='section'><strong class='small-muted'>Sample kernels</strong></div>", unsafe_allow_html=True)
for name, K in kernels.items():
    st.write(f"**{name}**")
    st.write(K)

st.info(get('goto_tools'))

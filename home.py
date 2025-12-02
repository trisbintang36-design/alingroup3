import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import io
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
header .css-1v3fvcr { /* hides default Streamlit menu text slightly for cleaner */
    display: none;
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
.stButton>button {
    background: linear-gradient(90deg,#00ffa3,#00d4ff) !important;
    color: #001;
    border: none;
}
.section {
    background: rgba(255,255,255,0.03);
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 12px;
}
.lang-pill {
    background: rgba(255,255,255,0.03);
    padding: 6px 10px;
    border-radius: 999px;
    color: #cfefff;
    font-weight: 600;
    margin-right: 6px;
}
.small-muted {color: #bcd6ff; font-size:0.95rem;}
</style>
"""

st.markdown(FUTURE_CSS, unsafe_allow_html=True)

# --- Translations ---
LANGS = {
    "id": "Bahasa Indonesia",
    "en": "English",
    "zh": "中文",
    "ko": "한국어",
}
# default language selector in the top-right area via sidebar for consistency
st.sidebar.markdown("<div class='section'><strong class='small-muted'>Language / Bahasa / 语言 / 언어</strong></div>", unsafe_allow_html=True)
lang = st.sidebar.selectbox("Select language", options=list(LANGS.keys()), format_func=lambda k: LANGS[k])

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

st.markdown(f"<div class='section'><h4>{get('mat_affine')}</h4><p class='small-muted'>"
            "An affine transform is a 3x3 matrix that maps coordinates [x, y, 1] → [x', y', 1]. "
            "Common components: translation, rotation, scaling, shear."
            "</p></div>", unsafe_allow_html=True)

# Arrow demo (kept from original snippet behavior)
def make_arrow_image(size=200, color=(0, 200, 255)):
    im = Image.new("RGB", (size, size), (10, 10, 30))
    draw = ImageDraw.Draw(im)
    draw.polygon([(size*0.2, size*0.5), (size*0.7, size*0.2), (size*0.7, size*0.4),
                  (size*0.95, size*0.4), (size*0.95, size*0.6), (size*0.7, size*0.6),
                  (size*0.7, size*0.8)], fill=color)
    return im

def apply_affine_pil(img, matrix):
    mat = np.array(matrix, dtype=float)
    inv = np.linalg.inv(mat)
    a, b, c = inv[0, 0], inv[0, 1], inv[0, 2]
    d, e, f = inv[1, 0], inv[1, 1], inv[1, 2]
    return img.transform(img.size, Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC)

arrow = make_arrow_image(320)
def Tm(tx, ty): return np.array([[1,0,tx],[0,1,ty],[0,0,1]])
def Rm(deg):
    rad = np.deg2rad(deg); c,s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def Sm(sx, sy): return np.array([[sx,0,0],[0,sy,0],[0,0,1]])
def Hm(shx, shy): return np.array([[1,shx,0],[shy,1,0],[0,0,1]])

M = Tm(15, -25) @ Rm(22) @ Hm(0.25, 0) @ Sm(0.95,0.95)
trans_arrow = apply_affine_pil(arrow, M)

col1, col2 = st.columns(2)
col1.image(arrow, caption=get('mat_affine') + " — original", use_column_width=True)
col2.image(trans_arrow, caption=get('mat_affine') + " — transformed", use_column_width=True)

st.markdown(f"<div class='section'><h4>{get('conv')}</h4><p class='small-muted'>Convolution applies a kernel (small matrix) over an image. Examples: blur, sharpen, and edge detectors.</p></div>", unsafe_allow_html=True)

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

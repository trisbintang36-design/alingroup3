import streamlit as st
import numpy as np
from pathlib import Path

# --- Config & style ---
st.set_page_config(page_title="Matrix & Convolution Playground", layout="wide")
BASE_DIR = Path(__file__).parent

# --- Top-of-sidebar language selector (always at very top) ---
LANG_OPTIONS = [
    ("id", "🇮🇩 Bahasa Indonesia"),
    ("en", "🇺🇸 English"),
    ("zh", "🇨🇳 中文"),
    ("ko", "🇰🇷 한국어"),
]
lang_keys = [k for k, _ in LANG_OPTIONS]
lang_labels = {k: label for k, label in LANG_OPTIONS}
# Put language selector first in sidebar
lang = st.sidebar.selectbox("Language", options=lang_keys, index=1, format_func=lambda k: lang_labels[k])

# After language selector, show Home title (capitalized)
st.sidebar.title("Home")

# Simple translations
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
st.title(get("title"))
st.markdown(get("desc"))

st.header(get("quick_primer"))

st.subheader(get("mat_affine"))
st.write({
    "en": "An affine transform is represented by a 3×3 matrix that maps coordinates [x, y, 1] → [x', y', 1]. It composes translation, rotation, scaling, and shear.",
    "id": "Transformasi affine direpresentasikan oleh matriks 3×3 yang memetakan koordinat [x, y, 1] → [x', y', 1]. Terdiri dari translasi, rotasi, skala, dan shear.",
    "zh": "仿射变换由一个 3×3 矩阵表示，将坐标 [x, y, 1] 映射为 [x', y', 1]。它由平移、旋转、缩放和剪切组成。",
    "ko": "어파인 변환은 3×3 행렬로 표현되며 좌표 [x, y, 1] 를 [x', y', 1] 로 매핑합니다. 평행이동, 회전, 스케일, 전단으로 구성됩니다."
}[lang])

st.subheader(get("conv"))
st.write({
    "en": "Convolution applies a small kernel across image pixels to blur, sharpen, or detect edges. Try kernels in the Image Processing Tools page.",
    "id": "Konvolusi menerapkan kernel kecil pada piksel gambar untuk blur, sharpen, atau deteksi tepi. Coba kernel di halaman Image Processing Tools.",
    "zh": "卷积在图像像素上应用小核以实现模糊、锐化或边缘检测。请在“图像处理工具”页面尝试这些核。",
    "ko": "컨볼루션은 이미지를 흐리게 하거나 선명하게 하거나 에지 검출을 위해 작은 커널을 적용합니다. 'Image Processing Tools' 페이지에서 시도해 보세요."
}[lang])

st.info(get("goto_tools"))

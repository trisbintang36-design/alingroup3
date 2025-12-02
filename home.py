import streamlit as st
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
import io

# --- Language selection ---
LANG_OPTIONS = {"English": "en", "Bahasa Indonesia": "id"}
default_lang = "Bahasa Indonesia"
lang_choice = st.sidebar.selectbox("Language / Bahasa", list(LANG_OPTIONS.keys()), index=0)
lang = LANG_OPTIONS[lang_choice]

# --- Translations ---
TEXT = {
    "en": {
        "page_title": "Matrix & Convolution — Home",
        "title": "Matrix & Convolution Explorer — Home",
        "lead": "This app demonstrates basic 2D matrix transformations (rotation, scaling, translation, shear, flip) and convolutional filters on images. Use the 'Image Processing Tools' page to try interactive examples with your own images.",
        "matrix_header": "Quick Concepts",
        "affine_title": "Matrix Transformations (Affine)",
        "affine_bullets": [
            "Rotation: rotates coordinates around a center.",
            "Scaling: stretches or shrinks dimensions.",
            "Translation: moves the image position.",
            "Shear: slants shapes along X or Y.",
            "Flip: mirror horizontally or vertically."
        ],
        "conv_title": "Convolution",
        "conv_bullets": "Convolution applies a small kernel matrix over local image windows. Common kernels:\n- Blur (averaging) → smooths/noise reduction\n- Gaussian → smoother blur\n- Edge (Sobel, Laplacian) → edge detection\n- Sharpen → increases local contrast",
        "visual_examples": "Visual examples",
        "original": "Original (grid)",
        "rotated": "Rotated 30°",
        "edges": "Edges (approx)",
        "tip": "Tip: go to 'Image Processing Tools' to upload your images and try these operations interactively."
    },
    "id": {
        "page_title": "Matrix & Convolution — Beranda",
        "title": "Matrix & Convolution Explorer — Beranda",
        "lead": "Aplikasi ini menunjukkan transformasi matriks 2D dasar (rotasi, skala, translasi, shear, flip) dan filter konvolusi pada citra. Gunakan halaman 'Image Processing Tools' untuk mencoba contoh interaktif dengan citra Anda sendiri.",
        "matrix_header": "Konsep Singkat",
        "affine_title": "Transformasi Matriks (Affine)",
        "affine_bullets": [
            "Rotasi: memutar koordinat di sekitar pusat.",
            "Skala: memperbesar atau memperkecil dimensi.",
            "Translasi: memindahkan posisi citra.",
            "Shear: merenggangkan atau menyilang bentuk pada sumbu X atau Y.",
            "Flip: membalik citra secara horizontal atau vertikal."
        ],
        "conv_title": "Konvolusi",
        "conv_bullets": "Konvolusi menerapkan kernel (matriks kecil) pada jendela lokal citra. Kernel umum:\n- Blur (averaging) → meratakan / mengurangi noise\n- Gaussian → blur yang lebih halus\n- Edge (Sobel, Laplacian) → deteksi tepi\n- Sharpen → menajamkan kontras lokal",
        "visual_examples": "Contoh visual",
        "original": "Asli (grid)",
        "rotated": "Diputar 30°",
        "edges": "Tepi (aproks.)",
        "tip": "Tip: buka 'Image Processing Tools' untuk mengunggah citra dan mencoba operasi ini secara interaktif."
    }
}

t = TEXT[lang]

st.set_page_config(page_title=t["page_title"], layout="wide")
st.title(t["title"])
st.markdown(t["lead"])

st.header(t["matrix_header"])
st.subheader(t["affine_title"])
for b in t["affine_bullets"]:
    st.markdown(f"- {b}")

st.subheader(t["conv_title"])
st.markdown(t["conv_bullets"])

# Visual demo generator using PIL (no cv2)
def generate_grid_image_pil(size=512, grid_steps=8):
    img = Image.new("RGB", (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    step = max(4, size // grid_steps)
    for i in range(0, size, step):
        draw.line([(i, 0), (i, size)], fill=(220, 220, 220), width=1)
        draw.line([(0, i), (size, i)], fill=(220, 220, 220), width=1)
    draw.line([(size//4, size//4), (3*size//4, size//4)], fill=(0, 0, 200), width=6)
    arrow_head = [(3*size//4, size//4), (3*size//4 - 20, size//4 - 15), (3*size//4 - 20, size//4 + 15)]
    draw.polygon(arrow_head, fill=(0, 0, 200))
    r = 6
    cx, cy = size//2, size//2
    draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=(0, 150, 0))
    return img

def pil_rotate(img, angle):
    return img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(255,255,255))

def pil_sobel_like_edges(img):
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = edges.convert("RGB")
    return edges

demo = generate_grid_image_pil(512)
rotated = pil_rotate(demo, 30)
edges = pil_sobel_like_edges(demo)

st.header(t["visual_examples"])
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader(t["original"])
    st.image(demo, use_column_width=True)
with col2:
    st.subheader(t["rotated"])
    st.image(rotated, use_column_width=True)
with col3:
    st.subheader(t["edges"])
    st.image(edges, use_column_width=True)

st.markdown("---")
st.info(t["tip"])

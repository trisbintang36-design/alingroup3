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

st.set_page_config(page_title=t["page_title"], layout="wide", initial_sidebar_state="expanded")

# --- Futuristic theme CSS + header ---
def inject_futuristic_css():
    css = """
    <style>
    :root{
      --bg-1: #040812;
      --bg-2: #071226;
      --panel: rgba(255,255,255,0.03);
      --accent: #00ffe1;
      --accent-2: #8a2be2;
      --muted: #9aa8b2;
    }
    [data-testid="stAppViewContainer"] > .main {
      background: linear-gradient(135deg, var(--bg-1) 0%, #00121a 40%, #001824 100%);
      color: #cfeef4;
      min-height: 100vh;
      padding-top: 12px;
    }
    header[data-testid="stHeader"] {visibility: hidden;}
    footer {visibility: hidden;}
    /* Sidebar */
    [data-testid="stSidebar"] {
      background: linear-gradient(180deg, rgba(7,18,38,0.9), rgba(2,10,20,0.8));
      box-shadow: 0 8px 30px rgba(0,0,0,0.6);
      color: #cfeef4;
    }
    .css-1d391kg { background: transparent; } /* attempt to reduce white cards */
    /* Neon headings */
    h1, h2, h3 {
      color: var(--accent);
      text-shadow: 0 0 8px rgba(0,255,225,0.12), 0 0 18px rgba(138,43,226,0.06);
      font-family: "Segoe UI", Roboto, sans-serif;
    }
    .stMarkdown p, .stText {
      color: #cfeef4;
    }
    .neon-box {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border-radius: 12px;
      padding: 12px;
      box-shadow: 0 6px 30px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.02);
      border: 1px solid rgba(0,255,225,0.06);
    }
    .accent-pill {
      display:inline-block;
      padding:6px 12px;
      border-radius:20px;
      background: linear-gradient(90deg, rgba(0,255,225,0.12), rgba(138,43,226,0.08));
      color: var(--accent);
      font-weight:600;
    }
    /* Buttons */
    .stButton>button {
      background: linear-gradient(90deg, #00ffe1, #8a2be2);
      color: #021018;
      border: none;
      padding: 8px 16px;
      border-radius: 10px;
    }
    /* Make images have subtle glow */
    .stImage>div>img {
      box-shadow: 0 8px 30px rgba(0,0,0,0.6);
      border-radius: 6px;
      border: 1px solid rgba(255,255,255,0.03);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def inject_header_bar():
    header_html = f"""
    <div style="display:flex;align-items:center;gap:16px;padding:12px;border-radius:10px;margin-bottom:12px;">
      <div style="width:56px;height:56px;border-radius:12px;
                  background:linear-gradient(135deg,#00ffe1,#8a2be2);
                  display:flex;align-items:center;justify-content:center;box-shadow:0 8px 30px rgba(138,43,226,0.12);">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 12h18" stroke="#021018" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 3v18" stroke="#021018" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div>
        <div style="font-size:18px;font-weight:700;color:#e6fff7">{t['title']}</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.30)">{t['lead'][:110]}...</div>
      </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

inject_futuristic_css()
inject_header_bar()

st.title("")  # visual balance (header already shows main title)
st.markdown(f"<div class='neon-box'>{t['lead']}</div>", unsafe_allow_html=True)

st.header(t["matrix_header"])
st.subheader(t["affine_title"])
for b in t["affine_bullets"]:
    st.markdown(f"- {b}")

st.subheader(t["conv_title"])
st.markdown(t["conv_bullets"])

# Visual demo generator using PIL (no cv2)
def generate_grid_image_pil(size=512, grid_steps=8):
    img = Image.new("RGB", (size, size), (10, 18, 30))
    draw = ImageDraw.Draw(img)
    step = max(4, size // grid_steps)
    for i in range(0, size, step):
        draw.line([(i, 0), (i, size)], fill=(30, 40, 60), width=1)
        draw.line([(0, i), (size, i)], fill=(30, 40, 60), width=1)
    draw.line([(size//4, size//4), (3*size//4, size//4)], fill=(0, 255, 225), width=6)
    arrow_head = [(3*size//4, size//4), (3*size//4 - 20, size//4 - 15), (3*size//4 - 20, size//4 + 15)]
    draw.polygon(arrow_head, fill=(138, 43, 226))
    r = 6
    cx, cy = size//2, size//2
    draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=(0, 150, 0))
    return img

def pil_rotate(img, angle):
    return img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(10,18,30))

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

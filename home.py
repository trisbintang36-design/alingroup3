import streamlit as st
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
import io

st.set_page_config(page_title="Matrix & Convolution — Home", layout="wide")

st.title("Matrix & Convolution Explorer — Home")
st.markdown(
    "Aplikasi ini menunjukkan konsep dasar transformasi matriks 2D (rotasi, skala, translasi, shear, flip) "
    "dan operasi konvolusi pada citra (blur, sharpen, edge detection). Gunakan halaman 'Image Processing Tools' "
    "untuk mencoba interaktif pada citra Anda sendiri."
)

st.header("Ringkasan singkat")
st.subheader("Transformasi Matriks (Affine)")
st.markdown(
    "- Rotasi: memutar koordinat di sekitar pusat.\n"
    "- Skala: memperbesar atau memperkecil dimensi.\n"
    "- Translasi: memindahkan posisi citra.\n"
    "- Shear: merenggangkan/menyilang bentuk di sumbu X atau Y.\n"
    "- Flip: membalik citra secara horizontal/vertikal."
)

st.subheader("Konvolusi")
st.markdown(
    "Konvolusi menerapkan kernel (matriks kecil) pada jendela lokal citra. Contoh kernel umum:\n"
    "- Blur (averaging) → meratakan/noise reduction\n"
    "- Gaussian → blur yang lebih halus\n"
    "- Edge (Sobel, Laplacian) → deteksi tepi\n"
    "- Sharpen → menajamkan kontras lokal"
)

# --- Visual demo generator using PIL (no cv2) ---
def generate_grid_image_pil(size=512, grid_steps=8):
    img = Image.new("RGB", (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    step = max(4, size // grid_steps)
    for i in range(0, size, step):
        draw.line([(i, 0), (i, size)], fill=(220, 220, 220), width=1)
        draw.line([(0, i), (size, i)], fill=(220, 220, 220), width=1)
    # draw arrow (as polygon) and center dot
    # arrow shaft
    draw.line([(size//4, size//4), (3*size//4, size//4)], fill=(0, 0, 200), width=6)
    # arrow head
    arrow_head = [(3*size//4, size//4), (3*size//4 - 20, size//4 - 15), (3*size//4 - 20, size//4 + 15)]
    draw.polygon(arrow_head, fill=(0, 0, 200))
    # center dot
    r = 6
    cx, cy = size//2, size//2
    draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=(0, 150, 0))
    return img

def pil_rotate(img, angle):
    # PIL rotate rotates counter-clockwise; expand=False to keep same size
    return img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(255,255,255))

def pil_sobel_like_edges(img):
    # Use built-in FIND_EDGES for a simple demonstration (PIL). Convert to RGB for display.
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    # Increase contrast a bit by converting to 'L' then back to RGB
    edges = edges.convert("RGB")
    return edges

# generate demo images
demo = generate_grid_image_pil(512)
rotated = pil_rotate(demo, 30)
edges = pil_sobel_like_edges(demo)

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Original (grid)")
    st.image(demo, use_column_width=True)
with col2:
    st.subheader("Rotated 30°")
    st.image(rotated, use_column_width=True)
with col3:
    st.subheader("Edges (approx)")
    st.image(edges, use_column_width=True)

st.markdown("---")
st.info("Jika Anda ingin menggunakan OpenCV (cv2) untuk transformasi/konvolusi lebih lanjut, pasang paket opencv-python atau opencv-python-headless (lihat petunjuk di bawah).")

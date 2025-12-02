import streamlit as st
from PIL import Image
import numpy as np
import cv2

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

# --- Visual demo generator ---
def generate_grid_image(size=512, grid_steps=8):
    img = np.ones((size, size, 3), dtype=np.uint8) * 255
    step = max(4, size // grid_steps)
    for i in range(0, size, step):
        cv2.line(img, (i, 0), (i, size), (220, 220, 220), 1)
        cv2.line(img, (0, i), (size, i), (220, 220, 220), 1)
    cv2.arrowedLine(img, (size//4, size//4), (3*size//4, size//4), (0, 0, 200), 4, tipLength=0.2)
    cv2.circle(img, (size//2, size//2), 6, (0, 150, 0), -1)
    return img

def to_pil(img_np):
    return Image.fromarray(cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))

demo = generate_grid_image(512)

# simple rotation demo using cv2
M = cv2.getRotationMatrix2D((demo.shape[1]//2, demo.shape[0]//2), 30, 1.0)
rot = cv2.warpAffine(demo, M, (demo.shape[1], demo.shape[0]), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))

# sobel X demo
gray = cv2.cvtColor(demo, cv2.COLOR_BGR2GRAY)
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobelx = cv2.convertScaleAbs(sobelx)
sobelx_bgr = cv2.cvtColor(sobelx, cv2.COLOR_GRAY2BGR)

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Original (grid)")
    st.image(to_pil(demo), use_column_width=True)
with col2:
    st.subheader("Rotated 30°")
    st.image(to_pil(rot), use_column_width=True)
with col3:
    st.subheader("Sobel Edge (X)")
    st.image(to_pil(sobelx_bgr), use_column_width=True)

st.markdown("---")
st.info("Lanjutkan ke halaman 'Image Processing Tools' untuk mengupload citra Anda dan mencoba parameter transformasi / kernel.")

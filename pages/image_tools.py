import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import cv2
import io

st.set_page_config(page_title="Matrix & Convolution — Tools", layout="wide")

st.title("Image Processing Tools")
st.markdown("Upload gambar atau gunakan demo. Pilih transformasi atau filter di sidebar. Preview Original vs Transformed.")

# --- helper functions (embedded here so file berdiri sendiri) ---
def load_image(uploaded_file):
    if uploaded_file is None:
        return None
    image = Image.open(uploaded_file).convert("RGB")
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def pil_from_bgr(arr):
    return Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))

def generate_demo(size=512):
    img = np.ones((size, size, 3), dtype=np.uint8) * 255
    step = size // 8
    for i in range(0, size, step):
        cv2.line(img, (i,0), (i,size), (220,220,220), 1)
        cv2.line(img, (0,i), (size,i), (220,220,220), 1)
    cv2.putText(img, "DEMO", (size//6, size//2), cv2.FONT_HERSHEY_SIMPLEX, 3, (10, 10, 200), 8, cv2.LINE_AA)
    return img

# transformation implementations
def rotate_image(image, angle, center=None):
    h, w = image.shape[:2]
    if center is None:
        center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))

def scale_image(image, factor):
    h, w = image.shape[:2]
    new_w = max(1, int(w * factor))
    new_h = max(1, int(h * factor))
    scaled = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    canvas = np.ones((h, w, 3), dtype=np.uint8) * 255
    y = max(0, (h - new_h)//2)
    x = max(0, (w - new_w)//2)
    if new_h <= h and new_w <= w:
        canvas[y:y+new_h, x:x+new_w] = scaled
    else:
        canvas = scaled[0:h, 0:w]
    return canvas

def translate_image(image, tx, ty):
    h, w = image.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))

def shear_image(image, shear_x=0.0, shear_y=0.0):
    h, w = image.shape[:2]
    M = np.array([[1, shear_x, 0], [shear_y, 1, 0]], dtype=np.float32)
    return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))

def flip_image(image, mode=1):
    return cv2.flip(image, mode)

def apply_convolution(image, kernel, normalize=True):
    k = np.array(kernel, dtype=np.float32)
    s = np.sum(k)
    if normalize and abs(s) > 1e-6:
        k = k / s
    if image.ndim == 2 or image.shape[2] == 1:
        return cv2.filter2D(image, -1, k, borderType=cv2.BORDER_REPLICATE)
    else:
        chans = []
        for c in range(3):
            chans.append(cv2.filter2D(image[:,:,c], -1, k, borderType=cv2.BORDER_REPLICATE))
        merged = cv2.merge(chans)
        return np.clip(merged, 0, 255).astype(np.uint8)

def predefined_kernels():
    return {
        "blur_3": np.ones((3,3), dtype=np.float32),
        "gaussian_5": cv2.getGaussianKernel(5, -1) @ cv2.getGaussianKernel(5, -1).T,
        "sharpen": np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32),
        "sobel_x": np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32),
        "sobel_y": np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32),
        "laplacian": np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype=np.float32),
    }

# --- UI ---
uploaded = st.file_uploader("Upload image (jpg/png). Jika kosong, demo akan digunakan.", type=["jpg","jpeg","png"])
if uploaded:
    img = load_image(uploaded)
else:
    img = generate_demo(512)

st.sidebar.header("Tool selection")
tool = st.sidebar.radio("Pilih:", ["Affine Transformations", "Flip", "Convolution / Filters"])

if tool == "Affine Transformations":
    st.sidebar.subheader("Affine parameters")
    angle = st.sidebar.slider("Rotation (deg)", -180, 180, 0)
    scale = st.sidebar.slider("Scale", 0.1, 3.0, 1.0, 0.1)
    tx = st.sidebar.slider("Translate X (px)", -300, 300, 0)
    ty = st.sidebar.slider("Translate Y (px)", -300, 300, 0)
    shear_x = st.sidebar.slider("Shear X", -1.0, 1.0, 0.0, 0.01)
    shear_y = st.sidebar.slider("Shear Y", -1.0, 1.0, 0.0, 0.01)

    transformed = img.copy()
    transformed = scale_image(transformed, scale)
    transformed = rotate_image(transformed, angle)
    transformed = shear_image(transformed, shear_x, shear_y)
    transformed = translate_image(transformed, int(tx), int(ty))

    col_o, col_t = st.columns(2)
    with col_o:
        st.subheader("Original")
        st.image(pil_from_bgr(img), use_column_width=True)
    with col_t:
        st.subheader("Transformed")
        st.image(pil_from_bgr(transformed), use_column_width=True)

elif tool == "Flip":
    st.sidebar.subheader("Flip options")
    flip_mode = st.sidebar.selectbox("Mode", ["Horizontal", "Vertical", "Both"])
    mode = 1 if flip_mode=="Horizontal" else (0 if flip_mode=="Vertical" else -1)
    transformed = flip_image(img, mode)
    col_o, col_t = st.columns(2)
    with col_o:
        st.subheader("Original")
        st.image(pil_from_bgr(img), use_column_width=True)
    with col_t:
        st.subheader(f"Flipped: {flip_mode}")
        st.image(pil_from_bgr(transformed), use_column_width=True)

else:
    st.sidebar.subheader("Filter selection")
    kernels = predefined_kernels()
    choices = list(kernels.keys()) + ["Custom"]
    sel = st.sidebar.selectbox("Kernel", choices)
    if sel == "Custom":
        st.sidebar.markdown("Masukkan kernel sebagai rows dipisah ';' dan nilai dipisah koma. Contoh: 0,-1,0; -1,5,-1; 0,-1,0")
        custom = st.sidebar.text_area("Custom kernel", "0,-1,0; -1,5,-1; 0,-1,0")
        try:
            rows = [r.strip() for r in custom.split(";") if r.strip()!=""]
            kernel = np.array([[float(x) for x in row.split(",")] for row in rows], dtype=np.float32)
        except Exception:
            st.sidebar.error("Format kernel salah. Gunakan contoh di atas.")
            kernel = kernels["sharpen"]
    else:
        kernel = kernels[sel]

    normalize = st.sidebar.checkbox("Normalize kernel (sum -> 1) jika memungkinkan", value=True)
    transformed = apply_convolution(img, kernel, normalize=normalize)
    col_o, col_t = st.columns(2)
    with col_o:
        st.subheader("Original")
        st.image(pil_from_bgr(img), use_column_width=True)
    with col_t:
        st.subheader(f"Filtered: {sel}")
        st.image(pil_from_bgr(transformed), use_column_width=True)

st.markdown("---")
st.caption("Tip: Untuk hasil terbaik gunakan ukuran gambar sedang (<= 1024 px). Operasi di browser bisa lambat untuk gambar besar.")

import streamlit as st
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageChops
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import io

st.set_page_config(page_title="Matrix & Convolution — Tools (no cv2)", layout="wide")

st.title("Image Processing Tools (cv2-free)")
st.markdown("Upload gambar atau gunakan demo. Pilih transformasi atau filter di sidebar. Versi ini tidak membutuhkan OpenCV.")

# --- Helpers ---
def load_image_to_array(uploaded_file):
    if uploaded_file is None:
        return None
    pil = Image.open(uploaded_file).convert("RGB")
    return np.array(pil)

def pil_from_array(arr):
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def generate_demo_array(size=512):
    img = Image.new("RGB", (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    step = max(8, size // 8)
    for i in range(0, size, step):
        draw.line([(i, 0), (i, size)], fill=(220, 220, 220), width=1)
        draw.line([(0, i), (size, i)], fill=(220, 220, 220), width=1)
    draw.text((size//6, size//2 - 30), "DEMO", fill=(10,10,200))
    return np.array(img)

# --- Transform primitives (PIL-based) ---
def rotate_array(arr, angle):
    pil = pil_from_array(arr)
    rotated = pil.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(255,255,255))
    return np.array(rotated)

def scale_array(arr, scale_factor):
    h, w = arr.shape[:2]
    new_w = max(1, int(w * scale_factor))
    new_h = max(1, int(h * scale_factor))
    pil = pil_from_array(arr)
    scaled = pil.resize((new_w, new_h), resample=Image.BICUBIC)
    canvas = Image.new("RGB", (w, h), (255,255,255))
    paste_x = max(0, (w - new_w)//2)
    paste_y = max(0, (h - new_h)//2)
    canvas.paste(scaled, (paste_x, paste_y))
    return np.array(canvas)

def translate_array(arr, tx, ty):
    pil = pil_from_array(arr)
    # ImageChops.offset shifts image; positive tx moves right, positive ty moves down
    shifted = ImageChops.offset(pil, tx, ty)
    # fill exposed area with white
    if tx > 0:
        draw = ImageDraw.Draw(shifted)
        draw.rectangle([0, 0, tx-1, pil.height], fill=(255,255,255))
    elif tx < 0:
        draw = ImageDraw.Draw(shifted)
        draw.rectangle([pil.width + tx, 0, pil.width-1, pil.height], fill=(255,255,255))
    if ty > 0:
        draw = ImageDraw.Draw(shifted)
        draw.rectangle([0, 0, pil.width, ty-1], fill=(255,255,255))
    elif ty < 0:
        draw = ImageDraw.Draw(shifted)
        draw.rectangle([0, pil.height + ty, pil.width, pil.height-1], fill=(255,255,255))
    return np.array(shifted)

def shear_array(arr, shear_x=0.0, shear_y=0.0):
    pil = pil_from_array(arr)
    w, h = pil.size
    # PIL affine expects a 6-tuple (a, b, c, d, e, f) mapping:
    # x_in = a*x_out + b*y_out + c
    # y_in = d*x_out + e*y_out + f
    # For a shear on X by shx: matrix [[1, shx], [0,1]]
    a = 1.0
    b = shear_x
    c = 0.0
    d = shear_y
    e = 1.0
    f = 0.0
    sheared = pil.transform((w, h), Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC, fillcolor=(255,255,255))
    return np.array(sheared)

def flip_array(arr, mode):
    pil = pil_from_array(arr)
    if mode == "Horizontal":
        return np.array(pil.transpose(Image.FLIP_LEFT_RIGHT))
    elif mode == "Vertical":
        return np.array(pil.transpose(Image.FLIP_TOP_BOTTOM))
    else:
        # both
        return np.array(pil.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))

# --- Convolution using numpy sliding_window_view ---
def apply_convolution_array(arr, kernel, normalize=True):
    k = np.array(kernel, dtype=np.float32)
    kh, kw = k.shape
    if normalize:
        s = k.sum()
        if abs(s) > 1e-6:
            k = k / s
    pad_h = kh // 2
    pad_w = kw // 2
    if arr.ndim == 2:
        padded = np.pad(arr, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
        patches = sliding_window_view(padded, (kh, kw))
        # patches shape (H, W, kh, kw)
        out = np.tensordot(patches, k, axes=([2,3],[0,1]))
        return np.clip(out, 0, 255).astype(np.uint8)
    else:
        H, W, C = arr.shape
        out = np.zeros_like(arr, dtype=np.float32)
        for ch in range(C):
            padded = np.pad(arr[:,:,ch], ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
            patches = sliding_window_view(padded, (kh, kw))
            conv_ch = np.tensordot(patches, k, axes=([2,3],[0,1]))
            out[:,:,ch] = conv_ch
        return np.clip(out, 0, 255).astype(np.uint8)

def predefined_kernels():
    return {
        "blur_3": np.ones((3,3), dtype=np.float32),
        "gaussian_5": (np.array([[1,4,6,4,1],
                                 [4,16,24,16,4],
                                 [6,24,36,24,6],
                                 [4,16,24,16,4],
                                 [1,4,6,4,1]], dtype=np.float32)),
        "sharpen": np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32),
        "sobel_x": np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32),
        "sobel_y": np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32),
        "laplacian": np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype=np.float32),
    }

# --- UI ---
uploaded = st.file_uploader("Upload image (jpg/png). Jika kosong, demo akan digunakan.", type=["jpg","jpeg","png"])
if uploaded:
    img_arr = load_image_to_array(uploaded)
else:
    img_arr = generate_demo_array(512)

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

    transformed = img_arr.copy()
    transformed = scale_array(transformed, scale)
    transformed = rotate_array(transformed, angle)
    transformed = shear_array(transformed, shear_x, shear_y)
    transformed = translate_array(transformed, int(tx), int(ty))

    col_o, col_t = st.columns(2)
    with col_o:
        st.subheader("Original")
        st.image(pil_from_array(img_arr), use_column_width=True)
    with col_t:
        st.subheader("Transformed")
        st.image(pil_from_array(transformed), use_column_width=True)

elif tool == "Flip":
    st.sidebar.subheader("Flip options")
    flip_mode = st.sidebar.selectbox("Mode", ["Horizontal", "Vertical", "Both"])
    transformed = flip_array(img_arr, flip_mode)
    col_o, col_t = st.columns(2)
    with col_o:
        st.subheader("Original")
        st.image(pil_from_array(img_arr), use_column_width=True)
    with col_t:
        st.subheader(f"Flipped: {flip_mode}")
        st.image(pil_from_array(transformed), use_column_width=True)

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
    transformed = apply_convolution_array(img_arr, kernel, normalize=normalize)

    col_o, col_t = st.columns(2)
    with col_o:
        st.subheader("Original")
        st.image(pil_from_array(img_arr), use_column_width=True)
    with col_t:
        st.subheader(f"Filtered: {sel}")
        st.image(pil_from_array(transformed), use_column_width=True)

st.markdown("---")
st.caption("Versi ini tidak memerlukan OpenCV. Jika Anda lebih suka versi berbasis OpenCV, pasang paket opencv-python(-headless) dan gunakan file image_tools yang memakai cv2.")

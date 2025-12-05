import streamlit as st
from PIL import Image, ImageOps, ImageDraw
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

# --- Language selection ---
LANG_OPTIONS = {"English": "en", "Bahasa Indonesia": "id"}
lang_choice = st.sidebar.selectbox("Language / Bahasa", list(LANG_OPTIONS.keys()), index=0)
lang = LANG_OPTIONS[lang_choice]

# --- Translations ---
TEXT = {
    "en": {
        "page_title": "Image Processing Tools",
        "title": "Image Processing Tools",
        "lead": "Upload an image or use the demo. Choose transformation or filter in the sidebar. Preview Original vs Transformed.",
        "upload": "Upload image (jpg/png). If empty, demo will be used.",
        "tools": "Tool selection",
        "affine": "Affine Transformations",
        "flip": "Flip",
        "conv": "Convolution / Filters",
        "rotation": "Rotation (deg)",
        "scale": "Scale",
        "translate_x": "Translate X (px)",
        "translate_y": "Translate Y (px)",
        "shear_x": "Shear X",
        "shear_y": "Shear Y",
        "original": "Original",
        "transformed": "Transformed",
        "flip_mode": "Mode",
        "filter_selection": "Filter selection",
        "custom_kernel_help": "Enter kernel as rows separated by ';' and values by commas. Example: 0,-1,0; -1,5,-1; 0,-1,0",
        "normalize": "Normalize kernel (sum -> 1) if possible",
        "tip": "Tip: Use medium-size images (<= 1024 px) for best responsiveness."
    },
    "id": {
        "page_title": "Alat Pengolahan Citra",
        "title": "Alat Pengolahan Citra",
        "lead": "Unggah gambar atau gunakan demo. Pilih transformasi atau filter di sidebar. Pratinjau Asli vs Hasil.",
        "upload": "Unggah gambar (jpg/png). Jika kosong, demo akan digunakan.",
        "tools": "Pemilihan alat",
        "affine": "Transformasi Affine",
        "flip": "Flip",
        "conv": "Konvolusi / Filter",
        "rotation": "Rotasi (deg)",
        "scale": "Skala",
        "translate_x": "Translasi X (px)",
        "translate_y": "Translasi Y (px)",
        "shear_x": "Shear X",
        "shear_y": "Shear Y",
        "original": "Asli",
        "transformed": "Hasil",
        "flip_mode": "Mode",
        "filter_selection": "Pemilihan filter",
        "custom_kernel_help": "Masukkan kernel sebagai baris dipisah ';' dan nilai dipisah koma. Contoh: 0,-1,0; -1,5,-1; 0,-1,0",
        "normalize": "Normalisasi kernel (jumlah -> 1) jika memungkinkan",
        "tip": "Tip: Gunakan gambar ukuran sedang (<= 1024 px) untuk respons terbaik."
    }
}

t = TEXT[lang]

st.set_page_config(page_title=t["page_title"], layout="wide", initial_sidebar_state="expanded")


# Replace st.title(...) with st.markdown containing an <h1> so we can use unsafe HTML
st.markdown(f"<h1 style='color:#00ffe1'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='neon-box'>{t['lead']}</div>", unsafe_allow_html=True)

# --- helpers (cv2-free) ---
def load_image_to_array(uploaded_file):
    if uploaded_file is None:
        return None
    pil = Image.open(uploaded_file).convert("RGB")
    return np.array(pil)

def pil_from_array(arr):
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def generate_demo_array(size=512):
    img = Image.new("RGB", (size, size), (10, 18, 30))
    draw = ImageDraw.Draw(img)
    step = max(8, size // 8)
    for i in range(0, size, step):
        draw.line([(i,0), (i,size)], fill=(30,40,60), width=1)
        draw.line([(0,i), (size,i)], fill=(30,40,60), width=1)
    draw.text((size//6, size//2 - 30), "DEMO", fill=(0,255,225))
    return np.array(img)

def rotate_array(arr, angle):
    pil = pil_from_array(arr)
    return np.array(pil.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(10,18,30)))

def scale_array(arr, scale_factor):
    h, w = arr.shape[:2]
    new_w = max(1, int(w * scale_factor))
    new_h = max(1, int(h * scale_factor))
    pil = pil_from_array(arr)
    scaled = pil.resize((new_w, new_h), resample=Image.BICUBIC)
    canvas = Image.new("RGB", (w, h), (10,18,30))
    paste_x = max(0, (w - new_w)//2)
    paste_y = max(0, (h - new_h)//2)
    canvas.paste(scaled, (paste_x, paste_y))
    return np.array(canvas)

def translate_array(arr, tx, ty):
    pil = pil_from_array(arr)
    w, h = pil.size
    return np.array(pil.transform((w, h), Image.AFFINE, (1, 0, tx, 0, 1, ty), resample=Image.BICUBIC, fillcolor=(10,18,30)))

def shear_array(arr, shear_x=0.0, shear_y=0.0):
    pil = pil_from_array(arr)
    w, h = pil.size
    a = 1.0
    b = shear_x
    c = 0.0
    d = shear_y
    e = 1.0
    f = 0.0
    return np.array(pil.transform((w, h), Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC, fillcolor=(10,18,30)))

def flip_array(arr, mode):
    pil = pil_from_array(arr)
    if mode == "Horizontal":
        return np.array(pil.transpose(Image.FLIP_LEFT_RIGHT))
    elif mode == "Vertical":
        return np.array(pil.transpose(Image.FLIP_TOP_BOTTOM))
    else:
        return np.array(pil.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))

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
uploaded = st.file_uploader(t["upload"], type=["jpg","jpeg","png"])
if uploaded:
    img_arr = load_image_to_array(uploaded)
else:
    img_arr = generate_demo_array(512)

st.sidebar.header(t["tools"])
tool = st.sidebar.radio("", [t["affine"], t["flip"], t["conv"]])

if tool == t["affine"]:
    st.sidebar.subheader(t["affine"])
    angle = st.sidebar.slider(t["rotation"], -180, 180, 0)
    scale = st.sidebar.slider(t["scale"], 0.1, 3.0, 1.0, 0.1)
    tx = st.sidebar.slider(t["translate_x"], -300, 300, 0)
    ty = st.sidebar.slider(t["translate_y"], -300, 300, 0)
    shear_x = st.sidebar.slider(t["shear_x"], -1.0, 1.0, 0.0, 0.01)
    shear_y = st.sidebar.slider(t["shear_y"], -1.0, 1.0, 0.0, 0.01)

    transformed = img_arr.copy()
    transformed = scale_array(transformed, scale)
    transformed = rotate_array(transformed, angle)
    transformed = shear_array(transformed, shear_x, shear_y)
    transformed = translate_array(transformed, int(tx), int(ty))

    col_o, col_t = st.columns(2)
    with col_o:
        st.subheader(t["original"])
        st.image(Image.fromarray(img_arr), use_column_width=True)
    with col_t:
        st.subheader(t["transformed"])
        st.image(Image.fromarray(transformed), use_column_width=True)

elif tool == t["flip"]:
    st.sidebar.subheader(t["flip"])
    flip_mode = st.sidebar.selectbox(t["flip_mode"], ["Horizontal", "Vertical", "Both"])
    transformed = flip_array(img_arr, flip_mode)
    col_o, col_t = st.columns(2)
    with col_o:
        st.subheader(t["original"])
        st.image(Image.fromarray(img_arr), use_column_width=True)
    with col_t:
        st.subheader(f"{t['transformed']}: {flip_mode}")
        st.image(Image.fromarray(transformed), use_column_width=True)

else:
    st.sidebar.subheader(t["filter_selection"])
    kernels = predefined_kernels()
    choices = list(kernels.keys()) + ["Custom"]
    sel = st.sidebar.selectbox("", choices)
    if sel == "Custom":
        st.sidebar.markdown(t["custom_kernel_help"])
        custom = st.sidebar.text_area("Custom kernel", "0,-1,0; -1,5,-1; 0,-1,0")
        try:
            rows = [r.strip() for r in custom.split(";") if r.strip()!=""]
            kernel = np.array([[float(x) for x in row.split(",")] for row in rows], dtype=np.float32)
        except Exception:
            st.sidebar.error("Invalid kernel format.")
            kernel = kernels["sharpen"]
    else:
        kernel = kernels[sel]

    normalize = st.sidebar.checkbox(t["normalize"], value=True)
    transformed = apply_convolution_array(img_arr, kernel, normalize=normalize)

    col_o, col_t = st.columns(2)
    with col_o:
        st.subheader(t["original"])
        st.image(Image.fromarray(img_arr), use_column_width=True)
    with col_t:
        st.subheader(f"{t['transformed']}: {sel}")
        st.image(Image.fromarray(transformed), use_column_width=True)

st.markdown("---")
st.caption(t["tip"])


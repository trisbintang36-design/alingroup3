import streamlit as st
from PIL import Image
import numpy as np
import io
from scipy import ndimage
from pathlib import Path

st.set_page_config(page_title="Image Processing Tools", layout="wide")
PAGE_DIR = Path(__file__).parent

# Sidebar: Home title + Language with flags (at top)
st.sidebar.title("Home")
LANG_OPTIONS = [
    ("id", "🇮🇩 Bahasa Indonesia"),
    ("en", "🇺🇸 English"),
    ("zh", "🇨🇳 中文"),
    ("ko", "🇰🇷 한국어"),
]
lang_keys = [k for k, _ in LANG_OPTIONS]
lang_labels = {k: label for k, label in LANG_OPTIONS}
lang = st.sidebar.selectbox("Language", options=lang_keys, index=1, format_func=lambda k: lang_labels[k])

T = {
    "title": {"en":"Image Processing Tools","id":"Alat Pengolahan Gambar","zh":"图像处理工具","ko":"이미지 처리 도구"},
    "upload": {"en":"Upload an image (png/jpg/bmp)","id":"Unggah gambar (png/jpg/bmp)","zh":"上传图像 (png/jpg/bmp)","ko":"이미지 업로드 (png/jpg/bmp)"},
    "mode": {"en":"Mode","id":"Mode","zh":"模式","ko":"모드"},
    "transformations": {"en":"Transformations","id":"Transformasi","zh":"变换","ko":"변환"},
    "filters": {"en":"Filters","id":"Filter","zh":"滤波器","ko":"필터"},
    "download": {"en":"Download PNG","id":"Unduh PNG","zh":"下载 PNG","ko":"PNG 다운로드"},
    "example_info": {"en":"Upload an image to begin. Example will be used if none uploaded.","id":"Unggah gambar untuk memulai. Contoh akan digunakan jika tidak ada yang diunggah.","zh":"上传图像以开始。如果没有上传将使用示例。","ko":"시작하려면 이미지를 업로드하세요. 업로드하지 않으면 예제가 사용됩니다."},
}
get = lambda k: T[k][lang]

st.title(get("title"))

uploaded = st.file_uploader(get("upload"), type=["png","jpg","jpeg","bmp"], accept_multiple_files=False)
if not uploaded:
    st.info(get("example_info"))
    try:
        from urllib.request import urlopen
        example_url = "https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=800&q=80"
        with urlopen(example_url) as resp:
            uploaded = io.BytesIO(resp.read())
    except Exception:
        uploaded = None

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.sidebar.header(get("mode"))
    mode = st.sidebar.radio("", [get("transformations"), get("filters")])

    col_orig, col_proc = st.columns([1,1])
    col_orig.image(img, caption="Original", use_column_width=True)

    def apply_affine_pil(img, matrix):
        mat = np.array(matrix, dtype=float)
        inv = np.linalg.inv(mat)
        a, b, c = inv[0, 0], inv[0, 1], inv[0, 2]
        d, e, f = inv[1, 0], inv[1, 1], inv[1, 2]
        return img.transform(img.size, Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC)

    if mode == get("transformations"):
        st.sidebar.subheader("Affine parameters")
        tx = st.sidebar.slider("Translate X (px)", -300, 300, 0)
        ty = st.sidebar.slider("Translate Y (px)", -300, 300, 0)
        angle = st.sidebar.slider("Rotation (deg)", -180, 180, 0)
        sx = st.sidebar.slider("Scale X", 0.1, 3.0, 1.0, 0.05)
        sy = st.sidebar.slider("Scale Y", 0.1, 3.0, 1.0, 0.05)
        shx = st.sidebar.slider("Shear X", -1.0, 1.0, 0.0, 0.01)
        shy = st.sidebar.slider("Shear Y", -1.0, 1.0, 0.0, 0.01)
        center = st.sidebar.checkbox("Rotate about image center", value=True)

        st.markdown("Affine transform explanation:")
        st.write("An affine transform composes translation, rotation, scaling and shear into a single 3x3 matrix. The app composes these and applies via inverse mapping (no arrow image here — explanation only).")

        def T(tx, ty): return np.array([[1,0,tx],[0,1,ty],[0,0,1]])
        def R(deg):
            r = np.deg2rad(deg); c,s = np.cos(r), np.sin(r)
            return np.array([[c,-s,0],[s,c,0],[0,0,1]])
        def S(sx, sy): return np.array([[sx,0,0],[0,sy,0],[0,0,1]])
        def H(shx, shy): return np.array([[1,shx,0],[shy,1,0],[0,0,1]])

        w,h = img.size
        if center:
            to_center = T(-w/2, -h/2)
            back = T(w/2, h/2)
            M = back @ T(tx,ty) @ R(angle) @ H(shx, shy) @ S(sx,sy) @ to_center
        else:
            M = T(tx,ty) @ R(angle) @ H(shx, shy) @ S(sx,sy)

        processed = apply_affine_pil(img, M)
        col_proc.image(processed, caption="Transformed", use_column_width=True)

    else:
        st.sidebar.subheader("Filter / Kernel")
        filter_choice = st.sidebar.selectbox("Choose filter", ["Identity","Box blur (3x3)","Gaussian-ish blur (5x5)","Sharpen","Sobel X","Sobel Y","Custom 3x3"])
        if filter_choice == "Identity":
            kernel = np.array([[0,0,0],[0,1,0],[0,0,0]])
        elif filter_choice == "Box blur (3x3)":
            kernel = np.ones((3,3))/9.0
        elif filter_choice == "Gaussian-ish blur (5x5)":
            g1 = np.array([1,4,6,4,1])
            k5 = np.outer(g1,g1)
            kernel = k5 / k5.sum()
        elif filter_choice == "Sharpen":
            kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
        elif filter_choice == "Sobel X":
            kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        elif filter_choice == "Sobel Y":
            kernel = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
        else:
            st.sidebar.markdown("Edit 3x3 kernel values")
            vals = []
            for r in range(3):
                cols = st.sidebar.columns(3)
                row = []
                for c in range(3):
                    key = f"k_{r}_{c}"
                    row.append(cols[c].number_input(f"{r},{c}", value=0.0, format="%.3f", key=key))
                vals.append(row)
            kernel = np.array(vals, dtype=float)

        normalize = st.sidebar.checkbox("Normalize kernel (sum to 1)", value=("Box blur" in filter_choice or "Gaussian" in filter_choice))
        if normalize:
            s = kernel.sum()
            if s != 0:
                kernel = kernel / s

        st.sidebar.write("Kernel:")
        st.sidebar.write(kernel)

        arr = np.asarray(img).astype(np.float32)
        if arr.ndim == 3:
            out = np.zeros_like(arr)
            for ch in range(arr.shape[2]):
                out[:,:,ch] = ndimage.convolve(arr[:,:,ch], kernel, mode='reflect')
            out = np.clip(out, 0, 255).astype(np.uint8)
        else:
            out = ndimage.convolve(arr, kernel, mode='reflect')
            out = np.clip(out, 0, 255).astype(np.uint8)

        processed = Image.fromarray(out)
        col_proc.image(processed, caption=f"Filtered: {filter_choice}", use_column_width=True)

    st.markdown("---")
    buf = io.BytesIO()
    processed.save(buf, format="PNG")
    st.download_button(get("download"), data=buf.getvalue(), file_name="processed.png", mime="image/png")

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from pathlib import Path
import os

# --- Page / App config ---
st.set_page_config(page_title="Matrix & Convolution Explorer", layout="wide", initial_sidebar_state="expanded")

# --- Single language selection stored in session_state ---
LANG_OPTIONS = {"English": "en", "Bahasa Indonesia": "id"}
if "lang" not in st.session_state:
    st.session_state.lang = "id"  # default bahasa indonesia

# --- Theme selection stored in session_state (new) ---
if "theme" not in st.session_state:
    st.session_state.theme = "auto"  # auto = follow system prefers-color-scheme

# --- Futuristic theme CSS (media-query + force classes) ---
def inject_futuristic_css():
    css = """
    <style>
    /* Default: follow system preference */
    @media (prefers-color-scheme: dark) {
      :root {
        --bg-main: #030612;
        --text-main: #cfeef4;
        --accent: #00ffe1;
        --button-text: #021018;
      }
      [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(135deg, #030612 0%, #00121a 60%);
        color: var(--text-main);
        min-height: 100vh;
      }
      /* IMPORTANT: do not force a custom background on the sidebar.
         Use 'unset' so the sidebar can follow Streamlit/browser/system defaults. */
      [data-testid="stSidebar"] {
        background: unset !important;
        color: inherit !important;
      }
      h1,h2,h3 { color: var(--accent); text-shadow: 0 0 8px rgba(0,255,225,0.08); }
      .neon-box { background: rgba(255,255,255,0.02); padding:12px; border-radius:12px; border:1px solid rgba(0,255,225,0.04); }
      .stButton>button { background: linear-gradient(90deg,#00ffe1,#8a2be2); color: var(--button-text); border-radius:10px; padding:8px 14px; }
      .stImage>div>img { box-shadow: 0 10px 40px rgba(0,0,0,0.6); border-radius:6px; border:1px solid rgba(255,255,255,0.03); }
      .muted { color: #9aa8b2; }
    }

    @media (prefers-color-scheme: light) {
      :root {
        --bg-main: #ffffff;
        --text-main: #0b2540;
        --accent: #0057b7;
        --button-text: #ffffff;
      }
      [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(135deg, #ffffff 0%, #f6faff 60%);
        color: var(--text-main);
        min-height: 100vh;
      }
      /* Keep sidebar default/transparent so it doesn't use our gradient color */
      [data-testid="stSidebar"] {
        background: unset !important;
        color: inherit !important;
      }
      h1,h2,h3 { color: var(--accent); text-shadow: none; }
      .neon-box { background: rgba(0,87,183,0.03); padding:12px; border-radius:12px; border:1px solid rgba(0,87,183,0.06); }
      .stButton>button { background: linear-gradient(90deg,#0077cc,#6a3fb5); color: var(--button-text); border-radius:10px; padding:8px 14px; }
      .stImage>div>img { box-shadow: 0 6px 18px rgba(10,20,40,0.08); border-radius:6px; border:1px solid rgba(10,20,40,0.03); }
      .muted { color: #39536a; }
    }

    /* Force classes to override system preference (used when user selects Dark/Light manually)
       Note: we purposely DO NOT force the sidebar background here as well. */
    body.force-dark [data-testid="stAppViewContainer"] > .main {
      background: linear-gradient(135deg, #030612 0%, #00121a 60%) !important;
      color: #cfeef4 !important;
    }
    body.force-dark h1,h2,h3 { color:#00ffe1 !important; text-shadow: 0 0 8px rgba(0,255,225,0.08) !important; }

    body.force-light [data-testid="stAppViewContainer"] > .main {
      background: linear-gradient(135deg, #ffffff 0%, #f6faff 60%) !important;
      color: #0b2540 !important;
    }
    body.force-light h1,h2,h3 { color:#0057b7 !important; text-shadow: none !important; }

    /* small helpers */
    .neon-box { transition: background .2s, border .2s; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Inject CSS once
inject_futuristic_css()

# --- Sidebar: language + theme + page navigation ---
with st.sidebar:
    # Language selector
    lang_choice = st.selectbox("Language / Bahasa", list(LANG_OPTIONS.keys()),
                               index=0 if st.session_state.lang == "en" else 1)
    st.session_state.lang = LANG_OPTIONS[lang_choice]

    # Theme selector (Auto / Dark / Light)
    theme_choice = st.selectbox("Theme / Tema", ["Auto (system)", "Dark", "Light"],
                                index=0 if st.session_state.theme == "auto" else (1 if st.session_state.theme == "dark" else 2))
    if theme_choice == "Auto (system)":
        st.session_state.theme = "auto"
    elif theme_choice == "Dark":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

    st.markdown("---")
    page = st.radio("", ["Home / Introduction", "Image Processing Tools", "Team Members"])

# Add a small DOM node and JS to set body.force-dark / body.force-light when user chose manual theme.
st.markdown(
    f"""
    <div id="theme-data" data-theme="{st.session_state.theme}" style="display:none"></div>
    <script>
    (function() {{
      const el = document.getElementById('theme-data');
      if (!el) return;
      const theme = el.getAttribute('data-theme');
      document.body.classList.remove('force-dark','force-light');
      if (theme === 'dark') {{
        document.body.classList.add('force-dark');
      }} else if (theme === 'light') {{
        document.body.classList.add('force-light');
      }} // if 'auto' do nothing, let prefers-color-scheme apply
    }})();
    </script>
    """,
    unsafe_allow_html=True,
)

# --- Translations (centralized) ---
TEXT = {
    "en": {
        # Home
        "home_title": "Matrix & Convolution Explorer — Home",
        "home_lead": "This app demonstrates basic 2D matrix transformations (rotation, scaling, translation, shear, flip) and convolutional filters on images. Use the Image Processing Tools page to try interactive examples with your own images.",
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
        "conv_bullets": "Convolution applies a small kernel matrix over local image windows. Common kernels: Blur, Gaussian, Edge (Sobel/Laplacian), Sharpen.",
        "visual_examples": "Visual examples",
        "original": "Original (grid)",
        "rotated": "Rotated 30°",
        "edges": "Edges (approx)",
        "tip_home": "Tip: go to 'Image Processing Tools' to upload your images and try these operations interactively.",
        # Tools
        "tools_title": "Image Processing Tools",
        "tools_lead": "Upload an image or use the demo. Choose transformation or filter in the sidebar. Preview Original vs Transformed.",
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
        "original_label": "Original",
        "transformed_label": "Transformed",
        "flip_mode": "Mode",
        "filter_selection": "Filter selection",
        "custom_kernel_help": "Enter kernel as rows separated by ';' and values by commas. Example: 0,-1,0; -1,5,-1; 0,-1,0",
        "normalize": "Normalize kernel (sum -> 1) if possible",
        "tip_tools": "Tip: Use medium-size images (<= 1024 px) for best responsiveness.",
        # Team
        "team_title": "Team Members",
        "team_lead": "This page shows team biodata and photos. The app searches for photos in the 'images' folder. If a photo is not found, an initials avatar will be shown.",
        "sid": "SID",
        "origin": "Origin",
        "distribution": "Task distribution",
        "contrib_short": "Contributed to survey, cleaning, analysis, visualization, and building the Streamlit dashboard."
    },
    "id": {
        "home_title": "Matrix & Convolution Explorer — Beranda",
        "home_lead": "Aplikasi ini menunjukkan transformasi matriks 2D dasar (rotasi, skala, translasi, shear, flip) dan filter konvolusi pada citra. Gunakan halaman Image Processing Tools untuk mencoba contoh interaktif dengan citra Anda sendiri.",
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
        "conv_bullets": "Konvolusi menerapkan kernel (matriks kecil) pada jendela lokal citra. Kernel umum: Blur, Gaussian, Edge (Sobel/Laplacian), Sharpen.",
        "visual_examples": "Contoh visual",
        "original": "Asli (grid)",
        "rotated": "Diputar 30°",
        "edges": "Tepi (aproks.)",
        "tip_home": "Tip: buka 'Image Processing Tools' untuk mengunggah citra dan mencoba operasi ini secara interaktif.",
        # Tools
        "tools_title": "Alat Pengolahan Citra",
        "tools_lead": "Unggah gambar atau gunakan demo. Pilih transformasi atau filter di sidebar. Pratinjau Asli vs Hasil.",
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
        "original_label": "Asli",
        "transformed_label": "Hasil",
        "flip_mode": "Mode",
        "filter_selection": "Pemilihan filter",
        "custom_kernel_help": "Masukkan kernel sebagai baris dipisah ';' dan nilai dipisah koma. Contoh: 0,-1,0; -1,5,-1; 0,-1,0",
        "normalize": "Normalisasi kernel (jumlah -> 1) jika memungkinkan",
        "tip_tools": "Tip: Gunakan gambar ukuran sedang (<= 1024 px) untuk respons terbaik.",
        # Team
        "team_title": "Anggota Tim",
        "team_lead": "Halaman ini menampilkan biodata tim dan foto. Aplikasi mencari foto di folder 'images'. Jika foto tidak ditemukan, avatar inisial akan ditampilkan.",
        "sid": "SID",
        "origin": "Asal daerah",
        "distribution": "Distribusi tugas",
        "contrib_short": "Berkontribusi dalam survei, pembersihan data, analisis, visualisasi, dan pembuatan dashboard Streamlit."
    }
}

t = TEXT[st.session_state.lang]

# --- Shared helper functions (PIL + numpy, no cv2) ---
def generate_grid_image_pil(size=512, grid_steps=8, dark=False):
    bg = (10, 18, 30) if dark else (255, 255, 255)
    line = (30, 40, 60) if dark else (200, 200, 200)
    arrow = (0, 255, 225) if dark else (0, 0, 200)
    center_dot = (0, 150, 0) if dark else (0, 90, 0)
    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)
    step = max(4, size // grid_steps)
    for i in range(0, size, step):
        draw.line([(i, 0), (i, size)], fill=line, width=1)
        draw.line([(0, i), (size, i)], fill=line, width=1)
    draw.line([(size//4, size//4), (3*size//4, size//4)], fill=arrow, width=6)
    arrow_head = [(3*size//4, size//4), (3*size//4 - 20, size//4 - 15), (3*size//4 - 20, size//4 + 15)]
    draw.polygon(arrow_head, fill=(138, 43, 226) if dark else (138, 43, 226))
    r = 6
    cx, cy = size//2, size//2
    draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=center_dot)
    return img

def pil_rotate(img, angle, bg=(255,255,255)):
    return img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=bg)

def pil_edge_approx(img):
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    return edges.convert("RGB")

def pil_to_array(img):
    return np.array(img)

def array_to_pil(arr):
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8))

# Convolution helper using numpy
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
        "gaussian_5": np.array([[1,4,6,4,1],
                                 [4,16,24,16,4],
                                 [6,24,36,24,6],
                                 [4,16,24,16,4],
                                 [1,4,6,4,1]], dtype=np.float32),
        "sharpen": np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32),
        "sobel_x": np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32),
        "sobel_y": np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32),
        "laplacian": np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype=np.float32),
    }

# --- Team data (central) ---
TEAM = [
    {
        "short": "tris",
        "full_name": "Moh. Trisbintang A. Menu",
        "distribution": "Survei, bersihkan data, dashboard Streamlit (menu & navigasi)",
        "sid": "004202400102",
        "origin": "Gorontalo",
        "photo_file": "tris.jpg",
    },
    {
        "short": "fia",
        "full_name": "Dwi Anfia Putri Wulandari",
        "distribution": "Analisis dasar (histogram, boxplot), coding grafik Python, Streamlit bagian grafik",
        "sid": "004202400034",
        "origin": "Bogor",
        "photo_file": "fia.jpg",
    },
    {
        "short": "gina",
        "full_name": "Gina Sonia",
        "distribution": "Fokus laporan & bantu olah data",
        "sid": "004202400076",
        "origin": "Cikampek",
        "photo_file": "gina.jpg",
    },
    {
        "short": "fasya",
        "full_name": "Ananda Fasya Wiratama Putri",
        "distribution": "Analisis hubungan variabel, penjelasan pengaruh medsos ke mental, Streamlit bagian analisis",
        "sid": "004202400107",
        "origin": "Depok",
        "photo_file": "fasya.jpg",
    },
]

PHOTO_DIRS = ["images"]

def generate_avatar(name, size=270, bgcolor=(70,130,180)):
    initials = "".join([part[0].upper() for part in name.split()[:2]])
    img = Image.new("RGB", (size, size), bgcolor)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size // 3)
    except Exception:
        font = ImageFont.load_default()
    w, h = draw.textsize(initials, font=font)
    draw.text(((size - w) / 2, (size - h) / 2), initials, fill="white", font=font)
    return img

def find_photo_path(member, dirs):
    candidates = []
    if member.get("photo_file"):
        candidates.append(member["photo_file"])
    name_parts = [member["short"]] + member["full_name"].lower().split()
    for part in name_parts:
        candidates.append(f"{part}.jpg")
        candidates.append(f"{part}.jpeg")
        candidates.append(f"{part}.png")
    for d in dirs:
        p = Path(d)
        if not p.exists() or not p.is_dir():
            continue
        for cand in candidates:
            fpath = p / cand
            if fpath.exists():
                return str(fpath)
        for f in p.iterdir():
            if f.is_file() and member["short"].lower() in f.name.lower() and f.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                return str(f)
    return None

# --- Page render functions ---
def render_home():
    tt = TEXT[st.session_state.lang]
    st.markdown(f"<h1>{tt['home_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='neon-box'>{tt['home_lead']}</div>", unsafe_allow_html=True)

    st.header(tt["matrix_header"])
    st.subheader(tt["affine_title"])
    for b in tt["affine_bullets"]:
        st.markdown(f"- {b}")
    st.subheader(tt["conv_title"])
    st.markdown(tt["conv_bullets"])

    dark = (st.session_state.theme == "dark")
    demo = generate_grid_image_pil(512, dark=dark)
    bg_color = (10,18,30) if dark else (255,255,255)
    rotated = pil_rotate(demo, 30, bg=bg_color)
    edges = pil_edge_approx(demo)
    st.header(tt["visual_examples"])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(tt["original"])
        st.image(demo, use_column_width=True)
    with col2:
        st.subheader(tt["rotated"])
        st.image(rotated, use_column_width=True)
    with col3:
        st.subheader(tt["edges"])
        st.image(edges, use_column_width=True)
    st.markdown("---")
    st.info(tt["tip_home"])

def render_tools():
    tt = TEXT[st.session_state.lang]
    st.markdown(f"<h1>{tt['tools_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='neon-box'>{tt['tools_lead']}</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader(tt["upload"], type=["jpg","jpeg","png"])
    dark = (st.session_state.theme == "dark")
    bg_color = (10,18,30) if dark else (255,255,255)

    if uploaded:
        pil = Image.open(uploaded).convert("RGB")
        img_arr = pil_to_array(pil)
    else:
        demo = generate_grid_image_pil(512, dark=dark)
        img_arr = pil_to_array(demo)

    st.sidebar.header(tt["tools"])
    tool = st.sidebar.radio("", [tt["affine"], tt["flip"], tt["conv"]])

    if tool == tt["affine"]:
        st.sidebar.subheader(tt["affine"])
        angle = st.sidebar.slider(tt["rotation"], -180, 180, 0)
        scale = st.sidebar.slider(tt["scale"], 0.1, 3.0, 1.0, 0.1)
        tx = st.sidebar.slider(tt["translate_x"], -300, 300, 0)
        ty = st.sidebar.slider(tt["translate_y"], -300, 300, 0)
        shear_x = st.sidebar.slider(tt["shear_x"], -1.0, 1.0, 0.0, 0.01)
        shear_y = st.sidebar.slider(tt["shear_y"], -1.0, 1.0, 0.0, 0.01)

        # apply transforms (order: scale -> rotate -> shear -> translate)
        transformed = img_arr.copy()
        # scale
        h, w = transformed.shape[:2]
        new_w = max(1, int(w * scale)); new_h = max(1, int(h * scale))
        transformed = np.array(Image.fromarray(transformed).resize((new_w, new_h), resample=Image.BICUBIC))
        canvas = Image.new("RGB", (w, h), bg_color)
        canvas.paste(Image.fromarray(transformed), ((w - new_w)//2, (h - new_h)//2))
        transformed = pil_to_array(canvas)
        # rotate
        transformed = pil_to_array(Image.fromarray(transformed).rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=bg_color))
        # shear
        transformed = pil_to_array(Image.fromarray(transformed).transform((w, h), Image.AFFINE, (1.0, shear_x, 0.0, shear_y, 1.0, 0.0), resample=Image.BICUBIC, fillcolor=bg_color))
        # translate
        transformed = pil_to_array(Image.fromarray(transformed).transform((w, h), Image.AFFINE, (1,0,tx,0,1,ty), resample=Image.BICUBIC, fillcolor=bg_color))

        col_o, col_t = st.columns(2)
        with col_o:
            st.subheader(tt["original_label"])
            st.image(array_to_pil(img_arr), use_column_width=True)
        with col_t:
            st.subheader(tt["transformed_label"])
            st.image(array_to_pil(transformed), use_column_width=True)

    elif tool == tt["flip"]:
        st.sidebar.subheader(tt["flip"])
        flip_mode = st.sidebar.selectbox(tt["flip_mode"], ["Horizontal", "Vertical", "Both"])
        pil_img = Image.fromarray(img_arr)
        if flip_mode == "Horizontal":
            transformed = pil_to_array(pil_img.transpose(Image.FLIP_LEFT_RIGHT))
        elif flip_mode == "Vertical":
            transformed = pil_to_array(pil_img.transpose(Image.FLIP_TOP_BOTTOM))
        else:
            transformed = pil_to_array(pil_img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))
        col_o, col_t = st.columns(2)
        with col_o:
            st.subheader(tt["original_label"])
            st.image(array_to_pil(img_arr), use_column_width=True)
        with col_t:
            st.subheader(f"{tt['transformed_label']}: {flip_mode}")
            st.image(array_to_pil(transformed), use_column_width=True)

    else:
        st.sidebar.subheader(tt["filter_selection"])
        kernels = predefined_kernels()
        choices = list(kernels.keys()) + ["Custom"]
        sel = st.sidebar.selectbox("", choices)
        if sel == "Custom":
            st.sidebar.markdown(tt["custom_kernel_help"])
            custom = st.sidebar.text_area("Custom kernel", "0,-1,0; -1,5,-1; 0,-1,0")
            try:
                rows = [r.strip() for r in custom.split(";") if r.strip()!=""]
                kernel = np.array([[float(x) for x in row.split(",")] for row in rows], dtype=np.float32)
            except Exception:
                st.sidebar.error("Invalid kernel format.")
                kernel = kernels["sharpen"]
        else:
            kernel = kernels[sel]

        normalize = st.sidebar.checkbox(tt["normalize"], value=True)
        transformed = apply_convolution_array(img_arr, kernel, normalize=normalize)

        col_o, col_t = st.columns(2)
        with col_o:
            st.subheader(tt["original_label"])
            st.image(array_to_pil(img_arr), use_column_width=True)
        with col_t:
            st.subheader(f"{tt['transformed_label']}: {sel}")
            st.image(array_to_pil(transformed), use_column_width=True)

    st.markdown("---")
    st.caption(tt["tip_tools"])

def render_team():
    tt = TEXT[st.session_state.lang]
    st.markdown(f"<h1>{tt['team_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='neon-box'>{tt['team_lead']}</div>", unsafe_allow_html=True)

    for member in TEAM:
        cols = st.columns([1, 3])
        with cols[0]:
            photo_path = find_photo_path(member, PHOTO_DIRS)
            if photo_path:
                try:
                    img = Image.open(photo_path).convert("RGB")
                    st.image(img, width=270)
                except Exception:
                    st.warning(f"File {photo_path} found but cannot be opened. Showing avatar.")
                    st.image(generate_avatar(member["full_name"]), width=270)
            else:
                st.image(generate_avatar(member["full_name"]), width=270)
        with cols[1]:
            st.markdown(f"### {member['full_name']}")
            st.markdown(f"- **{tt['sid']}:** {member['sid']}")
            st.markdown(f"- **{tt['origin']}:** {member['origin']}")
            st.markdown(f"- **{tt['distribution']}:** {member['distribution']}")
            st.markdown(tt["contrib_short"])
        st.markdown("---")

# --- Run selected page ---
if page == "Home / Introduction":
    render_home()
elif page == "Image Processing Tools":
    render_tools()
else:
    render_team()

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import io
from image_processing import (
    rotate_image,
    scale_image,
    translate_image,
    shear_image,
    flip_image,
    apply_convolution,
    predefined_kernels,
)

st.set_page_config(page_title="Matrix & Convolution Explorer", layout="wide")

# Navigation
PAGES = ["Home / Introduction", "Image Processing Tools", "Team Members"]
page = st.sidebar.radio("Navigate pages", PAGES)

# Utilities
def load_image(uploaded_file):
    if uploaded_file is None:
        return None
    image = Image.open(uploaded_file).convert("RGB")
    return np.array(image)

def pil_from_array(arr):
    return Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))

def generate_grid_image(size=512, grid_steps=8):
    # generate a simple grid image for demonstrations
    img = np.ones((size, size, 3), dtype=np.uint8) * 255
    step = size // grid_steps
    for i in range(0, size, step):
        cv2.line(img, (i, 0), (i, size), (200, 200, 200), 1)
        cv2.line(img, (0, i), (size, i), (200, 200, 200), 1)
    # draw an arrow to visualize rotation/transform
    cv2.arrowedLine(img, (size//4, size//4), (3*size//4, size//4), (0, 0, 255), 4, tipLength=0.2)
    cv2.circle(img, (size//2, size//2), 6, (0, 128, 0), -1)
    return img

def generate_avatar(name, size=256, bgcolor=(100, 150, 200)):
    # Simple initials avatar using PIL
    initials = "".join([part[0].upper() for part in name.split()][:2])
    img = Image.new("RGB", (size, size), bgcolor)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size // 3)
    except:
        font = ImageFont.load_default()
    w, h = draw.textsize(initials, font=font)
    draw.text(((size - w) / 2, (size - h) / 2), initials, fill="white", font=font)
    return img

# --- Page: Home / Introduction ---
if page == "Home / Introduction":
    st.title("Matrix & Convolution Explorer")
    st.markdown(
        "This app demonstrates basic 2D matrix transformations (rotation, scaling, translation, shear, flip) "
        "and convolutional filters on images. Use the Image Processing Tools page to upload an image and try them interactively."
    )

    st.header("Quick Concepts")
    st.subheader("Matrix Transformations (Affine)")
    st.markdown(
        "- Rotation: rotates coordinates around a center. Matrix form (2x2 part) rotates points.\n"
        "- Scaling: stretches or shrinks coordinates.\n"
        "- Translation: moves coordinates by an offset (added vector).\n"
        "- Shear: slants the shape along X or Y.\n"
        "- Flip: mirror across axes (simple transforms)."
    )

    st.subheader("Convolution")
    st.markdown(
        "Convolution applies a kernel (small matrix) over the image. Common kernels:\n"
        "- Blur (averaging) smooths noise.\n"
        "- Gaussian blur gives smoother blur with less artifacting.\n"
        "- Edge detection (Sobel, Laplacian) highlights intensity changes.\n"
        "- Sharpening increases local contrast."
    )

    st.header("Visual examples")
    col1, col2, col3 = st.columns(3)
    demo = generate_grid_image(512)

    # Identity (original)
    with col1:
        st.subheader("Original / Identity")
        st.image(pil_from_array(demo), use_column_width=True)

    # Rotated
    rotated = rotate_image(demo, angle=30)
    with col2:
        st.subheader("Rotated by 30°")
        st.image(pil_from_array(rotated), use_column_width=True)

    # Edge detection
    edges = apply_convolution(demo, predefined_kernels()["edge_sobel_x"])
    # normalize to displayable range
    edges_disp = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX)
    edges_bgr = cv2.cvtColor(edges_disp.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    with col3:
        st.subheader("Sobel Edge (X)")
        st.image(pil_from_array(edges_bgr), use_column_width=True)

    st.markdown("Tip: go to 'Image Processing Tools' to try these operations on your own images.")

# --- Page: Image Processing Tools ---
elif page == "Image Processing Tools":
    st.title("Image Processing Tools")
    st.markdown("Upload an image and choose a transformation or filter. You will see Original vs Transformed preview.")

    # Upload
    uploaded = st.file_uploader("Upload an image (jpg/png). If none, a demo grid will be used.", type=["jpg", "jpeg", "png"])
    if uploaded:
        img = load_image(uploaded)
    else:
        img = generate_grid_image(512)

    # Sidebar navigation for operations
    st.sidebar.header("Operations")
    operation = st.sidebar.radio("Choose tool", ["Affine Transformations", "Flip", "Convolution / Filters"])

    if operation == "Affine Transformations":
        st.sidebar.subheader("Affine parameters")
        angle = st.sidebar.slider("Rotation angle (degrees)", -180, 180, 0)
        scale = st.sidebar.slider("Uniform scale", 0.1, 3.0, 1.0, 0.1)
        tx = st.sidebar.slider("Translate X (pixels)", -200, 200, 0)
        ty = st.sidebar.slider("Translate Y (pixels)", -200, 200, 0)
        shear_x = st.sidebar.slider("Shear X (factor)", -1.0, 1.0, 0.0, 0.01)
        shear_y = st.sidebar.slider("Shear Y (factor)", -1.0, 1.0, 0.0, 0.01)

        # Apply: combine transforms in a simple pipeline: scale -> rotate -> shear -> translate
        transformed = img.copy()
        transformed = scale_image(transformed, scale)
        transformed = rotate_image(transformed, angle)
        transformed = shear_image(transformed, shear_x, shear_y)
        transformed = translate_image(transformed, int(tx), int(ty))

        col_orig, col_trans = st.columns(2)
        with col_orig:
            st.subheader("Original")
            st.image(pil_from_array(img), use_column_width=True)
        with col_trans:
            st.subheader("Transformed")
            st.image(pil_from_array(transformed), use_column_width=True)

    elif operation == "Flip":
        st.sidebar.subheader("Flip options")
        flip_mode = st.sidebar.selectbox("Flip mode", ["Horizontal", "Vertical", "Both"])
        if flip_mode == "Horizontal":
            mode = 1
        elif flip_mode == "Vertical":
            mode = 0
        else:
            mode = -1
        transformed = flip_image(img, mode)
        col_orig, col_trans = st.columns(2)
        with col_orig:
            st.subheader("Original")
            st.image(pil_from_array(img), use_column_width=True)
        with col_trans:
            st.subheader(f"Flipped: {flip_mode}")
            st.image(pil_from_array(transformed), use_column_width=True)

    else:  # Convolution / Filters
        st.sidebar.subheader("Filter selection")
        kernels = predefined_kernels()
        kernel_names = list(kernels.keys()) + ["Custom"]
        choice = st.sidebar.selectbox("Kernel", kernel_names)
        if choice == "Custom":
            st.sidebar.markdown("Enter kernel values as comma-separated rows; e.g. '0,-1,0; -1,5,-1; 0,-1,0'")
            custom = st.sidebar.text_input("Custom kernel", "0,-1,0; -1,5,-1; 0,-1,0")
            try:
                # parse into 2D array
                rows = [r.strip() for r in custom.split(";") if r.strip() != ""]
                kernel = np.array([[float(x) for x in row.split(",")] for row in rows], dtype=np.float32)
            except Exception as e:
                st.sidebar.error("Couldn't parse kernel. Make sure to follow the example.")
                kernel = kernels["sharpen"]
        else:
            kernel = kernels[choice]

        normalize = st.sidebar.checkbox("Normalize kernel (sum -> 1) when possible", value=True)
        transformed = apply_convolution(img, kernel, normalize=normalize)

        col_orig, col_trans = st.columns(2)
        with col_orig:
            st.subheader("Original")
            st.image(pil_from_array(img), use_column_width=True)
        with col_trans:
            st.subheader(f"Filtered: {choice}")
            # If single-channel result, convert to BGR for display
            if len(transformed.shape) == 2:
                transformed = cv2.cvtColor(transformed.astype(np.uint8), cv2.COLOR_GRAY2BGR)
            st.image(pil_from_array(transformed), use_column_width=True)

    st.markdown("---")
    st.markdown("Hints:\n- Use small kernel sizes (3x3, 5x5) for fast results.\n- For large images, operations may be slower in the browser.")

# --- Page: Team Members ---
elif page == "Team Members":
    st.title("Team Members")
    st.markdown("Below are the members and their contributions. Replace images with real photos by placing them in the 'team_photos' folder "
                "or upload them using the uploader below.")

    # Default team list (editable by user)
    team = [
        {"name": "Alice Putri", "role": "Project lead, transforms & UI", "photo_file": None},
        {"name": "Budi Santoso", "role": "Convolution kernels & optimization", "photo_file": None},
        {"name": "Citra Dewi", "role": "Documentation & examples", "photo_file": None},
    ]

    uploaded_photos = {}
    st.subheader("Upload member photos (optional)")
    for i, member in enumerate(team):
        uploaded = st.file_uploader(f"Photo for {member['name']}", type=["jpg", "jpeg", "png"], key=f"photo_{i}")
        if uploaded:
            # store uploaded image bytes for display
            uploaded_photos[member["name"]] = Image.open(uploaded).convert("RGB")

    # Display team cards
    for member in team:
        cols = st.columns([1, 3])
        with cols[0]:
            if member["name"] in uploaded_photos:
                st.image(uploaded_photos[member["name"]], width=160)
            else:
                # generate avatar
                st.image(generate_avatar(member["name"]), width=160)
        with cols[1]:
            st.markdown(f"### {member['name']}")
            st.markdown(f"**Role / Contribution:** {member['role']}")
            st.markdown("Short bio: Enthusiastic about image processing, linear algebra, and building intuitive demos.")

    st.markdown("How the app works (short):")
    st.markdown(
        "1. You upload an image or use the demo image.\n"
        "2. Choose transformations or filters from the Image Processing Tools page.\n"
        "3. Parameters are applied using affine matrices (rotation, scale, shear, translation) and convolution kernels.\n"
        "4. Results are displayed side-by-side for visual comparison."
    )

    st.markdown("Feel free to edit the team list in the source code or replace avatars with real photos.")

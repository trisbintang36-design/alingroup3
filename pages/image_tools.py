import streamlit as st
from PIL import Image, ImageFilter, ImageOps

st.title("Image Processing Tools")

uploaded_file = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg","png","jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Original Image", use_column_width=True)

    st.sidebar.header("Transformasi & Filter")
    operation = st.sidebar.selectbox("Pilih operasi", ["Rotate", "Grayscale", "Blur", "Invert"])

    if operation == "Rotate":
        angle = st.sidebar.slider("Sudut rotasi", 0, 360, 90)
        transformed = img.rotate(angle)
    elif operation == "Grayscale":
        transformed = ImageOps.grayscale(img)
    elif operation == "Blur":
        radius = st.sidebar.slider("Radius blur", 1, 10, 2)
        transformed = img.filter(ImageFilter.GaussianBlur(radius))
    elif operation == "Invert":
        transformed = ImageOps.invert(img.convert("RGB"))

    st.image(transformed, caption=f"Transformed Image ({operation})", use_column_width=True)

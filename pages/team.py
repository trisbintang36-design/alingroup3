import streamlit as st
from PIL import Image

st.title("Team Members")

members = [
    {"name":"Alice", "photo":"images/alice.jpg", "role":"Project lead & matrix explanation"},
    {"name":"Bob", "photo":"images/bob.jpg", "role":"Image processing & coding"},
    {"name":"Charlie", "photo":"images/charlie.jpg", "role":"App deployment & documentation"},
]

for m in members:
    st.subheader(m["name"])
    img = Image.open(m["photo"])
    st.image(img, width=255)
    st.write(m["role"])

st.markdown("""
### How the App Works
1. Upload an image in the **Image Processing Tools** page.
2. Pilih transformasi atau filter dari sidebar.
3. Preview gambar asli vs hasil transformasi.
4. Pelajari transformasi matriks dan convolution di halaman **Home**.
""")

import streamlit as st
import numpy as np

st.title("Matrix & Image Processing App")
st.markdown("""
Aplikasi ini memungkinkan pengguna untuk:
- Memahami transformasi matriks
- Menerapkan filter dan convolution pada gambar
- Melihat hasil transformasi secara visual
""")

st.subheader("Contoh Transformasi Matriks")
matrix = np.array([[1, 2], [3, 4]])
st.write("Matriks Asli:")
st.write(matrix)
st.write("Transpose Matriks:")
st.write(matrix.T)

st.subheader("Contoh Convolution")
st.markdown("""
Kernel sederhana 3x3 untuk sharpen:
""")
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
st.write(kernel)
st.markdown("Convolution meningkatkan ketajaman gambar.")

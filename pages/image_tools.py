import streamlit as st
from PIL import Image
import numpy as np
import cv2

# Sidebar language (sama seperti home)
language = st.sidebar.selectbox(
    "Pilih Bahasa / Select Language / 选择语言",
    ("Indonesia", "English", "中文")
)

menu_items = {
    "Indonesia": ["Home", "Image Tools", "Team"],
    "English": ["Home", "Image Tools", "Team"],
    "中文": ["主页", "图像工具", "团队"]
}

selected_menu = st.sidebar.radio(
    "Menu" if language=="English" else "菜单" if language=="中文" else "Menu",
    menu_items[language]
)

if selected_menu == menu_items[language][1]:
    st.title("Image Tools" if language=="English" else
             "图像工具" if language=="中文" else
             "Image Tools")

    uploaded_file = st.file_uploader("Upload Gambar / Upload Image / 上传图片", type=['png','jpg','jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original", use_column_width=True)
        
        st.subheader("Transformasi Matriks / Matrix Transformation / 矩阵变换")
        rotate_angle = st.slider("Rotate (degree)" if language=="English" else
                                 "旋转角度" if language=="中文" else
                                 "Putar (derajat)", -180, 180, 0)
        if st.button("Apply Transformation / 应用变换 / Terapkan"):
            img_cv = np.array(image)
            (h, w) = img_cv.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
            rotated = cv2.warpAffine(img_cv, M, (w, h))
            st.image(rotated, caption="Transformed", use_column_width=True)

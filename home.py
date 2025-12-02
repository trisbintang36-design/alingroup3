import streamlit as st

# ========================
# Theme Modern
# ========================
st.set_page_config(
    page_title="Matrix & Image Processing App",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# Sidebar Bahasa
# ========================
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

# ========================
# Home Page
# ========================
if selected_menu == menu_items[language][0]:
    st.title("Matrix & Image Processing App" if language=="English" else
             "矩阵与图像处理应用" if language=="中文" else
             "Aplikasi Matrix & Image Processing")

    st.markdown("""
    **Fungsi Aplikasi:**  
    - Memahami transformasi matriks
    - Menerapkan filter & convolution pada gambar
    - Melihat hasil transformasi secara visual
    """ if language=="Indonesia" else
    """
    **App Functions:**  
    - Understand matrix transformations
    - Apply filters & convolution on images
    - Visualize results
    """ if language=="English" else
    """
    **应用功能:**  
    - 理解矩阵变换
    - 对图像应用滤波器和卷积
    - 可视化结果
    """
    )

    st.subheader("Contoh Transformasi Matriks / Matrix Transformation / 矩阵变换")
    st.write("Matriks Asli / Original / 原始矩阵")
    st.write([[1,2],[3,4]])
    st.write("Transpose / 转置 / Transpose")
    st.write([[1,3],[2,4]])

    st.subheader("Contoh Convolution / Convolution Example / 卷积示例")
    st.write("Kernel 3x3 untuk sharpen / 3x3 kernel to sharpen / 3x3锐化卷积核")
    st.write([[0,-1,0],[-1,5,-1],[0,-1,0]])
    st.write("Convolution meningkatkan ketajaman gambar / Convolution sharpens image / 卷积提升图像锐度")

import streamlit as st
from PIL import Image
import pandas as pd

def show_home():
    st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1 class="main-title">Sephora - Arta Frumuseții și Inovației</h1>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .content-container {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .text-box {
            max-width: 600px;
            text-align: justify;
        }
        .image-box img {
            max-width: 100%;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown(
            """
            <div class="content-container">
                <div class="text-box">
                    <p><strong>Sephora</strong> reprezintă excelența în lumea frumuseții, combinând produse premium cu tehnologie avansată.</p>
                    <p>Fondată în 1969 în Franța, Sephora a revoluționat industria cosmeticelor, oferind o experiență unică de cumpărare
                    prin magazine interactive și o platformă digitală de top.</p>
                    <p>Astăzi, Sephora este un brand global, prezent în peste 35 de țări, redefinind frumusețea prin inovație și diversitate.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        img = Image.open("media/sephora.png")
        st.image(img, caption="Sephora - Beauty Redefined", use_container_width=True)

    st.write("""
        ## O poveste despre eleganță și rafinament ✨
        Sephora nu este doar un brand, ci o comunitate globală a pasionaților de frumusețe. Oferind o gamă variată de produse,
        de la makeup de lux la îngrijire revoluționară a pielii, Sephora continuă să seteze trendurile în industrie.
        """)

    st.markdown("""
            <div style="text-align: center;">
                <h3 style="color: #E91E63;">💄 Eleganță în mișcare</h3>
                <p style="font-size: 16px; color: #555;">Descoperă universul Sephora, unde frumusețea se îmbină cu inovația.</p>
                <div style="width: 100px;">
            """, unsafe_allow_html=True)

    st.video("https://www.youtube.com/watch?v=tsSSr3-e7kM")

    product_data = pd.read_csv("dataset/product.csv")

    unique_products = product_data["product_name"].drop_duplicates().tolist()

    st.markdown("## 🛍️ Produse disponibile la Sephora")

    col1, col2 = st.columns(2)

    with col1:
        for i in range(0, 10, 2):
            st.write(f"💖 {unique_products[i]}")

    with col2:
        for i in range(1, 10, 2):
            st.write(f"💖 {unique_products[i]}")

    st.markdown("""
                </div>
            </div>
            """, unsafe_allow_html=True)

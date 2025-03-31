import streamlit as st
from PIL import Image

st.set_page_config(page_title="Sephora Analysis", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF3E0;
    }
    .main-title {
        color: #E91E63;
        font-size: 36px;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        background: -webkit-linear-gradient(45deg, #FF69B4, #000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom:12px;
    }
   .video-container {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown(
        """
        <div style="
            text-align: center;
        ">
            <h3 style="color: #E91E63; margin-bottom: 20px;">Sephora Navigation</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    img = Image.open("media/sidebar.jpg")
    st.image(img, caption="Sephora - Beauty Redefined")

    st.markdown("---")

    option_1 = st.radio("📌 Alege o secțiune:", ["Home", "Dataset", "Procesarea datelor", "Explorarea și Înțelegerea Setului de Date", "Tratarea Outliers", "Analiză corelații", "Variabile Categoriale", "Standardizare si normalizare", "Predicție"], index=0)

section = option_1

if section == "Home":
    from dataset.pages.home import show_home
    show_home()

elif section == "Dataset":
    from dataset.pages.dataset import show_dataset
    show_dataset()

elif section == "Procesarea datelor":
    from dataset.pages.valori_lipsa import show_procesare
    show_procesare()

if section == "Tratarea Outliers":
    from dataset.pages.outliers import show_outliers
    show_outliers()

elif section == "Explorarea și Înțelegerea Setului de Date":
    from dataset.pages.explorare import show_explorare
    show_explorare()

elif section == "Analiză corelații":
    from dataset.pages.correlations import show_correlations
    show_correlations()

elif section == "Predicție":
    from dataset.pages.predict_rating import show_prediction
    show_prediction()

elif section == "Variabile Categoriale":
    from dataset.pages.categorical_analysis import show_categorical_analysis
    show_categorical_analysis()

elif section == "Standardizare si normalizare":
    from dataset.pages.standardizare_normalizare import show_standardize_normalize
    show_standardize_normalize()
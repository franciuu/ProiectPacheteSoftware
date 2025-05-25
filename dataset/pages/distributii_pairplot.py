import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def vizualizare_reviews(reviews):
    st.subheader("Distribuții Reviews")

    col1, col2 = st.columns([2, 3])
    with col1:
        fig, ax = plt.subplots()
        sns.histplot(reviews['rating'], bins=5, kde=False, ax=ax)
        ax.set_title("Distribuția rating-urilor")
        st.pyplot(fig)
    with col2:
        st.markdown("**Interpretare:** Majoritatea recenziilor au rating 4 sau 5, ceea ce indică satisfacție ridicată.")

    col1, col2 = st.columns([2, 3])
    with col1:
        fig, ax = plt.subplots()
        sns.countplot(x='is_recommended', data=reviews, palette='viridis', ax=ax)
        ax.set_title("Distribuția is_recommended")
        st.pyplot(fig)
    with col2:
        st.markdown("**Interpretare:** Proporția mare de 1 arată că utilizatorii recomandă majoritar produsele.")

    col1, col2 = st.columns([2, 3])
    with col1:
        fig, ax = plt.subplots()
        sns.histplot(reviews['total_feedback_count'], bins=20, ax=ax)
        ax.set_title("Distribuția total_feedback_count")
        st.pyplot(fig)
    with col2:
        st.markdown("**Interpretare:** Majoritatea recenziilor au puțin feedback, dar există și recenzii foarte populare.")

def vizualizare_products(products):
    st.subheader("Distribuții Produse")

    col1, col2 = st.columns([2, 3])
    with col1:
        top_brands = products['brand_name'].value_counts().nlargest(10)
        fig, ax = plt.subplots()
        sns.barplot(x=top_brands.index, y=top_brands.values, palette='viridis', ax=ax)
        ax.set_title("Top 10 branduri")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    with col2:
        st.markdown("**Interpretare:** Brandurile din top domină oferta și pot influența statisticile globale.")

    col1, col2 = st.columns([2, 3])
    with col1:
        fig, ax = plt.subplots()
        sns.histplot(products['rating'], bins=10, ax=ax)
        ax.set_title("Distribuția rating-urilor produselor")
        st.pyplot(fig)
    with col2:
        st.markdown("**Interpretare:** Majoritatea produselor au rating peste 3, ceea ce sugerează o satisfacție generală bună.")

    col1, col2 = st.columns([2, 3])
    with col1:
        fig, ax = plt.subplots()
        sns.histplot(products['price_usd'], bins=20, ax=ax)
        ax.set_title("Distribuția prețurilor produselor")
        st.pyplot(fig)
    with col2:
        st.markdown("**Interpretare:** Distribuția prețurilor arată că portofoliul e axat pe produse accesibile.")

    for col, color_idx, text in zip(
        ['limited_edition', 'new', 'out_of_stock'],
        [3, 5, 8],
        [
            "Cele mai multe produse nu sunt in editie limitata.",
            "Cele mai multe produse nu sunt noi.",
            "Cele mai multe produse nu sunt epuizate din stoc."
        ]
    ):
        col1, col2 = st.columns([2, 3])
        with col1:
            fig, ax = plt.subplots()
            sns.countplot(x=col, data=products, palette='viridis', ax=ax)
            ax.set_title(f"Distribuția {col}")
            st.pyplot(fig)
        with col2:
            st.markdown(f"**Interpretare:** {text}")

def show_analiza():
    reviews_data = pd.read_csv("dataset/reviews_nan.csv")
    product_data = pd.read_csv("dataset/product_nan.csv")
    selected_reviews_cols = ['rating', 'is_recommended', 'total_feedback_count']
    selected_product_cols = ['brand_name', 'rating', 'price_usd', 'limited_edition', 'new', 'out_of_stock']
    reviews_selected = reviews_data[selected_reviews_cols]
    product_selected = product_data[selected_product_cols]

    st.markdown('<h1 class="main-title">Analiza explicită pe coloane selectate</h1>', unsafe_allow_html=True)
    vizualizare_reviews(reviews_selected)
    col1, col2 = st.columns([2, 3])
    with col1:
        numerical_cols = reviews_data.select_dtypes(include=[np.number]).columns
        pairplot_fig = sns.pairplot(reviews_data[numerical_cols], diag_kind='kde', corner=True, palette='viridis')
        pairplot_fig.fig.suptitle("Pairplot Reviews", y=1.02)
        st.pyplot(pairplot_fig)
    with col2:
        st.markdown("""
        ### Interpretare explicită pairplot Reviews (pe baza formei norilor de puncte)

        - **rating vs. is_recommended:**  
          Nu există o relație clară liniară sau o corelație vizibilă între cele două variabile. Punctele sunt grupate pe linii orizontale și verticale, ceea ce reflectă faptul că ambele variabile sunt discrete și concentrate pe câteva valori (`rating` ia valori între 1 și 5, iar `is_recommended` este binară, 0 sau 1). Din această cauză, nu se observă o asociere evidentă: există rating-uri mari și mici atât pentru recomandări, cât și pentru nerecomandări.

        - **helpfulness vs. total_feedback_count:**  
          Relația nu este liniară, dar se observă o ușoară tendință ca recenziile cu helpfulness apropiat de 1 să aibă mai des feedback total mai mare. Totuși, există și multe recenzii cu helpfulness mare și puțin feedback, deci legătura este slabă și dispersată. Forma norului este mai degrabă de tip "evantai" spre dreapta sus, fără o diagonală clară.

        - **total_pos_feedback_count vs. total_feedback_count:**  
          Aici există o relație clară, aproape liniară: pe măsură ce crește feedback-ul total, crește și feedback-ul pozitiv. Norul de puncte este aliniat de-a lungul diagonalei, ceea ce arată că majoritatea feedback-ului este pozitiv și că cele două variabile cresc împreună.

        - **price_usd cu celelalte variabile:**  
          Nu există niciun tipar sau corelație vizibilă între preț și celelalte variabile. Punctele sunt dispersate haotic, fără o direcție sau o formă clară, ceea ce arată că prețul nu influențează rating-ul, helpfulness sau feedback-ul.

        - **Distribuții univariate:**  
          - `rating` și `is_recommended` sunt puternic concentrate pe valorile maxime, cu puține recenzii negative sau nerecomandate.
          - `helpfulness` are două vârfuri: multe recenzii sunt considerate fie foarte utile (aproape de 1), fie deloc utile (aproape de 0).
          - Variabilele de feedback (`total_feedback_count`, `total_neg_feedback_count`, `total_pos_feedback_count`) sunt asimetrice, cu multe valori mici și câteva foarte mari (outlieri).
          - `price_usd` este și ea asimetrică, cu multe produse ieftine și câteva scumpe.

        **Concluzie explicită:**  
        Singura relație clară și aproape liniară este între feedback-ul total și cel pozitiv, ceea ce era de așteptat (feedback-ul pozitiv domină totalul). Restul relațiilor sunt slabe sau inexistente, cu norii de puncte dispersați, fără o direcție clară. Distribuțiile univariate arată un bias pozitiv (rating și recomandare maxime), iar helpfulness și feedback-ul au distribuții tipice pentru date de recenzii online, cu multe valori mici și câteva extreme.
        """)

    vizualizare_products(product_selected)
    col1, col2 = st.columns([2, 3])
    with col1:
        numeric_cols = product_data.select_dtypes(include=[np.number]).columns
        pairplot_fig = sns.pairplot(product_data[numeric_cols], diag_kind='kde', corner=True, palette='viridis')
        pairplot_fig.fig.suptitle("Pairplot Produse", y=1.02)
        st.pyplot(pairplot_fig)
    with col2:
        st.markdown("""
    ### Interpretare explicită pairplot Produse

    - **loves_count vs. rating:**  
      Nu se observă o relație clară între numărul de "loves" și rating. Norul de puncte este foarte dispersat, fără o direcție sau o formă evidentă. Aceasta sugerează că popularitatea unui produs (măsurată prin loves_count) nu este neapărat asociată cu rating-ul mediu acordat de utilizatori.

    - **loves_count vs. price_usd:**  
      Relația este tot dispersată, fără o tendință clară. Produsele cu prețuri mici și mari pot avea atât loves_count mic, cât și mare, ceea ce arată că prețul nu este un factor determinant pentru popularitate.

    - **rating vs. price_usd:**  
      Punctele sunt distribuite fără o direcție clară, ceea ce indică lipsa unei corelații între preț și rating. Produsele scumpe nu primesc neapărat rating-uri mai mari sau mai mici decât cele ieftine.

    - **limited_edition, new, online_only, out_of_stock, sephora_exclusive:**  
      Aceste variabile sunt binare (0/1), iar norii de puncte față de variabilele numerice nu arată relații evidente. Punctele sunt grupate pe linii orizontale, ceea ce e normal pentru variabilele categorice/boolene. Nu se observă o asociere clară între atributele de tip "ediție limitată", "nou", "doar online", "epuizat" sau "exclusiv Sephora" și celelalte variabile numerice.

    - **child_count:**  
      Se observă o ușoară tendință ca produsele cu mai multe variante (child_count mai mare) să aibă loves_count mai mare, dar relația nu este puternică. Forma norului este tot destul de dispersată, fără o diagonală clară.

    - **Distribuții univariate:**  
      - `loves_count` este foarte asimetrică, cu multe produse care au puține "loves" și câteva cu valori foarte mari (outlieri).
      - `rating` are o distribuție strânsă, majoritatea produselor având rating între 3 și 5.
      - `price_usd` este asimetrică, cu multe produse ieftine și câteva foarte scumpe.
      - Variabilele binare (limited_edition, new etc.) sunt concentrate pe 0, adică majoritatea produselor nu sunt ediție limitată, noi, doar online, epuizate sau exclusive.

    **Concluzie explicită:**  
    Nu există corelații puternice sau relații liniare între variabilele numerice principale. Majoritatea norilor de puncte sunt dispersați, fără o direcție clară, ceea ce arată că popularitatea, prețul și rating-ul sunt relativ independente în acest set de date. Singura tendință ușoară este că produsele cu mai multe variante tind să fie ceva mai populare (mai multe "loves"), dar și aici legătura este slabă. Distribuțiile univariate arată prezența unor outlieri și o concentrare a produselor pe valorile mici pentru loves_count și preț.
    """)


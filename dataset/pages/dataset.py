import streamlit as st
import pandas as pd

def show_dataset():
    product_data = pd.read_csv("dataset/product.csv")
    reviews_data = pd.read_csv("dataset/reviews.csv")

    st.markdown('<h1 class="main-title">Datasetul ales pentru compania Sephora</h1>', unsafe_allow_html=True)
    st.write("""
        **Sursa datelor:** Acest set de date a fost preluat de pe Kaggle. Datele originale se pot găsi aici:
        [Sephora Dataset pe Kaggle](https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews/data)

        **Ce surprind datele?**
        Datele surprind informații detaliate despre produsele Sephora, recenziile utilizatorilor și preferințele acestora.
       
        **Ce vom realiza?**
        Cu ajutorul acestor date, vom implementa următoarele tipuri de analize:
        - Vizualizarea caracteristicilor produselor și recenziilor
        - Detectarea tendințelor pe baza evaluărilor utilizatorilor
        - Explorarea oportunităților de extindere pe noi piețe
        - Prelucrări statistice și modele predictive folosind Python""")

    st.markdown("### 📊 Primele rânduri din fișierele dataset")

    st.subheader("🛍️ Produse Sephora")
    st.dataframe(product_data.head())

    st.subheader("📝 Recenzii Produse")
    st.dataframe(reviews_data.head())

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 Vizualizează variabilele despre Content Product Data"):
            st.write("""
                **Product Data Content:**
                - **product_id:** Identificator unic al produsului de pe site. Acesta nu are valoare predictivă dar prezinta legatura cu tabela reviews.
                - **product_name:** Numele complet al produsului. Nu avem intenția de a folosi NLP așa că va fi eliminat.
                - **brand_id:** Identificator unic al brandului produsului de pe site. Deși numeric, nu are sens matematic real. Il vom sterge deoarece pastram legatura prin numele brandului.
                - **brand_name:** Numele complet al brandului produsului. Îl vom păstra deoarece reprezinta o legatură cu tabela reviews.
                - **loves_count:** Numărul de utilizatori care au marcat produsul ca favorit
                - **rating:** Evaluarea medie a produsului pe baza recenziilor utilizatorilor
                - **variation_type:** Tipul de variație al produsului (ex. mărime, culoare)
                - **variation_value:** Valoarea specifică a variației produsului (ex. 100 ml, Golden Sand)
                - **variation_desc:** Descrierea variației produsului (ex. nuanță pentru ten deschis)
                - **ingredients:** Lista ingredientelor incluse în produs
                - **price_usd:** Prețul produsului în dolari americani
                - **limited_edition:** Indică dacă produsul este ediție limitată (1-adevărat, 0-fals)
                - **new:** Indică dacă produsul este nou (1-adevărat, 0-fals)
                - **online_only:** Indică dacă produsul este vândut exclusiv online (1-adevărat, 0-fals)
                - **out_of_stock:** Indică dacă produsul este momentan indisponibil (1-adevărat, 0-fals)
                - **sephora_exclusive:** Indică dacă produsul este exclusiv Sephora (1-adevărat, 0-fals)
                - **highlights:** O listă de caracteristici ce evidențiază produsul (ex. [‘Vegan’, ‘Mat Finish’])
                - **primary_category:** Prima categorie din structura de navigare
                - **secondary_category:** A doua categorie din structura de navigare
                - **tertiary_category:** A treia categorie din structura de navigare
                - **child_count:** Numărul de variații disponibile pentru produs
                - **child_max_price:** Cel mai mare preț dintre variațiile produsului
                - **child_min_price:** Cel mai mic preț dintre variațiile produsului
                """)

    with col2:
        if st.button("💬 Vizualizează variabilele despre Reviews Data Content"):
            st.write("""
                **Reviews Data Content:**
                - **author_id:** Identificator unic al autorului recenziei pe site. Acesta nu are valoare predictivă așa că va fi eliminat.
                - **rating:** Scorul oferit de autor pentru produs (de la 1 la 5)
                - **is_recommended:** Indică dacă autorul recomandă produsul (1-adevărat, 0-fals)
                - **helpfulness:** Raportul dintre totalul voturilor pozitive și totalul voturilor acordate recenziei
                - **total_feedback_count:** Numărul total de evaluări (pozitive și negative) pentru recenzie. Îl vom elimina deoarece reprezintă suma celor pozitive și negative.
                - **total_neg_feedback_count:** Numărul utilizatorilor care au oferit un vot negativ recenziei
                - **total_pos_feedback_count:** Numărul utilizatorilor care au oferit un vot pozitiv recenziei
                - **submission_time:** Data postării recenziei pe site (format: 'yyyy-mm-dd')
                - **review_text:** Textul principal al recenziei scris de autor. Nu avem intenția de a folosi NLP așa că va fi eliminat.
                - **review_title:** Titlul recenziei scris de autor. Nu avem intenția de a folosi NLP așa că va fi eliminat.
                - **skin_tone:** Tonul pielii autorului (ex. deschis, bronzat, etc.)
                - **eye_color:** Culoarea ochilor autorului (ex. căprui, verzi, etc.)
                - **skin_type:** Tipul de piele al autorului (ex. mixt, gras, etc.)
                - **hair_color:** Culoarea părului autorului (ex. castaniu, roșcat, etc.)
                - **product_id:** Identificator unic al produsului de pe site
                - **product_name:** Numele produsului. Va fi eliminat.
                - **brand_name:** Numele complet al brandului produsului. Îl vom păstra deoarece reprezinta o legatură cu tabela products.
                - **price_usd:** Pretul produsului
                """)
    product_data_copy = product_data.copy()
    reviews_data_copy = reviews_data.copy()
    product_data_copy = product_data_copy.drop(columns=["product_name", "brand_id"])
    reviews_data_copy = reviews_data_copy.drop(columns=["author_id", "review_text", "review_title", "product_name", "submission_time"])

    product_data_copy.to_csv("dataset/product_drop.csv", index=False)
    reviews_data_copy.to_csv("dataset/reviews_drop.csv", index=False)
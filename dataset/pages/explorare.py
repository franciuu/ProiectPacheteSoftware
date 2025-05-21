import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_explorare():
    @st.cache_data
    def load_data():
        df_products = pd.read_csv("dataset/product.csv")
        df_reviews = pd.read_csv("dataset/reviews.csv")
        return df_products, df_reviews

    df_products, df_reviews = load_data()

    st.markdown("""
        <style>
        .main-title {font-size: 2.8rem !important; color: #4F8BF9; font-weight: bold;}
        .stSelectbox label {font-weight: 600;}
        .stCodeBlock {background: #f5f7fa;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">Analiză vizuală și exploratorie pentru produse și recenzii</h1>',
                unsafe_allow_html=True)
    st.write(
        "Acest dashboard interactiv permite explorarea rapidă a datelor despre produse și recenzii. Selectează o analiză din listă pentru a vedea rezultatele.")

    exercitii = {
        "1️⃣ Afișează primele 5 rânduri din fiecare set de date": {
            "descriere": "Primele 5 rânduri din `product.csv` și `reviews.csv`.",
            "explicatie": "Această analiză te ajută să vezi structura și primele valori din fiecare set de date.",
            "cod": "df_products.head(), df_reviews.head()"
        },
        "2️⃣ Valorile unice din coloana brand_name (product.csv)": {
            "descriere": "Toate brandurile distincte din lista de produse.",
            "explicatie": "Poți vedea ce branduri există în portofoliul de produse.",
            "cod": "df_products['brand_name'].unique()"
        },
        "3️⃣ Prețul mediu al produselor (product.csv)": {
            "descriere": "Calculul prețului mediu pentru toate produsele.",
            "explicatie": "Prețul mediu oferă o idee despre poziționarea generală a produselor.",
            "cod": "df_products['price_usd'].mean()"
        },
        "4️⃣ Numărul de produse limited edition": {
            "descriere": "Numărul de produse marcate ca ediție limitată.",
            "explicatie": "Află câte produse speciale (ediție limitată) există în ofertă.",
            "cod": "df_products[df_products['limited_edition'] == 1].shape[0]"
        },
        "5️⃣ Produse din categoria Skincare (nume și preț)": {
            "descriere": "Lista produselor din categoria principală Skincare cu nume și preț.",
            "explicatie": "Filtrarea pe o categorie populară pentru a vedea oferta și prețurile.",
            "cod": "df_products[df_products['primary_category'] == 'Skincare'][['product_name', 'price_usd']]"
        },
        "6️⃣ Produsul cu cel mai mare preț": {
            "descriere": "Produsul cu prețul maxim.",
            "explicatie": "Identifici produsul premium din ofertă.",
            "cod": "df_products.loc[df_products['price_usd'].idxmax()][['product_name', 'price_usd']]"
        },
        "7️⃣ Prețul mediu pe categorie principală": {
            "descriere": "Prețul mediu al produselor pentru fiecare categorie principală.",
            "explicatie": "Compari categoriile după prețul mediu al produselor.",
            "cod": "df_products.groupby('primary_category')['price_usd'].mean()"
        },
        "8️⃣ Recenzii cu rating 5 pentru produsul P420652": {
            "descriere": "Toate recenziile cu rating maxim pentru produsul cu ID-ul P420652.",
            "explicatie": "Analizezi feedback-ul excelent pentru un anumit produs.",
            "cod": "df_reviews[(df_reviews['product_id'] == 'P420652') & (df_reviews['rating'] == 5)]"
        },
        "9️⃣ Scorul mediu de rating pentru fiecare brand": {
            "descriere": "Ratingul mediu pentru fiecare brand, pe baza recenziilor.",
            "explicatie": "Află ce branduri au cele mai bune recenzii din partea clienților.",
            "cod": "df_reviews.groupby('brand_name')['rating'].mean()"
        },
        "🔟 Top 3 produse cu cele mai multe recenzii pozitive": {
            "descriere": "Top 3 produse cu cele mai multe recenzii pozitive (total_pos_feedback_count).",
            "explicatie": "Identifici produsele cu cel mai mult feedback pozitiv.",
            "cod": "df_reviews.groupby('product_id')['total_pos_feedback_count'].sum().sort_values(ascending=False).head(3)"
        },
        "1️⃣1️⃣ Histograma distribuției prețurilor": {
            "descriere": "Histograma distribuției prețurilor produselor.",
            "explicatie": "Vizualizezi cum sunt distribuite prețurile produselor.",
            "cod": "plt.figure(figsize=(8,4)); plt.hist(df_products['price_usd'], bins=20, color='#4F8BF9', edgecolor='white'); plt.xlabel('Preț (USD)'); plt.ylabel('Frecvență'); plt.title('Distribuția prețurilor'); st.pyplot(plt.gcf())"
        },
        "1️⃣2️⃣ Grafic de bare: preț mediu pe brand (top 10)": {
            "descriere": "Grafic de bare cu prețul mediu pentru top 10 branduri cu cele mai multe produse.",
            "explicatie": "Compari vizual brandurile cu cele mai multe produse după prețul mediu.",
            "cod": """
top_brands = df_products['brand_name'].value_counts().head(10).index
avg_price = df_products[df_products['brand_name'].isin(top_brands)].groupby('brand_name')['price_usd'].mean().sort_values(ascending=False)
plt.figure(figsize=(10,4))
avg_price.plot(kind='bar', color='#F97B4F', edgecolor='black')
plt.ylabel('Preț mediu (USD)')
plt.title('Preț mediu pe brand (top 10)')
plt.xticks(rotation=30)
st.pyplot(plt.gcf())
"""
        },
        "1️⃣3️⃣ Mediana prețurilor pe fiecare categorie principală": {
            "descriere": "Calculează mediana prețurilor pentru fiecare categorie principală.",
            "explicatie": "Mediana este mai robustă la extreme decât media și arată prețul tipic din fiecare categorie.",
            "cod": "df_products.groupby('primary_category')['price_usd'].median()"
        },
        "1️⃣4️⃣ Numărul de recenzii pentru fiecare produs": {
            "descriere": "Afișează câte recenzii are fiecare produs.",
            "explicatie": "Poți vedea ce produse sunt cele mai populare sau cele mai discutate.",
            "cod": "df_reviews['product_id'].value_counts()"
        },
        "1️⃣5️⃣ Ratingul maxim și minim pentru fiecare brand": {
            "descriere": "Afișează ratingul maxim și minim primit de fiecare brand.",
            "explicatie": "Astfel vezi variația percepției clienților pentru fiecare brand.",
            "cod": "df_reviews.groupby('brand_name')['rating'].agg(['min', 'max'])"
        },
        "1️⃣6️⃣ Procentul de produse limited edition pe fiecare categorie": {
            "descriere": "Calculează procentul de produse limited edition pentru fiecare categorie principală.",
            "explicatie": "Află cât de exclusiviste sunt categoriile de produse.",
            "cod": """
limited_pct = df_products.groupby('primary_category')['limited_edition'].mean() * 100
limited_pct
"""
        }
    }

    selected = st.selectbox("🔍 Selectează o analiză", list(exercitii.keys()))
    st.markdown(f"#### {selected}")
    st.write(exercitii[selected]["descriere"])
    st.info(exercitii[selected]["explicatie"])
    st.code(exercitii[selected]["cod"], language="python")

    if st.button("🔎 Execută analiza"):
        if selected == "1️⃣ Afișează primele 5 rânduri din fiecare set de date":
            st.write("**product.csv:**")
            st.write(df_products.head())
            st.write("**reviews.csv:**")
            st.write(df_reviews.head())
        elif selected == "2️⃣ Valorile unice din coloana brand_name (product.csv)":
            st.write(df_products['brand_name'].unique())
        elif selected == "3️⃣ Prețul mediu al produselor (product.csv)":
            st.write(f"Prețul mediu: {df_products['price_usd'].mean():.2f} USD")
        elif selected == "4️⃣ Numărul de produse limited edition":
            st.write(f"Număr produse limited edition: {df_products[df_products['limited_edition'] == 1].shape[0]}")
        elif selected == "5️⃣ Produse din categoria Skincare (nume și preț)":
            st.dataframe(df_products[df_products['primary_category'] == 'Skincare'][['product_name', 'price_usd']])
        elif selected == "6️⃣ Produsul cu cel mai mare preț":
            max_row = df_products.loc[df_products['price_usd'].idxmax()]
            st.write(f"Produs: {max_row['product_name']}, Preț: {max_row['price_usd']:.2f} USD")
        elif selected == "7️⃣ Prețul mediu pe categorie principală":
            st.dataframe(df_products.groupby('primary_category')['price_usd'].mean().reset_index())
        elif selected == "8️⃣ Recenzii cu rating 5 pentru produsul P420652":
            st.dataframe(df_reviews[(df_reviews['product_id'] == 'P420652') & (df_reviews['rating'] == 5)])
        elif selected == "9️⃣ Scorul mediu de rating pentru fiecare brand":
            st.dataframe(df_reviews.groupby('brand_name')['rating'].mean().reset_index())
        elif selected == "🔟 Top 3 produse cu cele mai multe recenzii pozitive":
            st.dataframe(
                df_reviews.groupby('product_id')['total_pos_feedback_count'].sum().sort_values(ascending=False).head(
                    3).reset_index())
        elif selected == "️1️⃣1️⃣ Histograma distribuției prețurilor":
            plt.figure(figsize=(8, 4))
            plt.hist(df_products['price_usd'], bins=20, color='#4F8BF9', edgecolor='white')
            plt.xlabel('Preț (USD)')
            plt.ylabel('Frecvență')
            plt.title('Distribuția prețurilor')
            st.pyplot(plt.gcf())
            plt.clf()
        elif selected == "1️⃣2️⃣ Grafic de bare: preț mediu pe brand (top 10)":
            top_brands = df_products['brand_name'].value_counts().head(10).index
            avg_price = df_products[df_products['brand_name'].isin(top_brands)].groupby('brand_name')[
                'price_usd'].mean().sort_values(ascending=False)
            plt.figure(figsize=(10, 4))
            avg_price.plot(kind='bar', color='#F97B4F', edgecolor='black')
            plt.ylabel('Preț mediu (USD)')
            plt.title('Preț mediu pe brand (top 10)')
            plt.xticks(rotation=30)
            st.pyplot(plt.gcf())
            plt.clf()
        elif selected == "1️⃣3️⃣ Mediana prețurilor pe fiecare categorie principală":
            st.dataframe(df_products.groupby('primary_category')['price_usd'].median().reset_index())
        elif selected == "1️⃣4️⃣ Numărul de recenzii pentru fiecare produs":
            st.dataframe(df_reviews['product_id'].value_counts().reset_index().rename(columns={'index': 'product_id', 'product_id': 'nr_recenzii'}))
        elif selected == "1️⃣5️⃣ Ratingul maxim și minim pentru fiecare brand":
            st.dataframe(df_reviews.groupby('brand_name')['rating'].agg(['min', 'max']).reset_index())
        elif selected == "1️⃣6️⃣ Procentul de produse limited edition pe fiecare categorie":
            limited_pct = df_products.groupby('primary_category')['limited_edition'].mean() * 100
            st.dataframe(limited_pct.reset_index().rename(columns={'limited_edition': 'procent_limited_edition'}))

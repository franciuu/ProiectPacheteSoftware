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

    st.markdown('<h1 class="main-title">Analiza vizuala si exploratorie pentru produse si recenzii</h1>',
                unsafe_allow_html=True)
    st.write(
        "Acest dashboard interactiv permite explorarea rapida a datelor despre produse si recenzii. Selecteaza o analiza din lista pentru a vedea rezultatele.")

    exercitii = {
        "1️⃣ Afișează primele 5 rânduri din fiecare set de date": {
            "descriere": "Primele 5 rânduri din `product.csv` și `reviews.csv`.",
            "explicatie": "Vezi structura și primele valori din fiecare set de date.",
            "cod": """st.write("**product.csv:**")
st.write(df_products.head())
st.write("**reviews.csv:**")
st.write(df_reviews.head())"""
        },
        "2️⃣ Valorile unice din coloana brand_name (product.csv)": {
            "descriere": "Toate brandurile distincte din lista de produse.",
            "explicatie": "Ce branduri există în portofoliu.",
            "cod": """st.write(df_products['brand_name'].unique())"""
        },
        "3️⃣ Prețul mediu al produselor (product.csv)": {
            "descriere": "Calculul prețului mediu pentru toate produsele.",
            "explicatie": "Poziționarea generală a produselor.",
            "cod": """st.write(f"Prețul mediu: {df_products['price_usd'].mean():.2f} USD")"""
        },
        "4️⃣ Numărul de produse limited edition": {
            "descriere": "Numărul de produse marcate ca ediție limitată.",
            "explicatie": "Câte produse speciale există în ofertă.",
            "cod": """st.write(f"Număr produse limited edition: {df_products[df_products['limited_edition'] == 1].shape[0]}")"""
        },
        "5️⃣ Produse din categoria Skincare (nume și preț)": {
            "descriere": "Lista produselor din categoria Skincare cu nume și preț.",
            "explicatie": "Filtrare pe o categorie populară.",
            "cod": """st.dataframe(df_products[df_products['primary_category'] == 'Skincare'][['product_name', 'price_usd']])"""
        },
        "6️⃣ Produsul cu cel mai mare preț": {
            "descriere": "Produsul cu prețul maxim.",
            "explicatie": "Identifici produsul premium.",
            "cod": """max_row = df_products.loc[df_products['price_usd'].idxmax()]
st.write(f"Produs: {max_row['product_name']}, Preț: {max_row['price_usd']:.2f} USD")"""
        },
        "7️⃣ Prețul mediu pe categorie principală": {
            "descriere": "Prețul mediu al produselor pentru fiecare categorie.",
            "explicatie": "Compari categoriile după preț.",
            "cod": """st.dataframe(df_products.groupby('primary_category')['price_usd'].mean().reset_index())"""
        },
        "8️⃣ Recenzii cu rating 5 pentru produsul P420652": {
            "descriere": "Toate recenziile cu rating maxim pentru produsul P420652.",
            "explicatie": "Analizezi feedback-ul excelent.",
            "cod": """st.dataframe(df_reviews[(df_reviews['product_id'] == 'P420652') & (df_reviews['rating'] == 5)])"""
        },
        "9️⃣ Scorul mediu de rating pentru fiecare brand": {
            "descriere": "Ratingul mediu pentru fiecare brand.",
            "explicatie": "Ce branduri au cele mai bune recenzii.",
            "cod": """st.dataframe(df_reviews.groupby('brand_name')['rating'].mean().reset_index())"""
        },
        "🔟 Top 3 produse cu cele mai multe recenzii pozitive": {
            "descriere": "Top 3 produse cu cele mai multe recenzii pozitive.",
            "explicatie": "Produsele cu cel mai mult feedback pozitiv.",
            "cod": """st.dataframe(
    df_reviews.groupby('product_id')['total_pos_feedback_count'].sum().sort_values(ascending=False).head(3).reset_index())"""
        },
        "1️⃣1️⃣ Histograma distribuției prețurilor": {
            "descriere": "Histograma distribuției prețurilor produselor.",
            "explicatie": "Vizualizezi cum sunt distribuite prețurile.",
            "cod": """fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df_products['price_usd'].dropna(), bins=20, color='skyblue', edgecolor='black')
ax.set_xlabel('Preț (USD)')
ax.set_ylabel('Frecvență')
ax.set_title('Histograma distribuției prețurilor produselor')
ax.grid(axis='y', alpha=0.75)
st.pyplot(fig)
plt.clf()"""
        },
        "1️⃣2️⃣ Grafic de bare: preț mediu pe brand (top 10)": {
            "descriere": "Grafic de bare cu prețul mediu pentru top 10 branduri.",
            "explicatie": "Compari vizual brandurile după preț.",
            "cod": """top_brands = df_products['brand_name'].value_counts().head(10).index
avg_price = df_products[df_products['brand_name'].isin(top_brands)].groupby('brand_name')['price_usd'].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 4))
avg_price.plot(kind='bar', color='#F97B4F', edgecolor='black')
plt.ylabel('Preț mediu (USD)')
plt.title('Preț mediu pe brand (top 10)')
plt.xticks(rotation=30)
st.pyplot(plt.gcf())
plt.clf()"""
        },
        "1️⃣3️⃣ Mediana prețurilor pe fiecare categorie principală": {
            "descriere": "Mediana prețurilor pentru fiecare categorie.",
            "explicatie": "Mediana arată prețul tipic din fiecare categorie.",
            "cod": """st.dataframe(df_products.groupby('primary_category')['price_usd'].median().reset_index())"""
        },
        "1️⃣4️⃣ Numărul de recenzii pentru fiecare produs": {
            "descriere": "Câte recenzii are fiecare produs.",
            "explicatie": "Vezi ce produse sunt cele mai populare.",
            "cod": """st.dataframe(df_reviews['product_id'].value_counts().reset_index().rename(columns={'index': 'product_id', 'product_id': 'nr_recenzii'}))"""
        },
        "1️⃣5️⃣ Ratingul maxim și minim pentru fiecare brand": {
            "descriere": "Ratingul maxim și minim pentru fiecare brand.",
            "explicatie": "Variația percepției clienților pentru fiecare brand.",
            "cod": """st.dataframe(df_reviews.groupby('brand_name')['rating'].agg(['min', 'max']).reset_index())"""
        },
        "1️⃣6️⃣ Procentul de produse limited edition pe fiecare categorie": {
            "descriere": "Procentul de produse limited edition pe fiecare categorie.",
            "explicatie": "Cât de exclusiviste sunt categoriile.",
            "cod": """limited_pct = df_products.groupby('primary_category')['limited_edition'].mean() * 100
st.dataframe(limited_pct.reset_index().rename(columns={'limited_edition': 'procent_limited_edition'}))"""
        },
        "1️⃣7️⃣ Prelucrare statistică cu describe (product.csv)": {
            "descriere": "Statistici descriptive pentru preț și loves_count.",
            "explicatie": "Vezi rapid media, mediana, min, max etc. pentru variabile numerice.",
            "cod": """st.dataframe(df_products[['price_usd', 'loves_count']].describe())"""
        },
        "1️⃣8️⃣ Accesare cu iloc (product.csv)": {
            "descriere": "Afișează rândul 10 și coloana 2 din product.csv.",
            "explicatie": "Demonstrație de acces rapid la date cu iloc.",
            "cod": """st.write("Rândul 10, coloana 2 (index 9, 1):")
st.write(df_products.iloc[9, 1])"""
        },
    }

    selected = st.selectbox("🔍 Selectează o analiză", list(exercitii.keys()))
    st.markdown(f"#### {selected}")
    st.write(exercitii[selected]["descriere"])
    st.info(exercitii[selected]["explicatie"])

    st.markdown("##### Codul folosit pentru această analiză:")
    st.code(exercitii[selected]["cod"], language="python")

    if st.button("🔎 Execută analiza"):
        exec(exercitii[selected]["cod"], {'st': st, 'df_products': df_products, 'df_reviews': df_reviews, 'plt': plt})
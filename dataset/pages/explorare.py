import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_explorare():
    @st.cache_data
    def load_data():
        df_reviews = pd.read_csv("dataset/reviews_nan.csv")
        df_products = pd.read_csv("dataset/product_nan.csv")
        return df_reviews, df_products

    df_reviews, df_products = load_data()

    st.markdown('<h1 class="main-title">Explorarea și Înțelegerea Setului de Date</h1>', unsafe_allow_html=True)

    st.subheader("Vizualizare relațiilor dintre variabilele numerice (Pairplot)")
    numeric_cols = df_reviews.select_dtypes(include=['number']).dropna(axis=1)
    fig = sns.pairplot(numeric_cols)
    st.pyplot(fig)

    numeric_cols = df_products.select_dtypes(include=['number']).dropna(axis=1)
    fig = sns.pairplot(numeric_cols)
    st.pyplot(fig)

    st.write("""
        Pentru a înțelege mai bine datele noastre, vom analiza diferite aspecte, de la dimensiune și statistici descriptive, până la distribuția valorilor.
        Apasă pe butonul de sub fiecare secțiune pentru a vedea rezultatele explorării.
        """)

    def show_analysis(title, description, code, func):
        st.markdown(f"### {title}")
        st.write(description)
        st.code(code, language="python")
        if st.button(f"Execută analiza: {title}"):
            func()

    # **Număr de rânduri și coloane**
    show_analysis(
        "Dimensiunea datasetului",
        "Verificăm numărul total de rânduri și coloane din fiecare dataset.",
        "df_reviews.shape, df_products.shape",
        lambda: st.write(
            f"📊 `reviews_nan.csv`: {df_reviews.shape} rânduri și coloane, `product_nan.csv`: {df_products.shape}")
    )

    #  **Statistici descriptive**
    show_analysis(
        "Statistici descriptive pentru variabile numerice",
        "Calculăm statistici precum media, devierea standard, min/max și percentila 25/50/75 pentru fiecare variabilă numerică.",
        "df_reviews.describe(), df_products.describe()",
        lambda: st.write(df_reviews.describe(), df_products.describe())
    )

    # **Numărul de valori unice**
    show_analysis(
        "Numărul de valori unice per coloană",
        "Vedem câte valori unice există în fiecare coloană.",
        "df_reviews.nunique(), df_products.nunique()",
        lambda: st.write(df_reviews.nunique(), df_products.nunique())
    )

    # **Distribuția variabilelor categorice**
    show_analysis(
        "Distribuția variabilelor categorice",
        "Numărăm de câte ori apare fiecare valoare într-o coloană categorică.",
        "df_reviews['product_id'].value_counts(), df_products['brand_name'].value_counts()",
        lambda: st.write(df_reviews['product_id'].value_counts().head(10),
                         df_products['brand_name'].value_counts().head(10))
    )

    # **Analiza corelației între variabilele numerice**
    show_analysis(
        "Corelația între variabile numerice",
        "Calculăm coeficientul de corelație Pearson pentru a vedea relațiile dintre variabilele numerice.",
        "df_reviews.corr(), df_products.corr()",
        lambda: (
            plt.figure(figsize=(10, 5)),
            sns.heatmap(df_reviews.select_dtypes(include=['number']).corr(), annot=True, cmap="coolwarm"),
            st.pyplot(plt)
        )
    )

    # **Cele mai frecvente valori**
    show_analysis(
        "Cele mai frecvente valori dintr-o coloană",
        "Aflăm cele mai frecvente valori din coloanele `product_id` și `brand_name`.",
        "df_reviews['product_id'].value_counts(), df_products['brand_name'].value_counts()",
        lambda: st.write(df_reviews['product_id'].value_counts().head(10),
                         df_products['brand_name'].value_counts().head(10))
    )

    # **Compararea valorilor minime și maxime**
    show_analysis(
        "Valorile minime și maxime pentru variabile numerice",
        "Identificăm valorile extreme din fiecare coloană numerică.",
        "df_reviews.min(), df_reviews.max(), df_products.min(), df_products.max()",
        lambda: st.write(df_reviews.min(), df_reviews.max(), df_products.min(), df_products.max())
    )

    # **Distribuția unui subset de date**
    show_analysis(
        "Distribuția ratingurilor produselor",
        "Creăm un histogramă pentru distribuția ratingurilor.",
        "df_reviews['rating'].hist(bins=20)",
        lambda: (df_reviews['rating'].hist(bins=20), st.pyplot(plt))
    )

    # **Relația între două variabile numerice**
    show_analysis(
        "Corelația între `rating` și `helpfulness`",
        "Verificăm dacă recenziile cu rating mare sunt și considerate utile.",
        "df_reviews[['rating', 'helpfulness']].corr()",
        lambda: st.write(df_reviews[['rating', 'helpfulness']].corr())
    )

    #  **Identificarea produselor cele mai apreciate și cele mai criticate**
    show_analysis(
        "Cele mai apreciate și cele mai criticate produse",
        "Identificăm produsele cu cele mai mari și cele mai mici scoruri medii.",
        """
        best_products = df_reviews.groupby('product_id')['rating'].mean().sort_values(ascending=False).head(10)
        worst_products = df_reviews.groupby('product_id')['rating'].mean().sort_values().head(10)
        """,
        lambda: st.write(
            "⭐ **Produsele cu cele mai mari ratinguri:**",
            df_reviews.groupby('product_id')['rating'].mean().sort_values(ascending=False).head(10),
            "❌ **Produsele cu cele mai mici ratinguri:**",
            df_reviews.groupby('product_id')['rating'].mean().sort_values().head(10)
        )
    )

    st.title("📊 Analiza Avansată a Datelor: Grupări și Agregări")

    st.write("""
        În această secțiune, explorăm datele folosind **grupări**, **agregări**, **filtrări cu `.loc` și `.iloc`**, 
        precum și alte funcții avansate pentru extragerea insight-urilor relevante din date.

        Selectează o analiză și apasă butonul pentru a vizualiza rezultatele!
        """)

    # Definirea exercițiilor
    exercitii = {
        "1️⃣ Media ratingurilor pentru fiecare produs": {
            "descriere": "Calculăm media ratingurilor pentru fiecare produs și sortăm descrescător.",
            "cod": "df_reviews.groupby('product_id')['rating'].mean().sort_values(ascending=False)"
        },
        "2️⃣ Numărul total de recenzii per produs": {
            "descriere": "Numărăm câte recenzii are fiecare produs în datasetul de recenzii.",
            "cod": "df_reviews['product_id'].value_counts()"
        },
        "3️⃣ Produsele cu cele mai multe aprecieri (loves_count)": {
            "descriere": "Selectăm primele 10 produse cu cel mai mare număr de aprecieri.",
            "cod": "df_products[['product_id', 'loves_count']].nlargest(10, 'loves_count')"
        },
        "4️⃣ Produsele cu prețul maxim per categorie": {
            "descriere": "Identificăm produsul cu cel mai mare preț pentru fiecare categorie primară.",
            "cod": "df_products.loc[df_products.groupby('primary_category')['price_usd'].idxmax(), ['primary_category', 'product_id', 'price_usd']]"
        },
        "5️⃣ Distribuția prețurilor pe categorii de produse": {
            "descriere": "Calculăm statistici descriptive ale prețurilor pentru fiecare categorie.",
            "cod": "df_products.groupby('primary_category')['price_usd'].describe()"
        },
        "6️⃣ Cele mai utile recenzii (helpfulness maxim)": {
            "descriere": "Afișăm primele 5 recenzii considerate cele mai utile.",
            "cod": "df_reviews.nlargest(5, 'helpfulness')[['product_id', 'helpfulness']]"
        },
        "7️⃣ Produsele cu cele mai multe variații (child_count)": {
            "descriere": "Afișăm primele 10 produse cu cele mai multe variații disponibile.",
            "cod": "df_products[['product_id', 'child_count']].nlargest(10, 'child_count')"
        },
        "8️⃣ Produsele exclusiv online cu cel mai mare rating": {
            "descriere": "Selectăm produsele exclusiv online cu cele mai mari ratinguri medii.",
            "cod": "df_products[df_products['online_only'] == 1].groupby('product_id').agg(avg_rating=('rating', 'mean')).sort_values(by='avg_rating', ascending=False)"
        },
        "9️⃣ Media prețului și numărul de produse per brand": {
            "descriere": "Calculăm media prețului și numărul total de produse pentru fiecare brand.",
            "cod": "df_products.groupby('brand_id').agg(avg_price=('price_usd', 'mean'), product_count=('product_id', 'count')).sort_values(by='avg_price', ascending=False)"
        },
        "🔟 Categoriile cu cea mai mare variație de preț": {
            "descriere": "Calculăm variația prețurilor în fiecare categorie.",
            "cod": """df_products.groupby('primary_category').agg(
                    price_std=('price_usd', 'std')
                ).assign(price_range=lambda x: df_products.groupby('primary_category')['price_usd'].max() - df_products.groupby('primary_category')['price_usd'].min())"""
        }
    }

    exercitii.update({
        "1️⃣1️⃣ Produsele cu preț mai mare de 100 USD și exclusiv online": {
            "descriere": "Selectăm produsele care sunt exclusiv online și costă peste 100 USD.",
            "cod": """df_products.loc[
                    (df_products['price_usd'] > 100) & (df_products['online_only'] == 1),
                    ['product_id', 'price_usd', 'online_only']
                ]"""
        },
        "1️⃣2️⃣ Primele 5 produse după rating și număr de recenzii (iloc)": {
            "descriere": "Afișăm primele 5 produse sortate descrescător după rating și numărul total de feedback-uri.",
            "cod": """df_reviews[['product_id', 'rating', 'total_feedback_count']].sort_values(
                by=['rating', 'total_feedback_count'], ascending=[False, False]
                ).iloc[:5]
            """
        },
        "1️⃣3️⃣ Toate produsele dintr-o categorie anume (folosind loc)": {
            "descriere": "Filtrăm produsele dintr-o anumită categorie, de exemplu, 'Skincare'.",
            "cod": """df_products.loc[df_products['primary_category'] == 'Skincare', 
                    ['product_id', 'price_usd', 'child_count']]"""
        },
        "1️⃣4️⃣ Recenziile de la poziția 100 la 110 (iloc)": {
            "descriere": "Extragem recenziile dintre pozițiile 100 și 110 din dataset.",
            "cod": """df_reviews.iloc[100:110, [0, 1, 2, 3, 4]]"""
        }
    })

    selected_exercise = st.selectbox("🔍 Selectează o analiză", list(exercitii.keys()))

    st.markdown(f"### 🔹 {selected_exercise}")
    st.write(exercitii[selected_exercise]["descriere"])

    st.code(exercitii[selected_exercise]["cod"], language='python')

    if st.button("🔎 Execută analiza"):
        result = eval(exercitii[selected_exercise]["cod"])
        st.write("### 📊 Rezultate:")
        st.write(result)
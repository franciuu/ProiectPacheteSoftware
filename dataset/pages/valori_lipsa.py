import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def show_procesare():
    @st.cache_data
    def process_dataset():
        product_data = pd.read_csv("dataset/product_drop.csv")
        reviews_data = pd.read_csv("dataset/reviews_drop.csv")
        return product_data, reviews_data

    product_data, reviews_data = process_dataset()
    st.markdown('<h1 class="main-title">Tratarea valorilor lipsă</h1>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("📁 Identificarea valorilor lipsă - Produse")
        total = product_data.isnull().sum().sort_values(ascending=False)
        percent = (total * 100 / product_data.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=["Total", "Percent"])

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.bar(x=missing_data.index, height=missing_data["Percent"], color="pink")
        ax.set_ylabel('Percent')
        ax.set_title('Missing Data')
        ax.tick_params(axis='x', rotation=90)
        st.pyplot(fig)

    with col4:
        st.subheader("📁 Identificarea valorilor lipsă - Recenzii")
        total = reviews_data.isnull().sum().sort_values(ascending=False)
        percent = (total * 100 / reviews_data.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=["Total", "Percent"])

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.bar(x=missing_data.index, height=missing_data["Percent"], color="pink")
        ax.set_ylabel('Percent')
        ax.set_title('Missing Data')
        ax.tick_params(axis='x', rotation=90)
        st.pyplot(fig)

    st.markdown("### 🧠 Abordare pentru tratarea valorilor lipsă, coloane numerice")

    st.markdown("""
               În această secțiune ne concentrăm pe **tratarea valorilor lipsă din coloanele numerice**, aplicând metode diferite, adaptate în funcție de semnificația fiecărei variabile, proporția valorilor lipsă și recomandările teoretice din curs.

               #### 📦 Dataset: **Produse**
               - **`rating`** → *Regresie Liniară pe baza `loves_count` și `price_usd`*  
                 *Motivație:* Am ales regresia liniară deoarece `rating` este o variabilă numerică continuă, iar predictorii `loves_count` și `price_usd` sunt disponibili complet și pot explica variabilitatea ratingului într-un mod realist.

               - **`child_min_price` și `child_max_price`** → *Eliminare (drop)*  
                 *Motivație:* După analiza datasetului, s-a observat că aceste coloane conțin valori lipsă în cazul în care produsul nu are variații disponibile. Întrucât numărul de produse care nu au variații este mare, deci o eliminare a rândurilor nu este posibilă, am ales eliminarea coloanelor și excluderea lor din analiză.

               #### 📝 Dataset: **Recenzii**
               - **`helpfulness`** → *Înlocuire cu o valoare fixă*  
                 *Motivație:* Înlocuirea cu o valoare fixă este justificată deoarece `helpfulness` este o valoare **calculată**. Valorile lipsă reprezintă recenziile pentru care nu s-a lăsat nici un vot.

               - **`is_recommended`** → *Înlocuire cu valoarea cea mai frecventă (mod)*  
                 *Motivație:* Fiind o variabilă binară (0/1), metoda mod este potrivită pentru a păstra distribuția naturală.

               """)

    reviews_data['helpfulness'].fillna(0.0, inplace=True)

    for brand in reviews_data['brand_name'].unique():
        mode_val = reviews_data.loc[
            (reviews_data['brand_name'] == brand) & (reviews_data['is_recommended'].notnull()),
            'is_recommended'
        ].mode()
        if not mode_val.empty:
            reviews_data.loc[
                (reviews_data['brand_name'] == brand) & (reviews_data['is_recommended'].isnull()),
                'is_recommended'
            ] = mode_val[0]

    product_data.drop(columns=['child_min_price', 'child_max_price'], inplace=True)

    df_train = product_data.dropna(subset=['rating'])
    model = LinearRegression()
    model.fit(df_train[['loves_count', 'price_usd']], df_train['rating'])
    missing_rating = product_data[product_data['rating'].isnull()]
    product_data.loc[product_data['rating'].isnull(), 'rating'] = model.predict(
        missing_rating[['loves_count', 'price_usd']])

    st.markdown("### 🧠 Abordare pentru tratarea valorilor lipsă, coloane non-numerice")

    st.markdown("""
               În această etapă, am tratat valorile lipsă din **coloanele non-numerice**, aplicând soluții adaptate în funcție de tipul fiecărei variabile și contextul analizei.

               #### 📦 Dataset: **Produse**
               - **`variation_type`, `variation_value`, `variation_desc`, `tertiary_category`, `secondary_category`** → *Eliminare (drop)*  
                 *Motivație:* Aceste coloane descriu variații care lipsesc complet în majoritatea cazurilor și nu aduc valoare adăugată analizei.

               - **`size`, `highlights`, `ingredients`** → *Înlocuire cu valoarea cea mai frecventă (mod) per brand*  
                 *Motivație:* Aceste atribute sunt în general consistente în cadrul brandului. Pentru cazurile izolate (<1.4%) în care au rămas valori lipsă după completarea cu mod, s-au eliminat rândurile respective, având în vedere că sunt foarte puține și nu influențează semnificativ analiza.

               #### 📝 Dataset: **Recenzii**

               - **`skin_type`, `skin_tone`, `eye_color`, `hair_color`** → *Înlocuire cu mod per produs (`product_id`)*  
                 *Motivație:* Utilizatorii care cumpără același produs tind să aibă caracteristici personale similare (tonul pielii, tipul de piele, culoarea ochilor sau părului). Prin urmare, completarea acestor valori cu cele mai frecvente din cadrul aceluiași produs reflectă mai bine profilul real al consumatorilor și asigură o imputare contextualizată. Rândurile care au rămas tot cu `NaN` (<0.05%) au fost eliminate, deoarece sunt foarte puține și nu afectează semnificativ structura datelor.
               """)

    product_data.drop(
        columns=['variation_type', 'variation_value', 'variation_desc', 'tertiary_category', 'secondary_category'],
        inplace=True)

    for col in ['highlights', 'ingredients']:
        for brand in product_data['brand_name'].unique():
            mode_val = product_data.loc[
                (product_data['brand_name'] == brand) & (product_data[col].notnull()),
                col
            ].mode()
            if not mode_val.empty:
                product_data.loc[
                    (product_data['brand_name'] == brand) & (product_data[col].isnull()),
                    col
                ] = mode_val[0]

    for col in ['skin_type', 'skin_tone', 'eye_color', 'hair_color']:
        for pid in reviews_data['product_id'].unique():
            mode_val = reviews_data.loc[
                (reviews_data['product_id'] == pid) & (reviews_data[col].notnull()),
                col
            ].mode()
            if not mode_val.empty:
                reviews_data.loc[
                    (reviews_data['product_id'] == pid) & (reviews_data[col].isnull()),
                    col
                ] = mode_val[0]

    product_data.dropna(subset=['highlights', 'ingredients'], inplace=True)
    reviews_data.dropna(subset=['skin_type', 'skin_tone', 'eye_color', 'hair_color'], inplace=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("📁 Verificarea înlăturării valorilor lipsă - Produse")
        total = product_data.isnull().sum().sort_values(ascending=False)
        percent = (total * 100 / product_data.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=["Total", "Percent"])

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.bar(x=missing_data.index, height=missing_data["Percent"], color="pink")
        ax.set_ylabel('Percent')
        ax.set_title('Missing Data')
        ax.tick_params(axis='x', rotation=90)
        st.pyplot(fig)

    with col4:
        st.subheader("📁 Verificarea înlăturării valorilor lipsă - Recenzii")
        total = reviews_data.isnull().sum().sort_values(ascending=False)
        percent = (total * 100 / reviews_data.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=["Total", "Percent"])

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.bar(x=missing_data.index, height=missing_data["Percent"], color="pink")
        ax.set_ylabel('Percent')
        ax.set_title('Missing Data')
        ax.tick_params(axis='x', rotation=90)
        st.pyplot(fig)

    product_data.to_csv("dataset/product_nan.csv", index=False)
    reviews_data.to_csv("dataset/reviews_nan.csv", index=False)
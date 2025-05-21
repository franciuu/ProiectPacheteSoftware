import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def show_prediction():
    st.markdown('<h1 class="main-title">Predicție: Rating Review</h1>', unsafe_allow_html=True)

    st.markdown("""
    ### ℹ️ Descriere generală

    În această secțiune construim un **model de regresie liniară** care prezice valoarea `rating_review` – adică scorul acordat de un utilizator într-o recenzie – pe baza tuturor variabilelor numerice disponibile din dataseturile `reviews_sn.csv` și `product_sn.csv`.

    - 📎 Seturile de date au fost anterior **standardizate** (Z-score), iar variabilele categorice encodate.
    - 🔗 Fișierele sunt îmbinate pe `product_id`, astfel încât fiecare recenzie beneficiază și de caracteristicile produsului asociat.
    - 🧠 Modelul este evaluat pe baza a 3 metrici: **MAE**, **MSE** și **R²**.

    Acest model ne ajută să înțelegem în ce măsură variabilele disponibile pot explica percepția utilizatorului exprimată printr-un rating numeric.
    """)

    df_reviews = pd.read_csv("dataset/reviews_sn.csv")
    df_products = pd.read_csv("dataset/product_sn.csv")

    df = pd.merge(df_reviews, df_products, on="product_id", suffixes=("_review", "_product"))

    target = "rating_review"
    exclude = ["product_id", target]

    X = df.drop(columns=exclude, errors="ignore")
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.subheader("📈 Evaluarea modelului")
    col1, col2, col3 = st.columns(3)
    col1.metric("📉 MAE", f"{mae:.4f}")
    col2.metric("📉 MSE", f"{mse:.4f}")
    col3.metric("📈 R²", f"{r2:.4f}")

    st.markdown("""
    🧠 **Interpretare:**  
    - R² ridicat → modelul explică o proporție mare din variația ratingului recenziilor.  
    - MAE și MSE reduse → predicții precise pentru date standardizate.
    """)

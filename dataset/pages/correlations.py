import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def show_correlations():
    st.markdown('<h1 class="main-title">Heatmap Corelații între Seturi de Date</h1>', unsafe_allow_html=True)

    @st.cache_data
    def load_data():
        df_reviews = pd.read_csv("dataset/clean_reviews_outliers.csv", low_memory=False)
        df_products = pd.read_csv("dataset/clean_products_outliers.csv", low_memory=False)
        return df_reviews, df_products

    df_reviews, df_products = load_data()

    df_reviews = df_reviews[
        (df_reviews["total_pos_feedback_count"] + df_reviews["total_neg_feedback_count"]) > 0
        ].copy()

    df_reviews["positive_ratio"] = df_reviews["total_pos_feedback_count"] / (
            df_reviews["total_pos_feedback_count"] + df_reviews["total_neg_feedback_count"]
    )

    df_reviews = df_reviews.drop(columns=["total_pos_feedback_count", "total_neg_feedback_count"])
    df_reviews.to_csv("dataset/clean_reviews_outliers_nou.csv", index=False)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📘 Recenzii")

        st.markdown("### ℹ️ Preprocesare variabile recenzii")
        st.markdown("""
        Înainte de analiza corelațiilor, s-au efectuat următoarele transformări asupra setului de date `df_reviews`:

        - ❌ **Eliminare coloane redundante:** `total_pos_feedback_count` și `total_neg_feedback_count`  
          - Acestea sunt deja reprezentate în noua variabilă calculată.

        - ✅ **Calculare variabilă nouă:** `positive_ratio`  
          - Formula: `total_pos / (total_pos + total_neg)`  
          - Reprezintă proporția de reacții pozitive – un indicator clar al aprecierii unei recenzii.

        - ❗ **Motivație:**  
          - Eliminarea redundanței previne colinearitatea și îmbunătățește performanța modelelor predictive.
        """)

        numeric_cols_reviews = [
            col for col in df_reviews.select_dtypes(include=["int64", "float64", "float32"]).columns
            if not col.lower().startswith("unnamed")
        ]

        if len(numeric_cols_reviews) >= 2:
            corr_reviews = df_reviews[numeric_cols_reviews].corr()
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr_reviews, annot=True, cmap="coolwarm", center=0, fmt=".2f", linewidths=0.5, ax=ax1)
            ax1.set_title("Heatmap Corelații - Recenzii (cu positive_ratio)")
            st.pyplot(fig1)

            st.markdown("""
            **📌 Interpretare:**
            - `helpfulness` și `positive_ratio` (0.94): Există o corelație foarte puternică între cât de utile sunt considerate recenziile și proporția recenziilor pozitive. Cu alte cuvinte, recenziile considerate utile tind să fie și pozitive.
            - `rating` și `is_recommended` (0.82): Rating-ul oferit și recomandarea produsului sunt strâns legate. Un rating mai mare este asociat cu o probabilitate mai mare ca produsul să fie recomandat.
            - `total_feedback_count`: Are corelații foarte slabe sau chiar negative cu celelalte variabile, cea mai mare fiind -0.14 cu positive_ratio. Asta sugerează că numărul total de feedback-uri nu este legat semnificativ de calitatea sau tonul recenziilor.
            - `price_usd`: Prețul produsului nu are o corelație semnificativă cu nicio altă variabilă (toate valorile sunt apropiate de 0), deci prețul nu influențează direct rating-ul, recomandarea sau utilitatea recenziilor.
            """)
        else:
            st.warning("Tabelul `df_reviews` nu conține suficiente coloane numerice.")

    with col2:
        st.markdown("### 🛍️ Produse")
        numeric_cols_products = [
            col for col in df_products.select_dtypes(include=["int64", "float64", "float32"]).columns
            if not col.lower().startswith("unnamed")
        ]

        if len(numeric_cols_products) >= 2:
            corr_products = df_products[numeric_cols_products].corr()
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr_products, annot=True, cmap="coolwarm", center=0, fmt=".2f", linewidths=0.5, ax=ax2)
            ax2.set_title("Heatmap Corelații - Produse")
            st.pyplot(fig2)

            st.markdown("""
            **📌 Interpretare:**
            - `loves_count` și `child_count` (0.41): Produsele cu mai multe variante (child_count mai mare) tind să aibă și mai multe „loves” din partea utilizatorilor.
            - `limited_edition` și `out_of_stock` (0.17): Produsele ediție limitată tind să fie mai des epuizate din stoc.
            - `loves_count` și `online_only` (-0.35): Produsele disponibile exclusiv online primesc mai puține „loves” din partea utilizatorilor.
            - `rating` nu este influențat semnificativ de alte variabile – deci reflectă evaluarea directă, nu caracteristici ale produsului.
            - `price_usd` este slab corelat cu celelalte variabile, cea mai mare corelație fiind cu online_only (-0.16), ceea ce sugerează că prețul nu influențează semnificativ celelalte caracteristici analizate.
            """)
        else:
            st.warning("Tabelul `df_products` nu conține suficiente coloane numerice.")

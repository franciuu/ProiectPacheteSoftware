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
            - `rating` și `is_recommended` sunt **puternic corelate** (**0.82**) – recenziile bune duc la recomandări.
            - `positive_ratio` are **corelație pozitivă moderată** cu `helpfulness` și `rating` – un semnal clar că reacțiile pozitive indică satisfacție.
            - `helpfulness` are o **corelație negativă puternică** cu feedbackul negativ – review-urile slabe sunt considerate mai puțin utile.
            - `price_usd` rămâne **necorelat** – prețul nu influențează calitatea sau aprecierea recenziei.
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
            - `loves_count` are **corelație moderată pozitivă** cu `child_count` (**0.41**) – produsele cu mai multe variante sunt mai apreciate.
            - `loves_count` are **corelație slab negativă** cu `new` (**-0.29**) și `online_only` (**-0.35**) – produsele noi sau doar online par mai puțin populare.
            - `rating` nu este influențat semnificativ de alte variabile – deci reflectă evaluarea directă, nu caracteristici ale produsului.
            - `price_usd` este **aproape independent** – nu influențează popularitatea sau scorul produselor.
            """)
        else:
            st.warning("Tabelul `df_products` nu conține suficiente coloane numerice.")

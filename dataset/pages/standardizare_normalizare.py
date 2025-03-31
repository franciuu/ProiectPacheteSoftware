import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def show_standardize_normalize():
    st.title("Standardizare")

    @st.cache_data
    def load_data():
        df_reviews = pd.read_csv("dataset/reviews_encoded.csv", low_memory=False)
        df_products = pd.read_csv("dataset/products_encoded.csv", low_memory=False)
        return df_reviews, df_products

    df_reviews, df_products = load_data()

    def get_numeric_cols(df, exclude_cols=[]):
        return [col for col in df.select_dtypes(include=["int64", "float64"]).columns
                if col not in exclude_cols and not col.lower().startswith("unnamed")]

    reviews_numeric = get_numeric_cols(df_reviews, exclude_cols=['product_id'])
    products_numeric = get_numeric_cols(df_products, exclude_cols=['product_id'])

    scaler = StandardScaler()
    df_reviews[reviews_numeric] = scaler.fit_transform(df_reviews[reviews_numeric])
    df_products[products_numeric] = scaler.fit_transform(df_products[products_numeric])

    os.makedirs("dataset", exist_ok=True)
    df_reviews.to_csv("dataset/reviews_sn.csv", index=False)
    df_products.to_csv("dataset/product_sn.csv", index=False)

    st.subheader("📘 Recenzii - După standardizare")
    st.dataframe(df_reviews.head())

    st.subheader("🛍️ Produse - După standardizare")
    st.dataframe(df_products.head())

    st.success("✅ Fișierele `reviews_sn.csv` și `product_sn.csv` au fost salvate cu valorile standardizate.")

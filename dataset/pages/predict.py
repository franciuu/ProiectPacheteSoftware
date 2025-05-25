import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb

def show_prediction():
    st.markdown('<h1 style="color:#6C3483;">Analiză predictivă și exploratorie pe două seturi de date cosmetice</h1>',
                unsafe_allow_html=True)
    st.markdown("""
        Vom parcurge două abordări de analiză a datelor:
        - **Predicție a ratingului recenziilor folosind Linear Regression** pe setul de recenzii.
        - **Predicție a prețului produselor folosind Random Forest și XGBoost** pe setul de produse.
        """)

    st.header("1️⃣ Predicție rating review cu Linear Regression")
    st.markdown("""
    **Scop:**  
    Să prezicem ratingul unei recenzii folosind caracteristicile disponibile în fișierul.  
    Vom construi un model de regresie liniară, îl vom evalua și vom interpreta rezultatele.
    """)

    df_reviews = pd.read_csv("dataset/reviews_sn.csv")
    target = "rating"
    exclude = ["product_id", "brand_name", target]
    Xr = df_reviews.drop(columns=exclude, errors="ignore")
    y = df_reviews[target]

    Xr_train, Xr_test, y_train, y_test = train_test_split(Xr, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(Xr_train, y_train)
    y_pred = model.predict(Xr_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.subheader("📊 Rezultatele modelului Linear Regression")
    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", f"{mae:.4f}")
    col2.metric("MSE", f"{mse:.4f}")
    col3.metric("R²", f"{r2:.4f}")

    st.markdown("""
    **Interpretare:**
    - **MAE (Eroare Absolută Medie)**  
        Această valoare ne arată, în medie, cu cât diferă predicțiile modelului față de valorile reale ale ratingului.  
        - O valoare de 0.4310 înseamnă că, în medie, modelul greșește cu aproximativ 0.43 puncte la fiecare predicție de rating (pe o scară de la 1 la 5, de exemplu, această eroare este destul de mică).
        - Un MAE mai mic indică o precizie mai bună.
    - **MSE (Eroare Medie Pătratică)**  
        MSE penalizează mai puternic erorile mari, fiind sensibil la predicțiile foarte greșite.
        - O valoare de 0.3317 sugerează că variația pătratică dintre valorile reale și cele prezise este redusă.
        - Cu cât MSE este mai mic, cu atât modelul este mai robust la erori mari.
    - **R² (Coeficient de determinare)**  
        R² măsoară proporția din variația ratingului real care este explicată de model.
        - Un scor de 0.6742 înseamnă că aproximativ 67% din variația ratingurilor din setul de test este explicată de modelul nostru.
        - Un R² apropiat de 1 indică un model foarte bun, în timp ce valori apropiate de 0 arată că modelul nu explică bine datele.
    > Un R² de 0.67 arată că două treimi din variația ratingurilor poate fi explicată de datele de intrare, ceea ce este un rezultat solid pentru un model liniar, mai ales într-un domeniu cu factori subiectivi ca evaluarea produselor cosmetice.
    > Erorile (MAE și MSE) sunt relativ mici, ceea ce sugerează că, pentru majoritatea recenziilor, predicțiile sunt apropiate de realitate.  
    > Totuși, există încă o treime din variație care nu este explicată, ceea ce poate fi cauzat de factori subiectivi, variabile lipsă sau relații neliniare pe care acest model nu le poate surprinde.
    """)

    st.header("2️⃣ Predicție preț produs cu Random Forest și XGBoost")
    st.markdown("""
       **Scop:**  
       Să prezicem prețul unui produs folosind caracteristicile disponibile în fișierul de produse, utilizând două modele avansate: Random Forest și XGBoost.  
       Vom compara performanța acestora și vom interpreta rezultatele.
       """)

    df_products = pd.read_csv("dataset/product_sn.csv")
    target = "price_usd"
    exclude = ["product_id", "brand_name", target]
    X = df_products.drop(columns=exclude, errors="ignore")
    y = df_products[target]
    X = X.select_dtypes(include=[np.number])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)

    # XGBoost
    xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict(X_test)

    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_mse = mean_squared_error(y_test, rf_pred)
    rf_r2 = r2_score(y_test, rf_pred)
    xgb_mae = mean_absolute_error(y_test, xgb_pred)
    xgb_mse = mean_squared_error(y_test, xgb_pred)
    xgb_r2 = r2_score(y_test, xgb_pred)

    st.subheader("📊 Rezultate Random Forest vs XGBoost")
    results = pd.DataFrame({
        "Model": ["Random Forest", "XGBoost"],
        "MAE": [rf_mae, xgb_mae],
        "MSE": [rf_mse, xgb_mse],
        "R²": [rf_r2, xgb_r2]
    })
    st.dataframe(results)

    st.markdown(""" 
       **Interpretare rezultate Random Forest vs XGBoost**

        - **MAE (Mean Absolute Error):**  
        Ambele modele au valori MAE similare (Random Forest: 0.4025, XGBoost: 0.4087), ceea ce înseamnă că, în medie, predicțiile lor diferă de valorile reale ale prețului cu aproximativ 0.40 unități. Un MAE mai mic indică predicții mai precise, iar diferența dintre cele două modele este foarte mică.

        - **MSE (Mean Squared Error):**  
        Valorile MSE sunt apropiate (Random Forest: 0.4619, XGBoost: 0.4682), ceea ce arată că ambele modele gestionează bine erorile mari, fără să existe predicții extrem de greșite. Un MSE mai mic este preferabil, iar Random Forest are un ușor avantaj aici.

        - **R² (Coeficient de determinare):**  
        R² măsoară cât de mult din variația prețului este explicată de model. Random Forest are un scor R² de 0.4904, iar XGBoost de 0.4835. Ambele modele explică aproape 49% din variația prețului, ceea ce este rezonabil pentru un set de date real, dar arată că există încă factori care nu sunt surprinși de modele.

        > **Concluzie:**  
        > Ambele modele oferă performanțe similare, cu un ușor avantaj pentru Random Forest la toate cele trei metrici. Niciun model nu depășește clar celălalt, astfel încât alegerea finală poate depinde de alte criterii (timp de antrenare, interpretabilitate sau preferințe de implementare).  
        > Pentru o acuratețe și mai mare, se pot încerca optimizări suplimentare sau inginerie de caracteristici.
       """)


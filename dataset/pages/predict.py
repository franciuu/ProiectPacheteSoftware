import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb
import statsmodels.api as sm

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
    Vom construi un model de regresie liniară, îl vom evalua pe setul de test și vom interpreta rezultatele.
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

    Xr_train_sm = sm.add_constant(Xr_train)
    sm_model = sm.OLS(y_train, Xr_train_sm).fit()

    Xr_test_sm = sm.add_constant(Xr_test)
    Xr_test_sm = Xr_test_sm.reindex(columns=Xr_train_sm.columns, fill_value=0)
    y_pred_sm = sm_model.predict(Xr_test_sm)
    r2_sm_test = r2_score(y_test, y_pred_sm)

    st.markdown("#### Toate rezultatele de mai jos sunt calculate pe **setul de test** (date nevăzute la antrenare) pentru o evaluare obiectivă a performanței.")

    st.subheader("📈 Analiză statistică detaliată cu statsmodels (antrenat pe train, evaluat pe test)")
    st.markdown("""
    Rezumatul de mai jos oferă informații detaliate despre coeficienții modelului (antrenați pe train), semnificația statistică a fiecărei variabile, intervale de încredere și diagnostice de model.
    """)
    st.text(sm_model.summary())

    st.markdown(f"""
**🧮 Explicație R²:**  
- **R² afișat în summary (0.692):** Este calculat pe setul de antrenament și arată cât de bine se potrivește modelul pe datele pe care a fost antrenat.  
- **R² calculat cu coeficienții statsmodels pe setul de test:** `{r2_sm_test:.4f}`  
  Acesta reflectă acuratețea reală pe date nevăzute (test), fiind o estimare mai realistă a performanței modelului în practică.

**De ce pot exista diferențe mici între R² din statsmodels și scikit-learn?**  
- statsmodels și scikit-learn folosesc formule aproape identice pentru R², dar pot apărea diferențe minore din cauza modului de tratare a interceptului și a preciziei numerice.
- R² din statsmodels summary este pe train, iar R² din scikit-learn este pe test. Pentru comparație corectă, folosește mereu R² pe test.

**Interpretare OLS Regression Results:**  
- **R-squared:** 0.692 → Modelul explică 69.2% din variația ratingurilor din setul de antrenament.
- **Adj. R-squared:** 0.691 → Corectat pentru numărul de variabile, penalizează adăugarea de predictori irelevanți.
- **F-statistic:** 469.8 (p=0.00) → Modelul este semnificativ statistic (cel puțin o variabilă explică ratingul).
- **Coeficienți:**  
    - Fiecare coeficient arată cu cât se modifică ratingul la o unitate creștere a variabilei respective, restul constant.
    - P-value < 0.05 (ex: `is_recommended`, `helpfulness`) înseamnă efect semnificativ statistic.
    - Intervalele [0.025, 0.975] arată limitele între care se află coeficientul cu 95% probabilitate.
- **Diagnostică model:**  
    - **Durbin-Watson:** 2.028 → Nu există autocorelație a erorilor.
    - **Jarque-Bera:** 6265.267 (p=0.00) → Reziduurile nu sunt distribuite normal, dar la seturi mari acest lucru e comun.
    - **Cond. No.:** 5.63e+15 → Posibilă multicoliniaritate (corelații între predictori).

> **Pe scurt:**  
> - R² pe test este cel mai relevant pentru performanța reală.
> - Coeficienții semnificativi statistic pot fi interpretați ca factori determinanți ai ratingului.
> - Modelul explică o proporție mare din variație, dar nu totul (există factori subiectivi sau neliniați).
    """)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.subheader("📊 Rezultatele modelului Linear Regression (scikit-learn, pe test)")
    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", f"{mae:.4f}")
    col2.metric("MSE", f"{mse:.4f}")
    col3.metric("R²", f"{r2:.4f}")

    st.markdown("""
    ### 🔎 Interpretare rezultate

    - **MAE (Eroare Absolută Medie):**  
      Modelul greșește, în medie, cu aproximativ 0.43 puncte la fiecare predicție de rating. 

    - **MSE (Eroare Medie Pătratică):**  
      Erorile mai mari sunt penalizate suplimentar, iar valoarea de 0.3317 arată că modelul nu face predicții foarte greșite. Un MSE mai mic reflectă robustețea modelului la erori mari.

    - **R² (Coeficient de determinare):**  
      Aproximativ 67% din variația ratingurilor reale este explicată de model pe setul de test. Aceasta înseamnă că modelul surprinde bine relația dintre caracteristici și rating, dar există încă factori suplimentari care nu sunt incluși în model.

    > Toate aceste valori sunt calculate pe setul de test (date nevăzute de model la antrenare), deci oferă o imagine realistă asupra performanței modelului în practică.
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

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)

    xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict(X_test)

    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_mse = mean_squared_error(y_test, rf_pred)
    rf_r2 = r2_score(y_test, rf_pred)
    xgb_mae = mean_absolute_error(y_test, xgb_pred)
    xgb_mse = mean_squared_error(y_test, xgb_pred)
    xgb_r2 = r2_score(y_test, xgb_pred)

    st.subheader("📊 Rezultate Random Forest vs XGBoost (toate pe setul de test)")
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

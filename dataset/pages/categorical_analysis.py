import streamlit as st
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer

def show_categorical_analysis():
    st.title("Analiza Variabilelor Categoriale din `products.csv`")

    st.markdown("""
    În această secțiune, explorăm variabilele **categoriale** din fișierul `products.csv`, explicăm metodele de **encodare** potrivite pentru acestea și le aplicăm practic.

    ⚙️ Encodarea transformă variabilele **categorice** în formate **numerice** care pot fi folosite în modele de Machine Learning.
    """)

    df = pd.read_csv("dataset/clean_products_outliers.csv")

    # 1. BRAND NAME
    st.subheader("🔹 `brand_name` — Label Encoding")
    st.markdown("""
    **📌 Tip:** Categorie nominală 

    **✅ Scop:** Să înțelegem dacă anumite branduri influențează ratingul, prețul, preferințele utilizatorilor.

    **🧠 Ce aplicăm:** `Label Encoding` → fiecare brand primește un cod numeric unic. Am luat această alegere deoarece `Label Encoding` păstrează dimensiunea mică a datasetului, spre deosebire de `One-Hot` (care explodează dimensionalitatea).

    **🚀 Ce îmbunătățește:**
    - Transformă `string`-urile în format numeric pentru ML.
    - Reduce complexitatea și dimensiunea datasetului.
    - Permite vizualizări rapide pe baza codului brandului (ex: medii per brand).

    **ℹ️ Despre `LabelEncoder`:**
    - Atribuie un număr întreg fiecărei clase unice.
    - Nu presupune vreo ordine între valori.
    """)
    le_brand = LabelEncoder()
    df['brand_name'] = le_brand.fit_transform(df['brand_name'])

    st.write(df[['brand_name']].head())

    # 2. INGREDIENTS - TF-IDF
    st.subheader("🔹 `ingredients` — TF-IDF Vectorization (Top 10)")
    st.markdown("""
    **📌 Tip:** Text semi-structurat, listă lungă de ingrediente

    **✅ Scop:** Extragerea trăsăturilor din compoziție care ar putea influența ratingul sau preferințele utilizatorilor.

    **🧠 Ce aplicăm:** `TF-IDF` (Term Frequency-Inverse Document Frequency). Am luat această alegere pentru că `ingredients` este text liber, nu o categorie fixă. `TF-IDF` transformă textul în scoruri numerice care reflectă importanța fiecărui cuvânt în contextul tuturor produselor. Evită bias-ul introdus de ingrediente foarte comune (le penalizează frecvența globală).

    **🚀 Ce îmbunătățește:**
    - Permite clasificarea produselor pe bază de compoziție.
    - Poți descoperi ingrediente care contribuie la rating pozitiv/negativ.

    **ℹ️ Despre `TF-IDF`:**
    - TF: cât de des apare un cuvânt într-un produs
    - IDF: inversul frecvenței în toate produsele
    - Output: scoruri numerice pentru cele mai informative ingrediente
    """)

    def extract_ingredients(text):
        try:
            items = re.findall(r"'(.*?)'", text)
            ingredients = [i for i in items if not i.endswith(':')]
            return ' '.join(ingredients)
        except:
            return ''

    df['ingredients'] = df['ingredients'].astype(str).apply(extract_ingredients)

    tfidf = TfidfVectorizer(max_features=10)
    tfidf_matrix = tfidf.fit_transform(df['ingredients'])
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=[f"ing_{col}" for col in tfidf.get_feature_names_out()])
    df = df.drop(columns=['ingredients'])  # eliminăm coloana originală
    df = pd.concat([df, tfidf_df], axis=1)

    st.dataframe(tfidf_df.head())

    # 3. HIGHLIGHTS - MultiLabel Binarizer
    st.subheader("🔹 `highlights` — MultiLabel Binarizer")
    st.markdown("""
    **📌 Tip:** Listă de etichete (multi-label) per produs

    **✅ Scop:** Evidențiază calități de marketing (ex: "Vegan", "Cruelty-Free") care pot influența decizia de cumpărare.

    **🧠 Ce aplicăm:** `MultiLabelBinarizer` → fiecare atribut devine o coloană binară (1/0). Am luat această alegere deoarece fiecare produs poate avea mai multe highlights, deci nu e o simplă variabilă categorică.

    **🚀 Ce îmbunătățește:**
    - Ne permite să analizăm care highlights sunt frecvente și care contribuie la performanță.
    - Devine o sursă puternică de features (trăsături) pentru clasificare.

    **ℹ️ Despre `MultiLabelBinarizer`:**
    - Acceptă liste de etichete multiple.
    - Generează o coloană pentru fiecare etichetă unică.
    - Valorile sunt binare (1 = atribut prezent).
    """)

    def parse_highlights(x):
        try:
            return re.findall(r"'(.*?)'", x)
        except:
            return []

    highlights_parsed = df['highlights'].astype(str).apply(parse_highlights)
    mlb = MultiLabelBinarizer()
    hl_df = pd.DataFrame(mlb.fit_transform(highlights_parsed), columns=[f"hl_{c}" for c in mlb.classes_])
    df = df.drop(columns=['highlights'])
    df = pd.concat([df, hl_df], axis=1)

    st.dataframe(hl_df.head())

    # 4. PRIMARY CATEGORY - One Hot
    st.subheader("🔹 `primary_category` — One-Hot Encoding")
    st.markdown("""
    **📌 Tip:** Categorie nominală unică (fiecare produs are una)

    **✅ Scop:** Vrem să știm din ce categorie face parte produsul — Fragrance, Skincare, Makeup etc.

    **🧠 Ce aplicăm:** `One-Hot Encoding` → fiecare categorie devine o coloană binară. Am luat această alegere deoarece `primary_category` are puține valori unice. `One-Hot` e ideal pentru astfel de cazuri pentru că nu impune o ordine între valori. Modelele ML tratează fiecare categorie ca o trăsătură independentă.

    **🚀 Ce îmbunătățește:**
    - Ne ajută să vedem ce categorii sunt cele mai populare.
    - Poate evidenția diferențe de preț, rating sau compoziție pe categorii.

    **ℹ️ Despre `One-Hot Encoding`:**
    - Transformă o coloană cu N categorii în N coloane binare.
    - Evită ambiguitatea pe care o introduc codările numerice simple.
    """)

    ohe_df = pd.get_dummies(df['primary_category'], prefix='cat').astype(int)
    df = df.drop(columns=['primary_category'])
    df = pd.concat([df, ohe_df], axis=1)

    st.dataframe(ohe_df.head())

    # 5. Salvare finală
    df.to_csv("dataset/products_encoded.csv", index=False)
    st.success("✅ Fișierul `products_encoded.csv` a fost salvat cu succes!")

    st.title("📋 Analiza Variabilelor Categoriale din `reviews.csv`")

    st.markdown("""
        În această secțiune, analizăm variabilele **categoriale** din fișierul `reviews.csv` și aplicăm metode de **encodare** potrivite fiecărei coloane.

        ⚙️ Encodarea transformă informația textuală sau simbolică în format numeric, compatibil cu modele de Machine Learning.
        """)

    df = pd.read_csv("dataset/clean_reviews_outliers_nou.csv")

    #si pt brand name din reviews
    le_brand = LabelEncoder()
    df['brand_name'] = le_brand.fit_transform(df['brand_name'])

    # --- SKIN TONE ---
    st.subheader("🔹 `skin_tone` - One-Hot Encoding")
    st.markdown("""
        **Scop:** Tonul pielii poate influența recomandarea sau evaluarea anumitor produse.  
        **De ce One-Hot:** Nu există o ordine logică între valori.  
        **Ce aplicăm:** `pd.get_dummies()`  
        **Ce obținem:** Variabile binare pentru fiecare categorie (`light`, `medium`, etc).
        """)
    tone_df = pd.get_dummies(df['skin_tone'], prefix="tone").astype(int)
    df = pd.concat([df.drop(columns=['skin_tone']), tone_df], axis=1)
    st.dataframe(tone_df.head())

    # --- EYE COLOR ---
    st.subheader("🔹 `eye_color` - One-Hot Encoding")
    st.markdown("""
        **Scop:** Poate fi relevant pentru produsele de machiaj (rimel, farduri etc.)  
        **De ce One-Hot:** Valorile sunt nominale, fără ierarhie.  
        **Ce aplicăm:** `pd.get_dummies()`
        """)
    eye_df = pd.get_dummies(df['eye_color'], prefix="eye").astype(int)
    df = pd.concat([df.drop(columns=['eye_color']), eye_df], axis=1)
    st.dataframe(eye_df.head())

    # --- SKIN TYPE ---
    st.subheader("🔹 `skin_type` - One-Hot Encoding")
    st.markdown("""
        **Scop:** Tipul pielii influențează experiența cu produsul.  
        **De ce One-Hot:** Nu există o relație ordonată între `dry`, `oily`, `combination`.  
        **Ce aplicăm:** `pd.get_dummies()`
        """)
    skin_df = pd.get_dummies(df['skin_type'], prefix="skin").astype(int)
    df = pd.concat([df.drop(columns=['skin_type']), skin_df], axis=1)
    st.dataframe(skin_df.head())

    # --- HAIR COLOR ---
    st.subheader("🔹 `hair_color` - One-Hot Encoding")
    st.markdown("""
        **Scop:** Unele produse pot avea efect diferit în funcție de culoarea părului.  
        **De ce One-Hot:** Categorii nominale (brown, blonde etc.).  
        **Ce aplicăm:** `pd.get_dummies()`
        """)
    hair_df = pd.get_dummies(df['hair_color'], prefix="hair").astype(int)
    df = pd.concat([df.drop(columns=['hair_color']), hair_df], axis=1)
    st.dataframe(hair_df.head())

    # --- Salvare ---
    st.subheader("📁 Salvare fișier encodat")
    df.to_csv("dataset/reviews_encoded.csv", index=False)
    st.success("✅ Fișierul `reviews_encoded.csv` a fost salvat cu succes.")


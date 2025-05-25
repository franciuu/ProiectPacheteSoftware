import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def show_outliers():
    product_data = pd.read_csv("dataset/product_nan.csv")
    reviews_data = pd.read_csv("dataset/reviews_nan.csv")
    st.markdown('<h1 class="main-title">Detectarea și Tratarea Valorilor Extreme</h1>', unsafe_allow_html=True)

    st.markdown("""
          ## 🔬 Ce este un **Boxplot**?
          Un **boxplot** este un grafic care ne ajută să înțelegem distribuția unui set de date și să identificăm **outliers** (valori extreme).

          ### 🔹 Elemente ale unui Boxplot:
          - 🟥 **Cutia (Box-ul):** Reprezintă **Interquartile Range (IQR)**, adică intervalul dintre **percentila 25% (Q1) și percentila 75% (Q3)**.
          - ➖ **Linia din mijloc:** Indică **mediana (Q2, percentila 50%)**, valoarea centrală a distribuției.
          - 📏 **Mustățile (Whiskers):** Se extind la **1.5 × IQR** față de Q1 și Q3 și reprezintă intervalul acceptabil al datelor.
          - 🔴 **Punctele din afara mustăților:** Sunt **outliers** – valori extreme care pot influența analiza.

          ### 🎯 **La ce te ajută un Boxplot?**
          ✅ **Detectarea valorilor extreme** – identificăm produse/recenzii care au valori anormale.  
          ✅ **Analiza distribuției datelor** – vedem dacă distribuția este **simetrică sau asimetrică**.  
          ✅ **Luarea deciziilor** – putem elimina sau transforma outlierii pentru o analiză mai precisă.
          
          """)
    st.info("Pentru interpretarea graficelor am tinut cont si de statisticile generate in sectiunea anterioara relevante pentru boxplot deoarece unele valori sunt greu de interpretat")

    numeric_cols_product = ["loves_count", "rating", "price_usd", "child_count"]
    numeric_cols_reviews = ["rating", "helpfulness", "total_feedback_count", "total_neg_feedback_count",
                            "total_pos_feedback_count", "price_usd"]

    st.markdown("### 🛍️ Produse Sephora - Detectarea Outliers")
    st.info("Am evidentiat linia medianei pentru a o putea distinge")
    fig_product, axes_product = plt.subplots(1, len(numeric_cols_product), figsize=(15, 5))
    fig_product.suptitle("Boxplot pentru setul de date - Produse")

    for i, col in enumerate(numeric_cols_product):
        sns.boxplot(y=product_data[col], ax=axes_product[i], color="pink", medianprops={'color': 'red', 'ls': ':', 'lw': 3})
        plt.ticklabel_format(style='plain', axis='y')
        axes_product[i].set_title(col)

    st.pyplot(fig_product)

    st.markdown("## 📊 Analiza detaliată a variabilelor")

    st.write("""
        ### 📌 `loves_count` - Numărul de utilizatori care au marcat produsul ca favorit
        Această vizualizare ne ajută să înțelegem cât de popular este fiecare produs pe Sephora. 

        - **Mediana** este aproximativ 10.000, ceea ce înseamnă că jumătate dintre produse au sub 10.000 de aprecieri.
        - **IQR** (Interquartile Range) se întinde între 3.802 (Q1) și 27.278 (Q3), indicând o variabilitate mare între produsele cu popularitate medie.
        - **Mustățile** se extind până în jur de ~62.500, ceea ce înseamnă că majoritatea produselor se încadrează în acest interval (considerate non-outlieri).
        - **Outlierii** sunt numeroși și extrem de mari, depășind chiar și 1.400.000, ceea ce arată că există produse excepțional de populare, care distorsionează semnificativ distribuția vizuală.

        🛍️ **Concluzie:**  
        Distribuția loves_count este puternic dezechilibrată (right-skewed), cu o majoritate de produse care au între 4.000 și 30.000 de aprecieri, dar și cu un număr semnificativ de produse extrem de populare care depășesc cu mult acest interval. 

        ---
    
        ### 📌 `rating` - Evaluarea produselor
        Acest boxplot arată distribuția ratingurilor oferite produselor Sephora de către utilizatori.

        - **Mediana** este în jur de 4.25, ceea ce înseamnă că 50% dintre produse au ratinguri sub acesta valoare
        - **IQR (Interquartile Range)** se întinde de la Q1 = 4.0 până la Q3 = 4.52, indicând o concentrare ridicată a ratingurilor în zona pozitivă, între 4 și 5.
        - **Mustățile** se extind între **aproximativ 3.3 și 5.0**, ceea ce arată că majoritatea ratingurilor sunt concentrate în acest interval.
        - **Outlierii** sugerează că unele produse au primit recenzii foarte slabe, posibil din cauza calității scăzute sau a neconcordanței între așteptările clienților și realitatea produsului.

        🛍️ **Concluzie:**  
        Distribuția rating este puternic concentrată în zona înaltă (pozitivă), ceea ce sugerează o tendință generală de satisfacție din partea utilizatorilor Sephora. Totuși, prezența outlierilor sub 3 indică și existența unor produse cu recenzii negative.

        ---
        
        ### 📌 `price_usd` - Prețul produselor
        Acest boxplot arată distribuția prețurilor produselor Sephora.

        - **Mediana** este de aproximativ 35 USD, ceea ce înseamnă că jumătate dintre produse costă sub această valoare.
        - **IQR (Interquartile Range)** se întinde de la Q1 = 25 la Q3 = 58, indicând că majoritatea produselor au prețuri între 25 și 58 USD, o gamă accesibilă pentru produse de beauty mid-range.
        - **Mustățile** ating valori în jur de ~110–130 USD, sugerând că prețurile până în acest prag sunt considerate normale, în contextul distribuției.
        - **Outlierii** sunt evidențiați prin puncte izolate care ajung până la 1.900 USD, reprezentând produse de lux sau seturi speciale cu prețuri semnificativ mai mari decât media.

        🛍️ **Concluzie:**  
        Sephora oferă **produse pentru toate bugetele**, de la opțiuni accesibile până la articole premium extrem de scumpe.

        ---

        ### 📌 `child_count` - Numărul de variații ale produsului
        Acest boxplot analizează **câte variații** (dimensiuni, culori, arome) are fiecare produs.

        - **Mediana** este 0, ceea ce înseamnă că cel puțin 50% dintre produse nu au nicio variație disponibilă..
        - **IQR** (Interquartile Range) este de la Q1 = 0 la Q3 = 1, ceea ce sugerează că majoritatea produselor au 0 sau 1 variație, deci o diversitate foarte mică.
        - **Mustățile** se întind până în jurul valorii 10, ceea ce înseamnă că majoritatea produselor considerate normale au între 0 și 10 variații.
        - **Outlierii** sunt numeroși și urcă până la peste 100, indicând că unele produse au un număr excepțional de mare de opțiuni

        🛍️ **Concluzie:**  
        Majoritatea produselor Sephora au **puține variații**, dar unele articole, cum ar fi **paletele de farduri și parfumurile**, pot avea **foarte multe opțiuni**.

        ---

        🔍 **De ce sunt aceste boxplot-uri utile?**
        - Ne ajută să identificăm **produse neobișnuite** (ex. produse extrem de scumpe).
        - Permite detectarea **problemelor de calitate** (ex. produse cu rating scăzut).
        - Evidențiază trenduri și **strategie de prețuri** pentru produse noi.

        """)

    # --- Boxplot-uri pentru setul de date al recenziilor ---
    st.markdown("### 📝 Recenzii Produse - Detectarea Outliers")
    fig_reviews, axes_reviews = plt.subplots(1, len(numeric_cols_reviews), figsize=(18, 5))
    fig_reviews.suptitle("Boxplot pentru setul de date - Recenzii")

    for i, col in enumerate(numeric_cols_reviews):
        sns.boxplot(y=reviews_data[col], ax=axes_reviews[i], color="lightblue", medianprops={'color': 'red', 'ls': ':', 'lw': 5})
        axes_reviews[i].set_title(col)

    st.pyplot(fig_reviews)

    st.markdown("## 📊 Analiza detaliată a variabilelor")

    st.write("""
        ### 📌 `rating` - Scorul oferit de utilizatori produselor
        Acest boxplot arată distribuția ratingurilor acordate de utilizatori produselor.

        - **Mediana este în jur de 4.8**, ceea ce indică faptul că **majoritatea produselor primesc recenzii pozitive**.
        - **IQR-ul este între 4.5 și 5**, ceea ce înseamnă că **majoritatea utilizatorilor sunt foarte mulțumiți de produsele Sephora**.
        - **Mustățile ajung până la 3.0**, arătând că există și produse cu recenzii medii.
        - **Outlieri sunt putini, indică produse care au primit recenzii foarte slabe, sugerând **probleme de calitate, experiențe negative sau nepotrivire între așteptări și realitate**.

        🛍️ **Concluzie:**  
        Sephora are produse foarte apreciate, dar câteva produse primesc ratinguri scăzute, ceea ce poate indica **probleme de calitate** sau **experiențe negative** pentru anumite produse.

        ---
        ### 📌 `helpfulness` - Cât de utile sunt recenziile
        Variabila `helpfulness` măsoară **proporția voturilor pozitive primite de o recenzie** în comparație cu numărul total de voturi.

        #### 🔎 Interpretarea boxplot-ului:
        - **Mediana** este 0, iar valoarea maximă este 1.0.
        - **IQR** este mare: Q1 = 0, Q3 = 0.9, dar majoritatea valorilor sunt concentrate jos.
        - **Mustățile** ajung aproape de 1.0, dar valorile înalte sunt rare.
        - Nu există outlieri vizibili, dar distribuția este sever dezechilibrată.

        #### 🛍️ **Concluzie:**
        Cele mai multe recenzii nu sunt votate deloc sau nu sunt considerate utile. Doar un număr mic de recenzii ating scoruri mari de „helpfulness”, iar acestea sunt probabil cele mai detaliate sau bine argumentate.
        
        ---

        ### 📌 `total_feedback_count` - Numărul total de voturi pe recenzie
        Această variabilă arată cât de mult interacționează utilizatorii cu recenziile.

        - **Mediana** este 0, ceea ce indică faptul că cele mai multe recenzii nu primesc puține voturi.
        - **IQR**: Q1 = 0, Q3 = 3 → majoritatea recenziilor au sub 3 feedbackuri.
        - **Mustățile** urcă până la ~10–15.
        - **Outlierii** ajung la sute de voturi.

        🛍️ **Concluzie:**  
        Cele mai multe recenzii nu primesc multe voturi, dar unele produse primesc **recenzii virale**, ceea ce sugerează că sunt foarte discutate de comunitate.

        ---

        ### 📌 `total_neg_feedback_count` - Numărul de voturi negative
        Această variabilă arată câte voturi negative a primit o recenzie.

        - **Mediana** este 0, iar valoarea maximă este 465.
        - **IQR**: Q1 = 0, Q3 = 0 → deci peste 75% din recenzii nu au primit niciun vot negativ.
        - **Mustățile** sunt scurte, iar outlierii încep după 1.
        - **Outlierii** indică recenzii considerate nefolositoare sau greșite de comunitate.

        🛍️ **Concluzie:**  
        Cele mai multe recenzii sunt bine primite, dar unele sunt **puternic criticate** de utilizatori.

        ---

        ### 📌 `total_pos_feedback_count` - Numărul de voturi pozitive
        Această variabilă arată câte voturi pozitive a primit o recenzie.

        - **Mediana** este 0, iar valoarea maximă este 734.
        - **IQR**: Q1 = 0, Q3 = 2 → deci majoritatea recenziilor primesc sub 2 voturi pozitive.
        - **Mustățile** ajung până la 10–15, după care încep outlierii.
        - **Outlierii** sunt semnificativi și indică recenzii foarte apreciate.

        🛍️ **Concluzie:**  
        Asemănător cu feedbackul negativ, cel pozitiv este rareori oferit. Doar recenziile bine scrise, lungi sau cele care oferă insighturi reale sunt votate pozitiv în mod masiv.

        ---

        ### 📌 `price_usd` - Prețul produselor
        Acest boxplot arată distribuția prețurilor pentru produsele recenzate.

        - **Mediana** este sub 35 USD, ceea ce indică faptul că majoritatea produselor analizate sunt **produse accesibile**.
        - **IQR**: Q1 = 25, Q3 = 58 deci prețurile sunt moderate.
        - **Outlieri** care depășesc 400 USD indică faptul că există produse de lux sau seturi mari de produse.
        - **Mustățile arată că majoritatea produselor sunt sub 150 USD**, ceea ce confirmă că Sephora oferă produse accesibile pentru majoritatea consumatorilor.

        🛍️ **Concluzie:**  
        Produsele Sephora sunt variate ca preț, dar majoritatea recenziilor se referă la **produse accesibile**, în timp ce unele produse de lux sunt mai puțin discutate.

        ---
        """)

    # TRATARE OUTLIERS
    st.markdown("# 📊 Tratarea Outlierilor în `product_nan.csv`")

    st.write("""
        Outlierii pot influența semnificativ analizele, dar nu toate valorile extreme sunt erori.  
        În multe cazuri, aceste valori reprezintă **produse legitime**, cu caracteristici speciale care le fac să iasă în evidență.  

        Prin urmare, în loc să eliminăm aceste valori, alegem metode alternative de tratare, precum **transformarea logaritmică, winsorizarea și filtrarea condiționată**.  
        Acest lucru ne permite să păstrăm **integritatea datasetului**, fără a denatura distribuția variabilelor importante.
        """)

    df = pd.read_csv("dataset/product_nan.csv")

    # Transformare logaritmică pentru `loves_count`

    st.markdown("### 1️⃣ `loves_count` - Popularitatea produselor")
    st.write("""
        🔍 **Ce reprezintă această variabilă?**  
        - `loves_count` indică **numărul de utilizatori** care au marcat un produs ca favorit pe platforma Sephora.  
        - Unele produse devin **virale** sau sunt promovate agresiv, ceea ce generează valori extreme.

        ⚠ **Problema:**  
        - Distribuția este **extrem de asimetrică**, cu câteva produse care au sute de mii sau chiar milioane de aprecieri.  
        - Dacă folosim direct această variabilă, modelele de analiză vor fi **puternic influențate** de aceste extreme.  

        ✅ **Soluția:**  
        - Aplicăm transformarea **log(1 + x)** (`np.log1p()` în Python).  
        - Aceasta **reduce impactul** valorilor extreme, dar păstrează diferențele între produse populare și cele mai puțin cunoscute.

        ✅ **Decizie:**  
        - Păstrăm outlierii, dar aplicăm transformare logaritmică pentru a reduce impactul disproporționat al valorilor extreme.

        📌 **Motiv:**  
        - Produsele extrem de populare sunt **valide** și reflectă preferințele reale ale consumatorilor.  
        - Dacă am elimina aceste valori, am pierde **informații esențiale despre trenduri** și **produse virale**.  
        - Transformarea logaritmică **păstrează relațiile dintre produse**, dar reduce dezechilibrul dintre extreme.  
        """)

    df['loves_count'] = np.log1p(df['loves_count'])

    # Eliminarea produselor cu `loves_count` foarte mic pentru `rating`

    st.markdown("### 2️⃣ `rating` - Evaluarea produselor")
    st.write("""
        🔍 **Ce reprezintă această variabilă?**  
        - `rating` este scorul mediu oferit de utilizatori unui produs (între **1 și 5**).  
        - Un rating extrem (foarte mic sau foarte mare) poate fi **un indicator al calității**, dar și al **numărului redus de recenzii**.

        ⚠ **Problema:**  
        - Nu avem o coloană `reviews` (numărul de recenzii).  
        - Produsele cu **puține interacțiuni** (puține `loves_count`) pot avea ratinguri **înșelătoare**.

        ✅ **Soluția:**  
        - Folosim `loves_count` ca aproximare a popularității produsului.  
        - Eliminăm produsele cu `loves_count` mai mic de **10**, deoarece este puțin probabil să aibă ratinguri relevante.  
        - Această metodă asigură că includem doar produse **suficient apreciate**, evitând bias-ul generat de extreme.
        ✅ **Decizie:**  
        - Nu eliminăm produsele cu ratinguri extreme, dar aplicăm un filtru pe **loves_count** pentru a menține doar produsele relevante.

        📌 **Motiv:**  
        - Un rating mic **nu este o eroare**, ci poate indica un **produs de calitate slabă**.  
        - Produsele cu rating perfect (5.0) pot avea **foarte puține recenzii**, ceea ce le face **mai puțin reprezentative**.  
        - **În loc să eliminăm aceste produse**, am decis să păstrăm doar cele care au **un minim de loves_count**, presupunând că au primit **suficient feedback de la clienți**.  
        """)
    df = df[df['loves_count'] > np.log1p(10)]  # Transformăm și filtrăm după log

    # Winsorizare pentru `price_usd`**
    st.markdown("### 3️⃣ `price_usd` - Prețul produselor")
    st.write("""
        🔍 **Ce reprezintă această variabilă?**  
        - `price_usd` reflectă **prețul** produselor Sephora.  
        - Produsele pot varia de la câțiva dolari până la **mii de dolari** (ex: parfumuri exclusiviste, seturi de lux).

        ⚠ **Problema:**  
        - Unele produse **de lux** au prețuri extreme care pot **denatura analizele**.  
        - Dacă nu tratăm aceste valori, **media și devierea standard** vor fi puternic influențate.  

        ✅ **Soluția:**  
        - Aplicăm **winsorizare**: toate prețurile care depășesc **percentila 99%** sunt trunchiate la această limită.  
        - **De ce winsorizare și nu eliminare?**  
          - Pentru că **produsele de lux sunt valide**, dar vrem să prevenim efectul disproporționat asupra mediei.
        ✅ **Decizie:**  
        - Nu eliminăm produsele de lux, dar aplicăm **winsorizare**: trunchiem valorile peste **percentila 99%**.

        📌 **Motiv:**  
        - Produsele scumpe sunt **valide și importante** pentru analiza pieței de lux.  
        - Eliminarea lor ar **denatura realitatea prețurilor și gama de produse Sephora**.  
        - Winsorizarea ne permite să **controlăm efectul extremelor**, menținând totodată informația esențială despre produse.  
        """)
    upper_limit = df['price_usd'].quantile(0.99)
    df['price_usd'] = np.where(df['price_usd'] > upper_limit, upper_limit, df['price_usd'])

    # Transformare logaritmică pentru `child_count`

    st.markdown("### 4️⃣ `child_count` - Numărul de variații ale produsului")
    st.write("""
        🔍 **Ce reprezintă această variabilă?**  
        - `child_count` indică **numărul de variații** ale unui produs (ex: nuanțe de ruj, dimensiuni de parfum, opțiuni pentru ten).  

        ⚠ **Problema:**  
        - Anumite produse (ex: fonduri de ten) au **zeci sau sute de variații**, ceea ce creează outlieri.  
        - Dacă nu tratăm aceste valori, putem **supraestima complexitatea anumitor produse**.

        ✅ **Soluția:**  
        - Aplicăm transformarea **log(1 + x)** (`np.log1p()`), care:  
          - **Reduce impactul** produselor cu variații extreme.  
          - **Menține diferențele** între produsele cu 1-2 variații și cele cu 50+.  

        ✅ **Decizie:**  
        - Nu eliminăm aceste produse, dar aplicăm o **transformare logaritmică** pentru a echilibra distribuția.

        📌 **Motiv:**  
        - Produsele cu multe variații **nu sunt erori**, ci reflectă **diversitatea opțiunilor disponibile pentru clienți**.  
        - Transformarea logaritmică ne ajută să **păstrăm diferențele**, dar fără a denatura analiza.  
        """)
    df['child_count'] = np.log1p(df['child_count'])

    df.to_csv("dataset/clean_products_outliers.csv", index=False)

    st.markdown("### 📊 Compararea distribuțiilor după tratament")

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Distribuția variabilelor după transformare")

    cols = ['loves_count', 'rating', 'price_usd', 'child_count']
    titles = ['Loves Count', 'Rating', 'Price USD', 'Child Count']

    for i, col in enumerate(cols):
        row, col_idx = divmod(i, 2)
        sns.histplot(df[col], bins=30, kde=True, ax=axes[row, col_idx], color="pink")
        axes[row, col_idx].set_title(f"Distribuția {titles[i]} (după transformare)")

    st.pyplot(fig)

    # Tratare outliers reviews data

    st.markdown("# 📊 Tratarea Outlierilor în `reviews_nan.csv`")

    st.write("""
        Outlierii sunt valori extreme care pot influența analizele și modelele predictive, dar nu toate valorile extreme sunt erori.  
        În această secțiune, analizăm și aplicăm metode specifice pentru **`rating`, `helpfulness`, `total_feedback_count`, `total_neg_feedback_count`, `total_pos_feedback_count` și `price_usd`**.  

        ### 🔎 **De ce trebuie să tratăm outlierii?**  
        - Unele valori extreme pot distorsiona **media** și **distribuția** datelor.  
        - Outlierii pot **masca pattern-uri reale** din date.  
        - În loc să eliminăm datele, putem folosi **transformări sau winsorizare** pentru a păstra informațiile utile.  
        """)

    df = pd.read_csv("dataset/reviews_nan.csv")

    # Tratarea `rating`
    st.markdown("### 1️⃣ `rating` - Scorul oferit de utilizatori produselor")
    st.write("""
        🔍 **Problema:**  
        - `rating` este una dintre cele mai importante variabile pentru Sephora, deoarece reflectă experiența directă a utilizatorilor.  
        - Unele produse au **rating perfect (5.0)**, iar altele au **rating foarte mic (1.0)**.  
        - Dacă produsele cu ratinguri extreme au **doar 1-2 recenzii**, atunci ratingul lor nu este reprezentativ și poate induce în eroare analizele.  

        ✅ **Decizie:**  
        - **Nu eliminăm produsele cu ratinguri extreme**, deoarece un rating mic poate indica un produs slab, iar un rating mare poate indica un produs excelent.  
        - Aplicăm **filtrare pe `total_feedback_count`**, eliminând recenziile cu **mai puțin de 3 voturi totale**, deoarece aceste valori nu sunt suficient de relevante pentru a influența analiza.  

        📌 **Motiv:**  
        - Eliminarea ratingurilor extreme ar putea duce la **pierderea unor informații valoroase despre percepția reală a consumatorilor**.  
        - Filtrarea pe `total_feedback_count` asigură că produsele analizate au **suficient feedback pentru a fi relevante**, reducând bias-ul produselor cu puține voturi.  
        - Această metodă menține echilibrul între **păstrarea diversității produselor și eliminarea influenței distorsionate a ratingurilor izolate**.  
        """)
    df = df[df['total_feedback_count'] > 3]

    # 📌 **2️⃣ Tratarea `helpfulness`**
    st.markdown("### 2️⃣ `helpfulness` - Cât de utile sunt recenziile?")
    st.write("""
        🔍 **Problema:**  
        - `helpfulness` măsoară **cât de utile sunt recenziile** pentru utilizatori și poate influența semnificativ decizia de cumpărare.  
        - Unele recenzii au **helpfulness foarte scăzut (0.0)**, ceea ce înseamnă că utilizatorii fie le-au ignorat, fie nu le-au găsit utile.  
        - Există și recenzii cu `helpfulness` perfect (1.0), ceea ce poate însemna fie **o recenzie foarte detaliată și apreciată**, fie o distorsiune datorată numărului mic de voturi.  

        ✅ **Decizie:**  
        - **Nu eliminăm recenziile**, deoarece chiar și cele cu `helpfulness` mic pot conține informații utile pentru un subset de utilizatori.  
        - Aplicăm **winsorizare la percentila 1% și 99%** pentru a reduce impactul recenziilor extreme asupra distribuției generale.  

        📌 **Motiv:**  
        - Winsorizarea ne permite **să păstrăm recenziile valoroase**, dar fără influența disproporționată a extremelor.  
        - Dacă am elimina recenziile cu `helpfulness` mic, am putea **pierde feedback valoros** despre produse mai puțin populare, dar care ar putea fi relevante pentru anumite categorii de consumatori.  
        - Această metodă echilibrează analiza, păstrând **integritatea datelor** și reducând riscul unei analize părtinitoare.  
        """)
    df['helpfulness'] = df['helpfulness'].clip(lower=df['helpfulness'].quantile(0.01),
                                               upper=df['helpfulness'].quantile(0.99))

    # Tratarea `total_feedback_count`**
    st.markdown("### 3️⃣ `total_feedback_count` - Numărul total de voturi pe recenzie")
    st.write("""
        🔍 **Problema:**  
        - `total_feedback_count` arată cât de **interactivă** este o recenzie.  
        - Unele recenzii au **peste 800 de voturi**, ceea ce le face **mult mai influente** decât restul.  
        - Dacă nu limităm aceste extreme, analiza poate fi denaturată de un **număr mic de recenzii virale**, ceea ce ar putea duce la concluzii greșite.  

        ✅ **Decizie:**  
        - **Nu eliminăm recenziile**, deoarece interacțiunea ridicată poate fi un semnal al relevanței recenziei.  
        - Aplicăm **winsorizare la percentila 99%** pentru a limita impactul voturilor extreme.  

        📌 **Motiv:**  
        - Winsorizarea permite menținerea **recenziilor valoroase**, dar fără **influența disproporționată a celor virale**.  
        - Dacă am elimina recenziile cu multe voturi, am putea pierde informații critice despre produsele care generează **discuții intense**.  
        - Această metodă ne permite să **păstrăm insight-urile corecte**, fără a denatura structura generală a datelor.  
        """)
    upper_limit = df['total_feedback_count'].quantile(0.99)
    df['total_feedback_count'] = np.where(df['total_feedback_count'] > upper_limit, upper_limit,
                                          df['total_feedback_count'])

    # Tratarea `total_neg_feedback_count`**
    st.markdown("### 4️⃣ `total_neg_feedback_count` - Numărul de voturi negative")
    st.write("""
        🔍 **Problema:**  
        - Majoritatea recenziilor **nu au voturi negative**, dar câteva au **peste 300 de voturi negative**, ceea ce poate indica o recenzie extrem de controversată.  
        - Dacă lăsăm aceste valori neschimbate, recenziile negative extreme pot distorsiona analiza generală asupra satisfacției produselor.  

        ✅ **Decizie:**  
        - **Nu eliminăm recenziile**, deoarece feedback-ul negativ este valoros pentru identificarea **problemelor produselor**.  
        - Aplicăm **transformare logaritmică** pentru a reduce impactul disproporționat al voturilor negative extreme.  

        📌 **Motiv:**  
        - Transformarea logaritmică menține diferențele dintre recenzii, dar **echilibrează distribuția** și previne influența exagerată a unor valori extreme.  
        - Această metodă ajută la obținerea **unei perspective mai realiste** asupra impactului recenziilor negative.  
        """)
    df['total_neg_feedback_count'] = np.log1p(df['total_neg_feedback_count'])

    st.markdown(
        "## 🔍 De ce am aplicat **transformare logaritmică** și **winsorizare** pentru `total_pos_feedback_count` și `price_usd`?")

    st.write("""
        Nu toate variabilele cu valori extreme necesită eliminare prin **IQR**.  
        În cazul variabilelor `total_pos_feedback_count` (numărul de voturi pozitive pentru o recenzie) și `price_usd` (prețul produsului),  
        am decis să folosim **transformare logaritmică și winsorizare** pentru a păstra informațiile relevante, dar fără a distorsiona analiza.

        ---

        ### 📌 **1️⃣ `total_pos_feedback_count` - Numărul de voturi pozitive pentru o recenzie**  
        🔍 **Problema:**  
        - Această variabilă reflectă **gradul de apreciere a unei recenzii**, iar unele recenzii au un număr extrem de mare de voturi pozitive.  
        - Dacă aplicăm **IQR**, riscăm să eliminăm **recenziile extrem de valoroase**, care sunt esențiale pentru a înțelege **produsele foarte apreciate**.  

        ✅ **Decizie:**  
        - **Aplicăm transformare logaritmică** (`log(1+x)`) pentru a reduce dezechilibrul dintre recenziile cu puține voturi și cele extrem de populare.  

        📌 **Motiv:**  
        - Transformarea logaritmică reduce impactul disproporționat al **celor mai populare recenzii**, menținând însă informațiile relevante despre cât de apreciate sunt acestea.  
        - Fără această transformare, modelele de analiză ar putea **considera greșit că recenziile cu puține voturi sunt nesemnificative**, deși acestea pot conține informații valoroase.  
        - **Log-ul menține structura datelor**, dar echilibrează distribuția, permițând modelelor predictive să interpreteze mai bine relațiile dintre variabile.

        ---

        ### 📌 **2️⃣ `price_usd` - Prețul produselor**  
        🔍 **Problema:**  
        - Sephora vinde atât produse accesibile, cât și **produse de lux** care costă **peste 500 USD, 1000 USD sau chiar mai mult**.  
        - Dacă aplicăm **IQR**, am elimina **produsele premium**, care sunt **perfect legitime**, dar rare.  
        - Dacă lăsăm prețurile neschimbate, produsele extrem de scumpe ar influența excesiv **media** și **distribuția prețurilor**.

        ✅ **Decizie:**  
        - **Aplicăm winsorizare la percentila 99%** pentru a păstra prețurile produselor de lux, dar fără a lăsa aceste valori să denatureze statisticile generale.  

        📌 **Motiv:**  
        - **Winsorizarea este preferată în locul IQR**, deoarece **menține produsele premium** în analiză, dar previne ca acestea să **distorsioneze distribuția prețurilor**.  
        - Dacă am elimina aceste produse, **am trage concluzii greșite despre prețurile medii din Sephora**, ignorând segmentele de lux.  
        - Această metodă ne permite să păstrăm **toată gama de prețuri** fără a permite produselor ultra-scumpe să influențeze excesiv modelele predictive.

        ---

        ### 🔍 **Concluzie finală**  
        📌 **Transformarea logaritmică** a fost aplicată la `total_pos_feedback_count` pentru a **echilibra distribuția voturilor** și a menține informațiile despre recenziile valoroase.  
        📌 **Winsorizarea** a fost aplicată la `price_usd` pentru a **păstra produsele de lux**, dar fără ca acestea să influențeze statisticile generale.  
        📌 **Nu am folosit IQR**, deoarece aceste variabile **nu conțin erori**, ci reflectă caracteristici esențiale ale produselor și recenziilor.  

        Astfel, putem face **predicții mai precise** despre **ce produse sunt apreciate și cum se comportă utilizatorii pe platformă**.
        """)

    df['total_pos_feedback_count'] = np.log1p(df['total_pos_feedback_count'])

    upper_limit = df['price_usd'].quantile(0.99)  # Percentila 99%
    df['price_usd'] = np.where(df['price_usd'] > upper_limit, upper_limit, df['price_usd'])

    # Salvare fișier curățat
    df.to_csv("dataset/clean_reviews_outliers.csv", index=False)
    st.success("✅ Datele curățate au fost salvate în `clean_reviews_outliers.csv`.")

    st.markdown("### 📊 Compararea distribuțiilor după tratament")

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Distribuția variabilelor după transformare")

    # Variabilele pe care le vizualizam
    cols = ['rating', 'helpfulness', 'total_feedback_count', 'total_neg_feedback_count', 'price_usd',
            'total_pos_feedback_count']
    titles = ['Rating', 'Helpfulness', 'Total Feedback Count', 'Total Negative Feedback', 'Price USD',
              'Total Positive Feedback']

    # Plasare variabile în subploturi
    for i, col in enumerate(cols):
        row, col_idx = divmod(i, 3)
        sns.histplot(df[col], bins=30, kde=True, ax=axes[row, col_idx], color="lightblue")
        axes[row, col_idx].set_title(f"Distribuția {titles[i]} (după transformare)")

    st.pyplot(fig)

    # TRATARE IQR
    st.markdown("# 📊 Tratarea Outlierilor IQR in `reviews_nan.csv`")

    st.write("""
        Outlierii pot distorsiona analizele și trebuie tratați cu atenție.  
        În această secțiune, aplicăm metode precum:
        - **Winsorizare**
        - **Transformare logaritmică**
        - **Metoda IQR (Interquartile Range)**
        """)

    df = pd.read_csv("dataset/reviews_nan.csv")

    # **Metoda IQR pentru detectarea outlierilor**
    st.markdown("## 📊 Metoda IQR pentru Detectarea Outlierilor")
    st.write(""" 
        Interquartile Range (IQR) este o metodă statistică folosită pentru **detectarea valorilor extreme** într-un set de date.  
        IQR se calculează folosind **diferența dintre quartila 75% și quartila 25%**, iar outlierii sunt valorile care depășesc acest interval:

        🔢 **Formula IQR:**  
        \\[
        IQR = Q3 - Q1
        \\]

        📌 **Regulă pentru identificarea outlierilor:**  
        - **Outlier inferior**: Orice valoare **mai mică** decât \\( Q1 - 1.5 \cdot IQR \\)
        - **Outlier superior**: Orice valoare **mai mare** decât \\( Q3 + 1.5 \cdot IQR \\)

        Această metodă este utilă pentru **detectarea valorilor extreme**, dar **nu toate outlier-ele trebuie eliminate**.
        """)

    # Aplicare IQR pe `rating`**
    st.markdown("### 1️⃣ `rating` - Identificarea și tratarea outlierilor folosind IQR")
    Q1 = df['rating'].quantile(0.25)
    Q3 = df['rating'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_rating = df[(df['rating'] < lower_bound) | (df['rating'] > upper_bound)]

    st.write(f"""
        🔍 **Calcul IQR pentru `rating`**:
        - **Q1 (25%)**: {round(Q1, 2)}
        - **Q3 (75%)**: {round(Q3, 2)}
        - **IQR**: {round(IQR, 2)}
        - **Outlier inferior** (Q1 - 1.5 × IQR): {round(lower_bound, 2)}
        - **Outlier superior** (Q3 + 1.5 × IQR): {round(upper_bound, 2)}
        """)

    st.write(f"📌 **Numărul de outlieri în `rating` detectați prin IQR**: {len(outliers_rating)}")

    # Aplicare Winsorizare (trunchiere la limitele IQR)
    df['rating'] = np.where(df['rating'] < lower_bound, lower_bound, df['rating'])
    df['rating'] = np.where(df['rating'] > upper_bound, upper_bound, df['rating'])

    st.write("""
        ✅ **Decizie**:
        - **Nu eliminăm recenziile extreme**, ci aplicăm **trunchierea la limitele IQR** pentru a reduce impactul valorilor extreme.
        - Această metodă ajută la **normalizarea distribuției** fără a pierde informații valoroase.
        """)

    # Aplicare IQR pe `total_feedback_count`**
    st.markdown("### 2️⃣ `total_feedback_count` - Identificarea și tratarea outlierilor")
    Q1 = df['total_feedback_count'].quantile(0.25)
    Q3 = df['total_feedback_count'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_feedback = df[(df['total_feedback_count'] < lower_bound) | (df['total_feedback_count'] > upper_bound)]

    st.write(f"""
        🔍 **Calcul IQR pentru `total_feedback_count`**:
        - **Q1 (25%)**: {round(Q1, 2)}
        - **Q3 (75%)**: {round(Q3, 2)}
        - **IQR**: {round(IQR, 2)}
        - **Outlier inferior** (Q1 - 1.5 × IQR): {round(lower_bound, 2)}
        - **Outlier superior** (Q3 + 1.5 × IQR): {round(upper_bound, 2)}
        """)

    st.write(f"📌 **Numărul de outlieri în `total_feedback_count` detectați prin IQR**: {len(outliers_feedback)}")

    # Winsorizare pentru `total_feedback_count`
    df['total_feedback_count'] = np.where(df['total_feedback_count'] > upper_bound, upper_bound,
                                          df['total_feedback_count'])

    st.write("""
        ✅ **Decizie**:
        - **Nu eliminăm recenziile cu multe voturi**, dar trunchiem valorile extreme pentru a **reduce impactul disproporționat** asupra distribuției.
        - Această metodă ajută la **menținerea echilibrului între recenziile populare și cele mai puțin vizibile**.
        """)

    st.markdown("## 🔍 De ce nu am aplicat IQR pe toate variabilele?")

    st.write("""
        Metoda IQR (Interquartile Range) este foarte utilă pentru detectarea valorilor extreme, dar nu toate variabilele beneficiază de această tehnică.  
        Unele outlieri sunt **valori legitime** care oferă informații importante despre produse și recenzii.  

        ### ❌ **Variabile pe care NU am aplicat IQR**  
        1️⃣ **`total_neg_feedback_count` și `total_pos_feedback_count`**  
           - Aceste variabile sunt **puternic corelate** cu `total_feedback_count`.  
           - Aplicarea IQR separat pe ele ar putea elimina **recenzii populare**, ceea ce ar distorsiona analiza.  
           - **Decizie:** Am aplicat IQR doar pe `total_feedback_count`, controlând astfel impactul asupra celorlalte variabile.

        2️⃣ **`helpfulness`**  
           - Aceasta este o **proporție** (între 0 și 1), iar extremele sunt **valori naturale**.  
           - De exemplu, o recenzie cu **100% voturi pozitive** (`helpfulness = 1.0`) nu este un outlier, ci indică un feedback puternic pozitiv.  
           - **Decizie:** Am păstrat toate valorile, fără ajustare.

        📌 **Concluzie:**  
        Aplicarea **IQR pe toate variabilele ar fi putut duce la pierderea de informații importante**.  
        În schimb, am aplicat IQR **doar pe variabilele care distorsionau analiza (`rating` și `total_feedback_count`)**, păstrând echilibrul între curățarea datelor și menținerea semnificației lor.  
        """)

    df.to_csv("dataset/clean_reviews_outliers_iqr.csv", index=False)

    st.markdown("### 📊 Compararea distribuțiilor după tratament")

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Distribuția variabilelor după aplicarea IQR")

    cols = ['rating', 'total_feedback_count', 'total_neg_feedback_count', 'total_pos_feedback_count']
    titles = ['Rating', 'Total Feedback Count', 'Total Negative Feedback', 'Total Positive Feedback']

    for i, col in enumerate(cols):
        row, col_idx = divmod(i, 2)
        sns.histplot(df[col], bins=30, kde=True, ax=axes[row, col_idx], color="lightblue")
        axes[row, col_idx].set_title(f"Distribuția {titles[i]} (după IQR)")

    st.pyplot(fig)

    st.markdown("# 🔍 Alegerea metodei pentru analiza viitoare")

    st.write("""
        Scopul principal al analizei este să înțelegem **ce factori influențează popularitatea unui produs** și să dezvoltăm un model de predicție care să determine dacă un produs nou va fi apreciat de utilizatori.  

        Pentru a face acest lucru, trebuie să păstrăm cât mai multe informații relevante, inclusiv produsele extrem de populare sau cele cu multe recenzii, deoarece acestea conțin **semnale puternice despre preferințele consumatorilor**.  
        """)

    st.markdown("### 📊 Compararea metodelor de tratare a outlierilor")

    st.markdown("""
        După analizarea celor două metode (transformare logaritmică vs. eliminarea outlierilor prin IQR), am decis să folosim **fișierul obținut prin transformarea logaritmică**.  

        #### **Motivele alegerii acestei metode:**  
        - **Menține toate produsele în analiză**, inclusiv cele extrem de populare, care sunt **esențiale pentru predicție**.  
        - **Reduce impactul outlierilor**, permițând modelelor de machine learning să funcționeze mai bine.  
        - **Păstrează relațiile relative între produse**, ceea ce ajută la înțelegerea tendințelor consumatorilor.  
        - **Nu elimină informații valoroase**, evitând pierderea de date relevante despre produsele premium sau cele foarte apreciate.  
 
        Pentru a continua analiza și a dezvolta modele de predicție despre succesul unui produs pe Sephora, **vom folosi fișierul curățat prin transformare logaritmică**.
         """)
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily

def show_geopandas():
    st.title("Explorare spațială cu GeoPandas pe districtele Barcelonei")
    st.markdown("""
    **Notă:** Nu am putut folosi setul de date Sephora pentru analize spațiale, deoarece nu conține informații geografice.  
    Pentru această secțiune, am ales un set de date public cu limitele administrative ale districtelor orașului Barcelona, potrivit pentru demonstrații cu GeoPandas.

    **Despre setul de date:**  
    Setul conține poligoane pentru fiecare district din Barcelona, cu denumire și geometrie. Permite calcule de arie, distanțe, centroid, overlay și plotări avansate.
    """)

    st.subheader("1. Încărcare și reproiectare la CRS metric")
    st.write(
        "Încărcăm limitele districtelor din Barcelona și reproiectăm la un sistem de coordonate metric (EPSG:3857) pentru calcule corecte de arie și distanță.")
    url = 'https://raw.githubusercontent.com/jcanalesluna/bcn-geodata/master/districtes/districtes.geojson'
    districts = gpd.read_file(url).to_crs(epsg=3857)
    st.dataframe(districts.head())

    st.subheader("2. Calcul arie, centroid și boundary")
    st.write(
        "Calculăm aria fiecărui district (km²), centrul geometric (centroid) și extragem boundary-ul (conturul) fiecărui poligon.")
    districts['area_km2'] = districts.area / 1e6
    districts['centroid'] = districts.centroid
    districts['boundary'] = districts.boundary
    st.dataframe(districts[['NOM', 'area_km2', 'centroid']])

    st.subheader("3. Hartă tematică: aria districtelor")
    st.write("Afișăm harta districtelor colorată în funcție de aria fiecăruia (km²).")
    fig, ax = plt.subplots(figsize=(8, 8))
    districts.plot(ax=ax, edgecolor='black', column='area_km2', legend=True, cmap='Blues')
    plt.title('Arii districte Barcelona (km²)')
    st.pyplot(fig)

    st.subheader("4. Top 3 districte după arie")
    st.write("Afișăm cele mai mari 3 districte ca suprafață.")
    top3 = districts.nlargest(3, 'area_km2')
    st.dataframe(top3[['NOM', 'area_km2']])

    st.subheader("5. Districte sub media ariei")
    media_arie = districts['area_km2'].mean()
    st.write(f"Media ariei districtelor este {media_arie:.2f} km². Districtele sub această medie sunt:")
    sub_medie = districts[districts['area_km2'] < media_arie]
    st.dataframe(sub_medie[['NOM', 'area_km2']])

    st.subheader("6. Plotare boundary-uri (contururi) și centroiduri")
    st.write("Afișăm doar contururile districtelor și marcăm centroidurile cu roșu.")
    fig, ax = plt.subplots(figsize=(8, 8))
    districts['boundary'].plot(ax=ax, color='orange')
    districts['centroid'].plot(ax=ax, color='red', marker='x')
    plt.title('Boundary-uri și centroiduri districte Barcelona')
    st.pyplot(fig)

    st.subheader("7. Suma și media ariei tuturor districtelor")
    st.write("Calculăm suma și media ariei pentru toate districtele.")
    st.write(f"Suma ariei: {districts['area_km2'].sum():.2f} km²")
    st.write(f"Media ariei: {districts['area_km2'].mean():.2f} km²")

    st.subheader("8. Spatial join: muzee fictive")
    st.write("Simulăm trei muzee și vedem în ce district se află fiecare, folosind spatial join.")
    points = gpd.GeoDataFrame({
        'name': ['Muzeu 1', 'Muzeu 2', 'Muzeu 3'],
        'geometry': [Point(2.17, 41.38), Point(2.14, 41.40), Point(2.12, 41.36)]
    }, crs='EPSG:4326').to_crs(epsg=3857)
    joined = gpd.sjoin(points, districts, how='left', predicate='within')
    st.dataframe(joined[['name', 'NOM']])

    st.subheader("9. Distanța la Sagrada Familia")
    st.write("Calculăm distanța (km) de la centroidul fiecărui district la Sagrada Familia.")
    sagrada_fam = Point(2.1743680500855005, 41.403656946781304)
    sagrada_fam_gs = gpd.GeoSeries([sagrada_fam], crs=4326).to_crs(epsg=3857)
    districts['dist_sagrada_km'] = districts['centroid'].distance(sagrada_fam_gs[0]) / 1000
    st.dataframe(districts[['NOM', 'dist_sagrada_km']].sort_values('dist_sagrada_km'))

    st.subheader("10. Hartă: distanța la Sagrada Familia")
    st.write(
        "Colorăm harta districtelor în funcție de distanța la Sagrada Familia și marcăm locația acesteia cu o stea roșie.")
    fig, ax = plt.subplots(figsize=(10, 8))
    districts.plot(ax=ax, column='dist_sagrada_km', legend=True, cmap='viridis', edgecolor='black')
    sagrada_fam_gs.plot(ax=ax, color='red', marker='*', markersize=200, label='Sagrada Familia')
    plt.legend()
    plt.title('Distanța la Sagrada Familia (km)')
    st.pyplot(fig)

    st.subheader("11. Spatial join invers: puncte în afara districtelor")
    st.write(
        "Demonstrăm spatial join invers: generăm puncte, unele în oraș, altele în afara orașului, și vedem care nu aparțin niciunui district.")
    test_points = gpd.GeoDataFrame({
        'name': ['In Barcelona', 'Tot in Barcelona', 'În afara orașului'],
        'geometry': [Point(2.17, 41.38), Point(2.14, 41.40), Point(2.00, 41.60)]
    }, crs='EPSG:4326').to_crs(epsg=3857)
    joined = gpd.sjoin(test_points, districts, how='left', predicate='within')
    outside = joined[joined['index_right'].isna()]
    st.dataframe(outside[['name', 'geometry']])

    st.subheader("12. Hartă cu fundal real și centroiduri")
    st.write("Afișăm districtele colorate, centroidurile cu verde și o hartă reală de fundal (OpenStreetMap).")
    fig, ax = plt.subplots(figsize=(12, 8))
    districts.plot(column='NOM', ax=ax, alpha=0.5, legend=True, edgecolor='black')
    districts["centroid"].plot(ax=ax, color="green", markersize=30, label='Centroid')
    contextily.add_basemap(ax, crs=districts.crs.to_string())
    plt.title('Districtele Barcelonei cu centroiduri și hartă de fundal')
    plt.axis('off')
    plt.legend()
    st.pyplot(fig)

    st.subheader("13. Overlay: zone de parc simulate")
    st.write(
        "Simulăm parcuri circulare cu rază de 500m în jurul fiecărui centroid și afișăm doar zonele de district acoperite de aceste 'parcuri'.")
    parks = gpd.GeoDataFrame(geometry=districts['centroid'].buffer(500), crs=districts.crs)
    parks_intersection = districts.overlay(parks, how='intersection')
    fig, ax = plt.subplots(figsize=(12, 8))
    parks_intersection.plot(ax=ax, alpha=0.5, edgecolor='black', color='forestgreen')
    districts.boundary.plot(ax=ax, color='black', linewidth=0.8)
    plt.title('Zone de parc simulate (500m în jurul centroidului) în districtele Barcelonei')
    plt.axis('off')
    st.pyplot(fig)

    st.subheader("14. Districte fără zonele ocupate de parcurile simulate")
    st.write("Afișăm zonele de district rămase după excluderea parcurilor simulate.")
    parks_difference = districts.overlay(parks, how='difference')
    fig, ax = plt.subplots(figsize=(12, 8))
    parks_difference.plot(ax=ax, alpha=0.7, edgecolor='black', column='NOM', legend=True)
    plt.title('Districte fără zonele ocupate de parcurile simulate')
    plt.axis('off')
    st.pyplot(fig)
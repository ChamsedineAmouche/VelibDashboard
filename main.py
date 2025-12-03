import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Vélib IDF",
    page_icon="🚲",
    layout="wide"
)

def main():
    st.title("🚲 Analyse des Vélib' en Île-de-France")
    
    st.markdown("""
    Ce dashboard permet de visualiser les stations Vélib' en Île-de-France.
    **Source des données :** Open Data Île-de-France.
    """)

    # --- ÉTAPE 1 : CHARGEMENT DES DONNÉES ---
    # Nous le ferons à l'étape suivante, pour l'instant on affiche la carte vide
    
    # --- ÉTAPE 2 : AFFICHAGE DE LA CARTE (Leaflet via Folium) ---
    st.subheader("Carte de l'Île-de-France")
    
    # Coordonnées de Paris (centre de l'IDF)
    coords_idf = [48.8566, 2.3522]
    
    # Création de la carte
    m = folium.Map(location=coords_idf, zoom_start=11, tiles="OpenStreetMap")
    
    # Affichage dans Streamlit
    st_folium(m, width=1200, height=600)

if __name__ == "__main__":
    main()
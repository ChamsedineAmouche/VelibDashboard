import streamlit as st
import pandas as pd
import folium
import pydeck as pdk
from streamlit_folium import st_folium
from data.raw.get_data import get_data
from data.cleaned.clean_data import clean_data
from folium.plugins import MarkerCluster

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Vélib IDF",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data(ttl=300)  # données rafraîchies toutes les 5 minutes (CACHE INTELLIGENT avec TTL)
def load_raw_data():
    return get_data()

def main():
    st.title("🚲 Analyse des Vélib' en Île-de-France")
    
    st.markdown("""
    Ce dashboard permet de visualiser les stations Vélib' en Île-de-France.
    **Source des données :** Open Data Île-de-France.
    """)

    # --- ÉTAPE 1 : CHARGEMENT DES DONNÉES ---
    raw = load_raw_data()
    df = clean_data(raw)
    
    # --- ÉTAPE 2 : AFFICHAGE DE LA CARTE (Leaflet via Folium) ---
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position='[lon, lat]',
        get_radius=30,
        get_fill_color=[0, 0, 128],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=11,
        bearing=0,
        pitch=0,
    )

    tooltip = {
        "html": """
        <b>{nom_station}</b><br>
        <b>Commune :</b> {commune}<br>
        <b>Capacité :</b> {capacite_totale}<br>
        <b>Vélos dispo :</b> {velos_disponibles}<br>
        <b>Électriques :</b> {velos_electriques}<br>
        <b>Mécaniques :</b> {velos_mecaniques}<br>
        <b>Bornes libres :</b> {bornes_disponibles}<br>
        <b>Taux dispo :</b> {taux_dispo:.0%}<br>
        """,
        "style": {
            "backgroundColor": "rgba(30, 30, 30, 0.8)",
            "color": "white"
        }
    }

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="road",
    ))

if __name__ == "__main__":
    main()
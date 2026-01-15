import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt
from data.raw.get_data import get_data
from data.cleaned.clean_data import clean_data

# Configuration de la page
st.set_page_config(
    page_title="Projet Vélib Mamadou",
    page_icon="🚲",
    layout="wide"
)

# ---------------------------------------------------------
# 1. CHARGEMENT ET PRÉPARATION DES DONNÉES (CACHE)
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def charger_donnees():
    raw = get_data()
    df = clean_data(raw)
    
    # ... (tes calculs de couleur et radius existants) ...
    def definir_couleur(taux):
        if taux < 0.10: return [255, 0, 0, 160]
        elif taux < 0.30: return [255, 165, 0, 160]
        else: return [0, 128, 0, 160]
    df['color'] = df['taux_dispo'].apply(definir_couleur)
    df['radius'] = df['capacite_totale'] * 2

    # ... (ton calcul de message existant) ...
    def definir_message(taux):
        if taux < 0.10: return "🔴 Critique"
        elif taux < 0.30: return "🟠 Faible"
        else: return "🟢 Bon"
    df['message_taux'] = df['taux_dispo'].apply(definir_message)

    # --- CORRECTION ICI ---
    # On crée une colonne de texte pur pour l'affichage (ex: "67%")
    # Comme ça, Pydeck n'a qu'à afficher le texte sans réfléchir
    df['taux_str'] = df['taux_dispo'].apply(lambda x: f"{x:.0%}")
    
    return df

# ---------------------------------------------------------
# 2. FONCTION PRINCIPALE
# ---------------------------------------------------------
def main():
    
    # Chargement avec spinner
    with st.spinner('Chargement des données Vélib...'):
        try:
            df = charger_donnees()
        except Exception as e:
            st.error(f"Erreur de chargement : {e}")
            return

    # --- SIDEBAR (FILTRES) ---
    st.sidebar.title("Filtres")
    st.sidebar.write("Dashboard de **Mamadou et Chamsedine**")
    
    # Filtre Communes
    liste_communes = sorted(df['commune'].unique())
    choix_communes = st.sidebar.multiselect("Filtrer par Communes :", liste_communes)
    
    if choix_communes:
        df_filtered = df[df['commune'].isin(choix_communes)]
    else:
        df_filtered = df

    st.sidebar.info(f"{len(df_filtered)} stations sélectionnées")

    # --- TITRE & KPIS ---
    st.title("🚲 Analyse Vélib Île-de-France")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Stations", len(df_filtered))
    kpi2.metric("Vélos Dispo", df_filtered['velos_disponibles'].sum())
    kpi3.metric("Électriques ⚡", df_filtered['velos_electriques'].sum())
    # Affichage propre du pourcentage moyen
    kpi4.metric("Taux Remplissage", f"{df_filtered['taux_dispo'].mean():.1%}")

    st.markdown("---")

    # --- SECTION A : CARTE INTERACTIVE (PYDECK) ---
    st.subheader("📍 Carte des stations")

    # Centrage automatique de la vue
    if not df_filtered.empty:
        view_state = pdk.ViewState(
            latitude=df_filtered["lat"].mean(),
            longitude=df_filtered["lon"].mean(),
            zoom=12,
            pitch=40,
        )
    else:
        view_state = pdk.ViewState(latitude=48.85, longitude=2.35, zoom=11)

    # Configuration de la couche de points
    layer = pdk.Layer(
        "ScatterplotLayer",
        df_filtered,
        get_position='[lon, lat]',
        get_radius='radius',      # Utilise la colonne calculée
        get_fill_color='color',   # Utilise la colonne calculée
        pickable=True,
        opacity=0.8,
        stroked=True,
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1
    )

    tooltip = {
        "html": """
        <div style='font-family: sans-serif;'>
            <b>{nom_station}</b><br>
            <span style='color: #ccc; font-size: 0.9em;'>{commune}</span>
            <hr style='margin: 5px 0; border: 1px solid #555;'>
            
            <b>🚲 Vélos dispo :</b> {velos_disponibles} sur {capacite_totale}<br>
            <br>
            ⚡ Électriques : {velos_electriques}<br>
            ⚙️ Mécaniques : {velos_mecaniques}<br>
            <br>
            <b>Remplissage :</b> {taux_str} — {message_taux}
        </div>
        """,
        "style": {
            "backgroundColor": "rgba(20, 20, 20, 0.9)",
            "color": "white",
            "borderRadius": "8px",
            "padding": "12px",
            "boxShadow": "0 4px 6px rgba(0,0,0,0.3)"
        }
    }

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="light"
    ))

    # --- SECTION B : STATISTIQUES GLOBALES ---
    st.markdown("---")
    col_g1, col_g2 = st.columns([2, 1])

    with col_g1:
        st.subheader("📊 Top 15 Communes (Disponibilité)")
        # Histogramme simple
        chart_data = df_filtered.groupby('commune')['velos_disponibles'].mean().reset_index()
        chart_data = chart_data.sort_values(by='velos_disponibles', ascending=False).head(15)
        
        bar_chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('commune', sort='-y', title='Commune'),
            y=alt.Y('velos_disponibles', title='Moyenne vélos dispo'),
            color=alt.value('#3182bd'),
            tooltip=['commune', alt.Tooltip('velos_disponibles', format='.1f')]
        ).interactive()
        st.altair_chart(bar_chart, width="stretch")

    with col_g2:
        st.subheader("⚡ Répartition Élec / Méca")
        # Donut Chart
        total_elec = df_filtered['velos_electriques'].sum()
        total_meca = df_filtered['velos_mecaniques'].sum()
        
        pie_data = pd.DataFrame({
            'Type': ['Électriques', 'Mécaniques'],
            'Valeur': [total_elec, total_meca]
        })
        
        pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Valeur", type="quantitative"),
            color=alt.Color(field="Type", type="nominal", scale=alt.Scale(domain=['Électriques', 'Mécaniques'], range=['#1f77b4', '#aec7e8'])),
            tooltip=['Type', 'Valeur']
        )
        st.altair_chart(pie_chart, width="stretch")

    # --- SECTION C : ANALYSES DYNAMIQUES ---
    st.markdown("---")
    st.header("📈 Analyses Dynamiques")
    
    # 1. ANALYSE PAR TYPE (Radio Button)
    st.subheader("1. Comparaison par Type de Vélo")
    
    choix_type = st.radio(
        "Choisir le type de vélo à analyser :",
        ["Vélos Mécaniques ⚙️", "Vélos Électriques ⚡"],
        horizontal=True
    )

    if "Mécaniques" in choix_type:
        col_y = "velos_mecaniques"
        color_bar = "#aec7e8"
        title_y = "Total Vélos Mécaniques"
    else:
        col_y = "velos_electriques"
        color_bar = "#1f77b4"
        title_y = "Total Vélos Électriques"

    # Données : Somme par commune
    data_type = df_filtered.groupby('commune')[col_y].sum().reset_index().sort_values(by=col_y, ascending=False).head(20)

    chart_type = alt.Chart(data_type).mark_bar().encode(
        x=alt.X('commune', sort='-y', title="Commune"),
        y=alt.Y(col_y, title=title_y),
        color=alt.value(color_bar),
        tooltip=['commune', col_y]
    ).interactive()
    
    st.altair_chart(bar_chart, width="stretch")

    # 2. ANALYSE PAR CAPACITÉ (Slider)
    st.markdown("---")
    st.subheader("2. Filtrage par Capacité de la Station")
    st.write("Ce graphique montre la relation entre la taille de la station et sa disponibilité.")

    # Slider dynamique
    max_capa = int(df['capacite_totale'].max())
    seuil_capa = st.slider("Afficher stations avec capacité > :", 0, max_capa, 30)

    # Filtrage local
    df_capa = df_filtered[df_filtered['capacite_totale'] >= seuil_capa]

    st.caption(f"Stations correspondantes : {len(df_capa)}")

    # Scatter plot (Nuage de points)
    scatter_capa = alt.Chart(df_capa).mark_circle(size=60).encode(
        x=alt.X('capacite_totale', title='Capacité Totale'),
        y=alt.Y('velos_disponibles', title='Vélos Disponibles'),
        # On colore par commune, mais sans légende (trop chargée)
        color=alt.Color('commune', legend=None), 
        tooltip=['nom_station', 'commune', 'capacite_totale', 'velos_disponibles']
    ).properties(
        height=400
    ).interactive()

    st.altair_chart(scatter_capa, width="stretch")

if __name__ == "__main__":
    main()
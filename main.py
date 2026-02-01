import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt

from data.raw.get_data import get_data
from data.cleaned.clean_data import clean_data

# Configuration de la page
st.set_page_config(
    page_title="Projet Dashboard Vélib",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data(ttl=300)
def charger_donnees() -> pd.DataFrame:
    """
    Charge les données Vélib depuis l'API, applique le nettoyage, puis prépare
    des colonnes dérivées utiles à la visualisation (couleur, rayon, labels).

    Le résultat est mis en cache (TTL=300s) pour limiter les appels.

    Returns
    -------
    pd.DataFrame
        DataFrame prêt pour le dashboard (colonnes nettoyées + colonnes dérivées).
    """
    raw = get_data()
    df = clean_data(raw)
    
    def definir_couleur(taux):
        if taux < 0.10: return [255, 0, 0, 160]
        elif taux < 0.30: return [255, 165, 0, 160]
        else: return [0, 128, 0, 160]
        
    df['color'] = df['taux_dispo'].apply(definir_couleur)
    df['radius'] = df['capacite_totale'] * 2

    def definir_message(taux):
        if taux < 0.10: return "🔴 Critique"
        elif taux < 0.30: return "🟠 Faible"
        else: return "🟢 Bon"
        
    df['message_taux'] = df['taux_dispo'].apply(definir_message)
    df['taux_str'] = df['taux_dispo'].apply(lambda x: f"{x:.0%}")
    
    return df

def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """""
    Construit les filtres dans la barre latérale (ex : communes) et renvoie
    un DataFrame filtré selon la sélection de l'utilisateur.

    Args:
        df : pd.DataFrame
            Données complètes des stations.

    Returns:
        pd.DataFrame
            Sous-ensemble filtré des stations.
    """
    st.sidebar.title("Filtres")
    st.sidebar.write("Dashboard de **Mamadou et Chamsedine**")

    liste_communes = sorted(df["commune"].dropna().unique())
    choix_communes = st.sidebar.multiselect("Filtrer par Communes :", liste_communes)

    if choix_communes:
        df_filtered = df[df["commune"].isin(choix_communes)]
    else:
        df_filtered = df

    st.sidebar.info(f"{len(df_filtered)} stations sélectionnées")
    return df_filtered

def render_kpis(df_filtered: pd.DataFrame) -> None:
    """
    Affiche les indicateurs clés (KPIs) en haut du dashboard : nombre de stations,
    vélos disponibles, vélos électriques et taux moyen de disponibilité.

    Args:
        df_filtered : (pd.DataFrame)
            Données filtrées selon la sélection utilisateur.
    """
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("Stations", len(df_filtered))
    kpi2.metric("Vélos Dispo", int(df_filtered["velos_disponibles"].sum()))
    kpi3.metric("Électriques", int(df_filtered["velos_electriques"].sum()))

    mean_rate = df_filtered["taux_dispo"].mean() if not df_filtered.empty else 0
    kpi4.metric("Taux Remplissage", f"{mean_rate:.1%}")

def render_map(df_filtered: pd.DataFrame) -> None:
    """
    Affiche la carte interactive des stations via PyDeck.
    Les points sont colorés selon le taux de disponibilité et leur taille dépend
    de la capacité de la station.
    
    Args:
        df_filtered : pd.DataFrame
            Données filtrées à afficher sur la carte.
    """
    st.subheader("📍 Carte des stations")

    if df_filtered.empty:
        st.info("Aucune station à afficher avec les filtres actuels.")
        return

    view_state = pdk.ViewState(
        latitude=float(df_filtered["lat"].mean()),
        longitude=float(df_filtered["lon"].mean()),
        zoom=12,
        pitch=40,
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        df_filtered,
        get_position="[lon, lat]",
        get_radius="radius",
        get_fill_color="color",
        pickable=True,
        opacity=0.8,
        stroked=True,
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1,
    )

    tooltip = {
        "html": """
        <div style='font-family: sans-serif;'>
            <b>{nom_station}</b><br>
            <span style='color: #ccc; font-size: 0.9em;'>{commune}</span>
            <hr style='margin: 5px 0; border: 1px solid #555;'>
            <b>🚲 Vélos dispo :</b> {velos_disponibles} / {capacite_totale}<br><br>
            ⚡ Électriques : {velos_electriques}<br>
            ⚙️ Mécaniques : {velos_mecaniques}<br><br>
            <b>Remplissage :</b> {taux_str} — {message_taux}
        </div>
        """,
        "style": {
            "backgroundColor": "rgba(20, 20, 20, 0.9)",
            "color": "white",
            "borderRadius": "8px",
            "padding": "12px",
            "boxShadow": "0 4px 6px rgba(0,0,0,0.3)",
        },
    }

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style="light",
        )
    )

def render_global_stats(df_filtered: pd.DataFrame) -> None:
    """
    Affiche les statistiques globales :
    - Top communes par moyenne de vélos disponibles (bar chart)
    - Répartition vélos électriques vs mécaniques (donut chart)
    
    Args:
        df_filtered : pd.DataFrame
            Données filtrées utilisées pour les agrégations.
    """
    st.markdown("---")
    col_g1, col_g2 = st.columns([2, 1])

    with col_g1:
        st.subheader("📊 Top 15 Communes (Disponibilité)")
        chart_data = (
            df_filtered.groupby("commune")["velos_disponibles"]
            .mean()
            .reset_index()
            .sort_values(by="velos_disponibles", ascending=False)
            .head(15)
        )

        bar_chart = (
            alt.Chart(chart_data)
            .mark_bar()
            .encode(
                x=alt.X("commune", sort="-y", title="Commune"),
                y=alt.Y("velos_disponibles", title="Moyenne vélos dispo"),
                tooltip=["commune", alt.Tooltip("velos_disponibles", format=".1f")],
            )
            .interactive()
        )
        st.altair_chart(bar_chart, width="stretch")

    with col_g2:
        st.subheader("⚡ Répartition Élec / Méca")
        pie_data = pd.DataFrame(
            {
                "Type": ["Électriques", "Mécaniques"],
                "Valeur": [
                    int(df_filtered["velos_electriques"].sum()),
                    int(df_filtered["velos_mecaniques"].sum()),
                ],
            }
        )

        pie_chart = (
            alt.Chart(pie_data)
            .mark_arc(innerRadius=50)
            .encode(
                theta=alt.Theta("Valeur:Q"),
                color=alt.Color("Type:N"),
                tooltip=["Type", "Valeur"],
            )
        )
        st.altair_chart(pie_chart, width="stretch")

def render_dynamic_analysis(df_filtered: pd.DataFrame, df_all: pd.DataFrame) -> None:
    """
    Affiche des analyses interactives basées sur les filtres utilisateur :
    - Comparaison mécaniques vs électriques par commune
    - Filtrage par capacité (slider) + nuage de points capacité vs vélos dispo

    Args:
        df_filtered : pd.DataFrame
            Données filtrées (communes sélectionnées).
        df_all : pd.DataFrame
            Données complètes (utile pour calculer le max de capacité du slider).
    """
    st.markdown("---")
    st.header("📈 Analyses Dynamiques")

    st.subheader("1. Comparaison par Type de Vélo")
    choix_type = st.radio(
        "Choisir le type de vélo à analyser :",
        ["Vélos Mécaniques ⚙️", "Vélos Électriques ⚡"],
        horizontal=True,
    )

    if "Mécaniques" in choix_type:
        col_y = "velos_mecaniques"
        title_y = "Total Vélos Mécaniques"
    else:
        col_y = "velos_electriques"
        title_y = "Total Vélos Électriques"

    data_type = (
        df_filtered.groupby("commune")[col_y]
        .sum()
        .reset_index()
        .sort_values(by=col_y, ascending=False)
        .head(20)
    )

    chart_type = (
        alt.Chart(data_type)
        .mark_bar()
        .encode(
            x=alt.X("commune", sort="-y", title="Commune"),
            y=alt.Y(col_y, title=title_y),
            tooltip=["commune", col_y],
        )
        .interactive()
    )
    st.altair_chart(chart_type, width="stretch")

    st.markdown("---")
    st.subheader("2. Filtrage par Capacité de la Station")
    max_capa = int(df_all["capacite_totale"].max())
    seuil_capa = st.slider("Afficher stations avec capacité ≥ :", 0, max_capa, 30)

    df_capa = df_filtered[df_filtered["capacite_totale"] >= seuil_capa]
    st.caption(f"Stations correspondantes : {len(df_capa)}")

    scatter_capa = (
        alt.Chart(df_capa)
        .mark_circle(size=60)
        .encode(
            x=alt.X("capacite_totale", title="Capacité Totale"),
            y=alt.Y("velos_disponibles", title="Vélos Disponibles"),
            color=alt.Color("commune", legend=None),
            tooltip=["nom_station", "commune", "capacite_totale", "velos_disponibles"],
        )
        .properties(height=400)
        .interactive()
    )
    st.altair_chart(scatter_capa, width="stretch")

def render_histogram_velos(df_filtered: pd.DataFrame) -> None:
    """
    Affiche un histogramme représentant la distribution du nombre
    de vélos disponibles par station.
    
    Args:
        df : pd.DataFrame
            Données complètes des stations.
    """
    
    st.markdown("---")
    st.subheader("📐 Distribution du nombre de vélos disponibles par station")

    hist = (
        alt.Chart(df_filtered)
        .mark_bar()
        .encode(
            x=alt.X(
                "velos_disponibles:Q",
                bin=alt.Bin(step=1),
                axis=alt.Axis(
                    title="Nombre de vélos disponibles",
                    format="d"
                )
            ),
            y=alt.Y(
                "count():Q",
                title="Nombre de stations"
            ),
            tooltip=[
                alt.Tooltip("count():Q", title="Stations")
            ]
        )
        .properties(height=400)
    )

    st.altair_chart(hist, width="stretch")

def main() -> None:
    """
    Point d'entrée du dashboard Streamlit.
    Orchestration : chargement des données, filtres, KPIs, carte et graphiques.
    """
    st.title("🚲 Analyse Vélib Île-de-France")

    with st.spinner("Chargement des données Vélib..."):
        df = charger_donnees()

    df_filtered = sidebar_filters(df)

    render_kpis(df_filtered)
    st.markdown("---")

    render_map(df_filtered)
    render_histogram_velos(df_filtered)
    render_global_stats(df_filtered)
    render_dynamic_analysis(df_filtered, df)

if __name__ == "__main__":
    main()
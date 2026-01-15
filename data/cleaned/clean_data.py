import pandas as pd

def clean_data(raw):
    """Nettoie et prépare les données Vélib pour le dashboard."""
    df = pd.DataFrame(raw)

    if df.empty:
        print("Aucune donnée récupérée.")
        return df
    
    # Renommage des colonnes principales
    df = df.rename(columns={
        "stationcode": "code_station",
        "name": "nom_station",
        "capacity": "capacite_totale",
        "numdocksavailable": "bornes_disponibles",
        "numbikesavailable": "velos_disponibles",
        "mechanical": "velos_mecaniques",
        "ebike": "velos_electriques",
        "nom_arrondissement_communes": "commune",
        "code_insee_commune": "code_insee",
    })

    # Conversion des types (string en int)
    colonnes_int = [
        "capacite_totale",
        "bornes_disponibles",
        "velos_disponibles",
        "velos_mecaniques",
        "velos_electriques",
    ]

    for col in colonnes_int:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Supprimer les stations sans géolocalisation
    df = df.dropna(subset=["lat", "lon"])

    # Conversion latitudes/longitudes
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

    # Filtrer sur les stations actives
    df = df[df["is_installed"] == "OUI"]
    df = df[df["is_renting"] == "OUI"]

    # Colonne calculée : taux de remplissage
    df["taux_dispo"] = df["velos_disponibles"] / df["capacite_totale"]

    # Réorganisation
    df = df[[
        "code_station",
        "nom_station",
        "commune",
        "lat",
        "lon",
        "capacite_totale",
        "velos_disponibles",
        "velos_mecaniques",
        "velos_electriques",
        "bornes_disponibles",
        "taux_dispo"
    ]]

    print("Données Vélib nettoyées :", df.shape)
    return df
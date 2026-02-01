import urllib.request
import json
from typing import List, Dict, Any

# URL API
VELIB_API_URL = (
    "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/"
    "velib-disponibilite-en-temps-reel/records"
)

# Comme l'API ne renvoit que 100 résultats maximum il faut gérer la pagination
def fetch_page(offset: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Récupère une page de résultats depuis l'API Vélib.

    L'API étant limitée à 100 enregistrements par requête, cette fonction
    permet de récupérer une tranche de données via les paramètres offset/limit.

    Args:
        offset : int, optional
            Position de départ dans le jeu de données (pagination), par défaut 0.
        limit : int, optional
            Nombre maximum d'enregistrements à récupérer (max = 100), par défaut 100.

    Returns:
        list[dict]
            Liste de dictionnaires représentant les stations Vélib.
            Retourne une liste vide en cas d'erreur réseau.
    """
    
    url = f"{VELIB_API_URL}?limit={limit}&offset={offset}"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            raw = response.read()
            text = raw.decode("utf-8")
            data = json.loads(text)
            return data.get("results", [])
    except Exception as e:
        print("Erreur réseau :", e)
        return []

def get_data() -> List[Dict[str, Any]]:
    """
    Récupère l'ensemble des stations Vélib disponibles via pagination automatique.

    Cette fonction appelle l'API autant de fois que nécessaire afin de contourner
    la limite de 100 résultats par requête imposée par l'API Open Data.

    Returns:
        List[Dict[str, Any]]
            Liste complète des stations Vélib sous forme de dictionnaires,
            incluant les coordonnées géographiques (lat, lon) lorsque disponibles.
    """
    
    all_stations = []
    offset = 0
    limit = 100  # Maxmimum autorisé par l'API
    
    while True:
        results = fetch_page(offset=offset, limit=limit)

        if not results:
            break  # Plus de données → on s'arrête

        # Transformation des résultats
        for rec in results:
            fields = rec.copy()

            # Extraction latitude/longitude
            coords = fields.get("coordonnees_geo")
            if isinstance(coords, dict):
                fields["lon"] = coords.get("lon")
                fields["lat"] = coords.get("lat")

            all_stations.append(fields)

        # Passer à la page suivante
        offset += limit

    return all_stations
import urllib.request
import json

# URL API
VELIB_API_URL = (
    "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/"
    "velib-disponibilite-en-temps-reel/records"
)

# Comme l'API ne renvoit que 100 résultats maximum il faut gérer la pagination
def fetch_page(offset=0, limit=100):
    """Récupère une seule page de l’API via urllib."""
    
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

def get_data():
    """Récupère toutes les stations Vélib via pagination automatique."""
    
    all_stations = []
    offset = 0
    limit = 100  # Maxmimum autorisé par l'API
    
    while True:
        print(f"Récupération page offset={offset}...")

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

    print(f"{len(all_stations)} stations téléchargées au total")
    return all_stations
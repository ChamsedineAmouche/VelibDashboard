# 🚲 Dashboard Vélib’ – Analyse de la disponibilité des vélos en Île-de-France

## Auteurs
- **Chamsedine AMOUCHE**
- **Mamadou BA**

**Formation :** E3FI – Groupe 1l 
**Année universitaire :** 2025–2026

---

## Objectif du projet

L’objectif de ce projet est d’analyser et de visualiser la disponibilité des stations Vélib’ en Île-de-France à partir de données publiques accessibles en temps réel.

Le projet prend la forme d’un dashboard interactif permettant :
- de localiser les stations Vélib’ sur une carte
- d’évaluer leur niveau de remplissage
- de comparer la disponibilité entre communes
- d’explorer dynamiquement les données à l’aide de visualisations interactives.

---

## Guide utilisateur

### Prérequis
- Python **3.11 ou supérieur**
- Navigateur web

### Installation

```bash
git clone https://github.com/ChamsedineAmouche/VelibDashboard.git
cd VelibDashboard
pip install -r requirements.txt
```

### Lancement du Dashboard

```bash
python main.py
```

Pour accéder au dashboard il faut accéder à l'URL indiquée dans la console (http://172.20.10.2:8501 par défaut).

---

## Fonctionnalités

### Carte interactive

La carte permet de visualiser l’ensemble des stations Vélib’ d’Île-de-France (environ 1500 stations) sous forme de points géolocalisés.

Pour chaque station, l’utilisateur peut :
- Se repérer et naviguer (zoom/dézoom, déplacement) afin de cibler un quartier ou une commune.
- Cliquer / survoler une station pour afficher une infobulle détaillée contenant :
  - le **nom** de la station et la **commune**,
  - la **capacité totale**,
  - le **nombre de vélos disponibles**,
  - la **répartition mécanique / électrique**,
  - le **taux de remplissage** (calculé) et un indicateur textuel (ex : *Critique / Faible / Bon*).
- Lire une **couleur de disponibilité** (ex : rouge/orange/vert) basée sur le taux de remplissage.
- Observer une **taille de point** proportionnelle à la capacité (stations plus grandes = points plus visibles).

> Objectif : donner une lecture immédiate de la disponibilité des vélos à l’échelle régionale, tout en gardant une information détaillée station par station.

---

### KPI globaux (indicateurs clés)

En haut du dashboard, des KPI synthétisent l’état du réseau pour la sélection courante (toutes communes ou communes filtrées) :
- Nombre de stations affichées
- Total de vélos disponibles
- Total de vélos électriques
- Taux de remplissage moyen (moyenne des taux calculés)

> Objectif : fournir une vue rapide de la disponibilité sur la zone étudiée.

---

### Histogrammes et graphiques interactifs

Le dashboard propose plusieurs visualisations pour analyser les données :

- Top communes (disponibilité moyenne) : classement des communes selon la moyenne de vélos disponibles.
- Répartition Électriques / Mécaniques : graphique en anneau (donut) montrant la composition du parc disponible.
- Comparaison par type de vélo : choix interactif (radio) pour afficher le total de vélos mécaniques ou électriques par commune.
- Analyse capacité ↔ disponibilité : nuage de points permettant d’explorer la relation entre la capacité d’une station et le nombre de vélos disponibles.
- Histogramme numérique (distribution) : représentation de la distribution d’une variable numérique (ex : nombre de vélos disponibles par station) :
  - **X** : valeur numérique (ex : 0, 1, 2, … vélos)
  - **Y** : nombre de stations ayant cette valeur


> Objectif : passer d’une lecture “localisée” (carte) à une lecture “statistique” (tendances globales).

---

### Filtres dynamiques

Un panneau latéral permet de filtrer dynamiquement l’affichage :
- Filtre par communes : l’utilisateur peut sélectionner une ou plusieurs communes.
- Tous les éléments (carte, KPI, graphiques) se mettent à jour automatiquement selon la sélection.
- Filtre par capacité (slider) : possibilité d’afficher uniquement les stations dont la capacité dépasse un seuil.

> Objectif : permettre une analyse ciblée par zone géographique ou par type de station.

---

### Données temps réel & rafraîchissement (cache)

Les données proviennent d’une API publique mise à jour régulièrement.  
Pour éviter de surcharger l’API et conserver un dashboard fluide, un mécanisme de cache est utilisé :
- Les données sont mises en cache côté Streamlit avec un TTL (ex : 5 minutes).
- Au-delà de ce délai, le dashboard récupère à nouveau les données et se met à jour.

> Objectif : concilier données dynamiques et performance.

---

## Données

- Source : Open Data Paris (https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records")
- API publique
- Environ 1500 stations
- Données géolocalisées

---

## Guide développeur

### Architecture du projet

```text
├── src/
│   ├── __init__.py
│   └── dashboard.py
├── data/
│   ├── raw/
│   │   ├── __init__.py
│   │   └── get_data.py
│   ├── cleaned/
│   │   ├── __init__.py
│   │   └── clean_data.py
│   └── __init__.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── README.md
├── main.py
```

---

## Qualité du code

- Linter / formateur : **Ruff**
- Code découpé, typé et documenté

Analyse du code : 

```bash
ruff check .
```

La majorité de nos erreurs ont pu être corrigés automatiquement grâce à cette comande :

```bash
ruff check . --fix
```

Pour le reste on a procédé à une correction manuelle.

---

## Rapport d’analyse

L’exploitation du dashboard Vélib’ permet de dégager plusieurs enseignements significatifs sur la répartition et la disponibilité des vélos en Île-de-France.

### 1. Réparation géographique des stations

La carte géolocalisée met clairement en évidence une forte concentration de stations dans Paris intra-muros, ainsi que dans les communes limitrophes proches (Boulogne-Billancourt, Issy-les-Moulineaux, Montreuil, Saint-Denis).
À l’inverse, les zones plus éloignées du centre parisien présentent une densité plus faible de stations, ce qui reflète une logique d’implantation prioritaire dans les zones à forte densité de population et à usage urbain intensif.

La couleur des points (rouge, orange, vert) montre également que certaines zones centrales connaissent ponctuellement des situations de tension (faible disponibilité), probablement liées à une forte demande.

### 2. Distribution du nombre de vélos disponibles par station

L’histogramme représentant la distribution du nombre de vélos disponibles par station révèle que :

- La majorité des stations disposent de peu à modérément de vélos (souvent entre 0 et 15 vélos).
- Les stations avec un très grand nombre de vélos disponibles sont rares et correspondent généralement à des stations de grande capacité.
- La distribution est asymétrique, avec une longue traîne, ce qui indique que quelques stations concentrent une capacité nettement supérieure à la moyenne.

Cette visualisation confirme que la disponibilité n’est pas homogène sur le réseau et dépend fortement de la taille et de la localisation de la station.

### 3. Répartition vélos mécaniques / électriques

Le graphique en anneau met en évidence une majorité de vélos mécaniques, les vélos électriques représentant une part significative mais minoritaire du parc disponible.
Cependant, l’analyse dynamique par type de vélo montre que Paris concentre la majorité des vélos électriques, ce qui peut s’expliquer par :

- une demande plus forte,
- une politique d’équipement prioritaire dans la capitale,
- ou une rotation plus rapide du parc électrique.

### 4. Analyse dynamique par type et par capacité

Les graphiques dynamiques permettent d’observer que :

- Paris domine largement en volume total de vélos (mécaniques comme électriques),
- Certaines communes présentent une meilleure disponibilité relative par station.
- Le filtrage par capacité met en évidence une relation positive entre la taille de la station et le nombre de vélos disponibles, sans pour autant garantir une disponibilité élevée en permanence.

Grâce à ce dashboard interactif, il est possible de passer d’une vision globale du réseau Vélib’ à une analyse fine par commune, type de vélo et capacité de station.
Les visualisations permettent non seulement d’identifier les zones bien couvertes, mais aussi de repérer les situations de tension ou de sous-utilisation, démontrant ainsi l’intérêt d’un outil de visualisation pour l’analyse de données urbaines en temps réel.

---

## Copyright

Projet pédagogique – ESIEE Paris – E3FI - 2026
Données Open Data Paris
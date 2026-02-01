# 🚲 Dashboard Vélib’ – Analyse de la disponibilité des vélos en Île-de-France

## Auteurs
- **Chamsedine AMOUCHE**
- **Mamadou BA**

**Formation :** E3FI – Groupe 1  
**Année universitaire :** 2025–2026

---

## 🎯 Objectif du projet

L’objectif de ce projet est d’analyser et de visualiser la **disponibilité des stations Vélib’ en Île-de-France** à partir de données publiques accessibles en temps réel.

Le projet prend la forme d’un **dashboard interactif** permettant :
- de localiser les stations Vélib’ sur une carte,
- d’évaluer leur niveau de remplissage,
- de comparer la disponibilité entre communes,
- d’explorer dynamiquement les données à l’aide de visualisations interactives.

---

## 🧭 Guide utilisateur

### Prérequis
- Python **3.11 ou supérieur**
- Connexion Internet
- Navigateur web moderne

### Installation

```bash
pip install -r requirements.txt
```

### Lancement

```bash
python main.py
```

---

## 🧩 Fonctionnalités

### 🗺️ Carte interactive (géolocalisation)

La carte permet de visualiser **l’ensemble des stations Vélib’** d’Île-de-France (environ 1500 stations) sous forme de points géolocalisés.

Pour chaque station, l’utilisateur peut :
- **Se repérer et naviguer** (zoom/dézoom, déplacement) afin de cibler un quartier ou une commune.
- **Cliquer / survoler** une station pour afficher une infobulle détaillée contenant :
  - le **nom** de la station et la **commune**,
  - la **capacité totale**,
  - le **nombre de vélos disponibles**,
  - la **répartition mécanique / électrique**,
  - le **taux de remplissage** (calculé) et un indicateur textuel (ex : *Critique / Faible / Bon*).
- Lire une **couleur de disponibilité** (ex : rouge/orange/vert) basée sur le taux de remplissage.
- Observer une **taille de point** proportionnelle à la capacité (stations plus grandes = points plus visibles).

> Objectif : donner une lecture immédiate de la disponibilité des vélos à l’échelle régionale, tout en gardant une information détaillée station par station.

---

### 📌 KPI globaux (indicateurs clés)

En haut du dashboard, des KPI synthétisent l’état du réseau pour la sélection courante (toutes communes ou communes filtrées) :
- **Nombre de stations** affichées
- **Total de vélos disponibles**
- **Total de vélos électriques**
- **Taux de remplissage moyen** (moyenne des taux calculés)

> Objectif : fournir une vue rapide “macro” de la disponibilité sur la zone étudiée.

---

### 📊 Histogrammes et graphiques interactifs

Le dashboard propose plusieurs visualisations pour analyser les données :

- **Top communes (disponibilité moyenne)** : classement des communes selon la moyenne de vélos disponibles.
- **Répartition Électriques / Mécaniques** : graphique en anneau (donut) montrant la composition du parc disponible.
- **Comparaison par type de vélo** : choix interactif (radio) pour afficher le total de vélos mécaniques ou électriques par commune.
- **Analyse capacité ↔ disponibilité** : nuage de points permettant d’explorer la relation entre la capacité d’une station et le nombre de vélos disponibles.
- **Histogramme numérique (distribution)** : représentation de la distribution d’une variable **numérique** (ex : nombre de vélos disponibles par station) :
  - **X** : valeur numérique (ex : 0, 1, 2, … vélos)
  - **Y** : nombre de stations ayant cette valeur

Les graphiques permettent l’exploration par survol (tooltips) et, selon le graphique, un comportement interactif (zoom/sélection).

> Objectif : passer d’une lecture “localisée” (carte) à une lecture “statistique” (tendances globales).

---

### 🎛️ Filtres dynamiques

Un panneau latéral permet de filtrer dynamiquement l’affichage :
- **Filtre par communes** : l’utilisateur peut sélectionner une ou plusieurs communes.
- Tous les éléments (carte, KPI, graphiques) se mettent à jour automatiquement selon la sélection.
- **Filtre par capacité** (slider) : possibilité d’afficher uniquement les stations dont la capacité dépasse un seuil.

> Objectif : permettre une analyse ciblée par zone géographique ou par type de station.

---

### 🔄 Données temps réel & rafraîchissement (cache)

Les données proviennent d’une **API publique** mise à jour régulièrement.  
Pour éviter de surcharger l’API et conserver un dashboard fluide, un mécanisme de cache est utilisé :
- Les données sont mises en cache côté Streamlit avec un **TTL** (ex : 5 minutes).
- Au-delà de ce délai, le dashboard récupère à nouveau les données et se met à jour.

> Objectif : concilier **données dynamiques** et **performance**.

---

## 🗄️ Données

- Source : Open Data Paris
- API publique
- ~1500 stations
- Données géolocalisées
- Accès reproductible

---

## 🧑‍💻 Guide développeur

### Arborescence

```text
├── main.py
├── src/dashboard.py
├── data/raw/get_data.py
├── data/cleaned/clean_data.py
├── requirements.txt
├── pyproject.toml
```

---

## 🧹 Qualité du code

- Linter / formateur : **Ruff**
- Code découpé, typé et documenté

---

## 📊 Rapport d’analyse

- Analyse de la disponibilité par commune
- Étude capacité ↔ vélos disponibles
- Répartition mécanique / électrique

---

## © Copyright

Projet pédagogique – ESIEE Paris – E3FI  
Données Open Data Paris

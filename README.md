# Unemployment Analysis with Python — CodeAlpha Task 2

> **CodeAlpha Data Science Internship**
> Intern : Moussa Guindo | ID : CA/DF1/100834

---

## Description

Ce projet analyse les **taux de chômage en Inde** en utilisant Python. L'objectif principal est d'explorer les tendances, d'identifier les régions les plus touchées et d'analyser l'impact du **Covid-19** sur le marché du travail.

---

## Technologies utilisées

| Outil | Usage |
|-------|-------|
| Python 3.13.9 | Langage principal |
| Pandas & NumPy | Nettoyage et manipulation des données |
| Matplotlib & Seaborn | Visualisation |
| KaggleHub | Téléchargement du dataset |

---

## Structure du projet

```
CodeAlpha_UnemploymentAnalysis/
│
├── unemployment_analysis.py      # Script principal
├── unemployment_overview.png     # Vue générale (4 graphiques)
├── unemployment_covid.png        # Impact Covid-19
├── unemployment_regional.png     # Heatmap + Boxplot régional
└── README.md
```

---

## Données utilisées

| Dataset | Lignes | Colonnes | Période |
|---------|--------|----------|---------|
| Unemployment in India.csv | 768 (740 après nettoyage) | 7 | 2019 → 2020 |
| Unemployment_Rate_upto_11_2020.csv | 267 | 9 | Jan → Nov 2020 |

---

## Analyses réalisées

- Évolution du taux de chômage dans le temps
- Top 10 états les plus touchés
- Distribution du taux de chômage
- **Impact du Covid-19** : comparaison avant/après Mars 2020
- Heatmap régionale par état et par mois
- Boxplot des états les plus affectés

---

## Insights clés

| # | Insight | Valeur |
|---|---------|--------|
| 1 | Taux de chômage moyen global | **11.79%** |
| 2 | Taux maximum enregistré | **76.74%** (pic Covid) |
| 3 | Taux minimum enregistré | **0.00%** |
| 4 | État le plus touché | **Tripura (28.35%)** |
| 5 | Taux moyen avant Covid | **9.23%** |
| 6 | Taux moyen après Covid | **12.96%** |
| 7 | Hausse due au Covid | **+3.73%** (+40% relatif) |

- Le Covid-19 a fait bondir le chômage de **9.23% à 12.96%** dès Mars 2020
- Certains états ont atteint des pics à **plus de 76%** pendant le confinement d'Avril 2020
- L'état le plus touché sur toute la période est **Tripura** avec 28.35% de moyenne
- Une corrélation négative existe entre la participation au marché du travail et le taux de chômage
- Le dataset contient **740 observations valides** après nettoyage (768 lignes initiales, 196 valeurs manquantes supprimées)

---

## Lancer le projet

```bash
# 1. Cloner le repo
git clone https://github.com/moussaguindo0909-boop/CodeAlpha_UnemploymentAnalysis.git
cd CodeAlpha_UnemploymentAnalysis

# 2. Installer les dépendances
pip install numpy pandas matplotlib seaborn kagglehub

# 3. Lancer le script
python unemployment_analysis.py
```
---

## Visualisations

### Chômage_covid
![Exploration](chômage_covid.png)

### Aperçu_du_chômage
![Matrice de confusion](aperçu_du_chômage.png)

### Chômage par régional
![Comparaison](chômage_régional.png)

---

---

## Auteur

**Moussa Guindo**
- Stage : CodeAlpha — Data Science
- ID : CA/DF1/100834
- Période : Juin 2026

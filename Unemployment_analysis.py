# ============================================================
# CodeAlpha Internship — Task 2: Unemployment Analysis
# Intern   : Moussa Guindo
# ID       : CA/DF1/100834
# Domain   : Data Science
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────
DATASET_PATH = r"C:\Users\mouss\.cache\kagglehub\datasets\gokulrajkmv\unemployment-in-india\versions\5"

FILE1 = os.path.join(DATASET_PATH, "Unemployment in India.csv")
FILE2 = os.path.join(DATASET_PATH, "Unemployment_Rate_upto_11_2020.csv")

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 130

# ─────────────────────────────────────────
# 1. CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────
print("=" * 60)
print("  CodeAlpha — Unemployment Analysis with Python")
print("=" * 60)

df1 = pd.read_csv(FILE1)
df2 = pd.read_csv(FILE2)

# Nettoyage des noms de colonnes (espaces)
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

print("\n Dataset 1 — Unemployment in India")
print(f"   Dimensions : {df1.shape[0]} lignes × {df1.shape[1]} colonnes")
print(df1.head(5))

print("\n Dataset 2 — Unemployment Rate upto 11/2020")
print(f"   Dimensions : {df2.shape[0]} lignes × {df2.shape[1]} colonnes")
print(df2.head(5))

# ─────────────────────────────────────────
# 2. NETTOYAGE DES DONNÉES
# ─────────────────────────────────────────
print("\n🧹 Nettoyage des données...")

# Renommer les colonnes pour simplifier
df1.rename(columns={
    "Region"                          : "State",
    "Date"                            : "Date",
    "Frequency"                       : "Frequency",
    "Estimated Unemployment Rate (%)" : "Unemployment_Rate",
    "Estimated Employed"              : "Employed",
    "Estimated Labour Participation Rate (%)" : "Labour_Participation"
}, inplace=True)

df2.rename(columns={
    "Region"                          : "State",
    "Date"                            : "Date",
    "Frequency"                       : "Frequency",
    "Estimated Unemployment Rate (%)" : "Unemployment_Rate",
    "Estimated Employed"              : "Employed",
    "Estimated Labour Participation Rate (%)" : "Labour_Participation",
    "longitude"                       : "Longitude",
    "latitude"                        : "Latitude",
    "Area"                            : "Area"
}, inplace=True)

# Convertir les dates
df1["Date"] = pd.to_datetime(df1["Date"].str.strip(), dayfirst=True)
df2["Date"] = pd.to_datetime(df2["Date"].str.strip(), dayfirst=True)

# Valeurs manquantes
print(f"\n   Valeurs manquantes df1 : {df1.isnull().sum().sum()}")
print(f"   Valeurs manquantes df2 : {df2.isnull().sum().sum()}")
df1.dropna(inplace=True)
df2.dropna(inplace=True)
print("    Nettoyage terminé")

# ─────────────────────────────────────────
# 3. STATISTIQUES DESCRIPTIVES
# ─────────────────────────────────────────
print("\n   Statistiques descriptives :")
print(df1[["Unemployment_Rate", "Employed", "Labour_Participation"]].describe().round(2))

# ─────────────────────────────────────────
# 4. VISUALISATION — VUE GÉNÉRALE
# ─────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.suptitle("Unemployment in India — Vue Générale", fontsize=16, fontweight="bold")

# 4.1 Évolution du taux de chômage dans le temps
df1_time = df1.groupby("Date")["Unemployment_Rate"].mean().reset_index()
axes[0, 0].plot(df1_time["Date"], df1_time["Unemployment_Rate"],
                color="#e74c3c", linewidth=2.5, marker="o", markersize=4)
axes[0, 0].set_title("Évolution du taux de chômage moyen")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Taux de chômage (%)")
axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45)

# 4.2 Top 10 états avec le taux de chômage le plus élevé
top10 = df1.groupby("State")["Unemployment_Rate"].mean().nlargest(10).reset_index()
axes[0, 1].barh(top10["State"], top10["Unemployment_Rate"],
                color=sns.color_palette("Reds_r", 10))
axes[0, 1].set_title("Top 10 États — Taux de chômage moyen")
axes[0, 1].set_xlabel("Taux de chômage (%)")

# 4.3 Distribution du taux de chômage
axes[1, 0].hist(df1["Unemployment_Rate"], bins=30,
                color="#3498db", edgecolor="white", alpha=0.8)
axes[1, 0].axvline(df1["Unemployment_Rate"].mean(), color="#e74c3c",
                   linestyle="--", linewidth=2, label=f"Moyenne : {df1['Unemployment_Rate'].mean():.1f}%")
axes[1, 0].set_title("Distribution du taux de chômage")
axes[1, 0].set_xlabel("Taux de chômage (%)")
axes[1, 0].set_ylabel("Fréquence")
axes[1, 0].legend()

# 4.4 Corrélation chômage vs participation au marché du travail
axes[1, 1].scatter(df1["Labour_Participation"], df1["Unemployment_Rate"],
                   alpha=0.5, color="#2ecc71", edgecolors="white", s=50)
axes[1, 1].set_title("Chômage vs Participation au marché du travail")
axes[1, 1].set_xlabel("Taux de participation (%)")
axes[1, 1].set_ylabel("Taux de chômage (%)")

plt.tight_layout()
plt.savefig("unemployment_overview.png", bbox_inches="tight")
plt.show()
print("\n   Graphique général sauvegardé : unemployment_overview.png")

# ─────────────────────────────────────────
# 5. ANALYSE COVID-19
# ─────────────────────────────────────────
print("\n   Analyse de l'impact du Covid-19...")

# Définir avant/après Covid (Mars 2020)
covid_start = pd.Timestamp("2020-03-01")
df2["Period"] = df2["Date"].apply(
    lambda x: "Après Covid (Mar-Nov 2020)" if x >= covid_start else "Avant Covid"
)

pre_covid  = df2[df2["Period"] == "Avant Covid"]["Unemployment_Rate"].mean()
post_covid = df2[df2["Period"] == "Après Covid (Mar-Nov 2020)"]["Unemployment_Rate"].mean()

print(f"   Taux moyen AVANT Covid : {pre_covid:.2f}%")
print(f"   Taux moyen APRÈS Covid : {post_covid:.2f}%")
print(f"   Augmentation           : +{post_covid - pre_covid:.2f}%")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Impact du Covid-19 sur le Chômage en Inde", fontsize=15, fontweight="bold")

# 5.1 Évolution avec ligne Covid
df2_time = df2.groupby("Date")["Unemployment_Rate"].mean().reset_index()
axes[0].plot(df2_time["Date"], df2_time["Unemployment_Rate"],
             color="#3498db", linewidth=2.5, marker="o", markersize=5)
axes[0].axvline(covid_start, color="#e74c3c", linestyle="--",
                linewidth=2, label="Début Covid (Mars 2020)")
axes[0].fill_between(df2_time["Date"], df2_time["Unemployment_Rate"],
                     where=df2_time["Date"] >= covid_start,
                     alpha=0.15, color="#e74c3c", label="Période Covid")
axes[0].set_title("Évolution du chômage — Avant vs Après Covid")
axes[0].set_xlabel("Date")
axes[0].set_ylabel("Taux de chômage (%)")
axes[0].legend()
axes[0].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45)

# 5.2 Comparaison avant/après par état
state_covid = df2.groupby(["State", "Period"])["Unemployment_Rate"].mean().unstack()
state_covid = state_covid.dropna()
state_covid_diff = (state_covid["Après Covid (Mar-Nov 2020)"] - state_covid["Avant Covid"]).nlargest(10)

axes[1].barh(state_covid_diff.index, state_covid_diff.values,
             color=["#e74c3c" if v > 0 else "#2ecc71" for v in state_covid_diff.values])
axes[1].axvline(0, color="black", linewidth=0.8)
axes[1].set_title("Top 10 États — Hausse du chômage due au Covid")
axes[1].set_xlabel("Variation du taux de chômage (%)")

plt.tight_layout()
plt.savefig("unemployment_covid.png", bbox_inches="tight")
plt.show()
print(" Graphique Covid sauvegardé : unemployment_covid.png")

# ─────────────────────────────────────────
# 6. ANALYSE PAR RÉGION
# ─────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle("Analyse Régionale du Chômage", fontsize=15, fontweight="bold")

# 6.1 Heatmap par état et mois
df2["Month"] = df2["Date"].dt.strftime("%b %Y")
pivot = df2.pivot_table(values="Unemployment_Rate", index="State", columns="Month", aggfunc="mean")
sns.heatmap(pivot, cmap="YlOrRd", ax=axes[0], linewidths=0.3,
            cbar_kws={"label": "Taux de chômage (%)"})
axes[0].set_title("Heatmap — Chômage par État et par Mois")
axes[0].set_xlabel("")
axes[0].tick_params(axis="x", rotation=45)
axes[0].tick_params(axis="y", labelsize=7)

# 6.2 Boxplot par état (top 10 états les plus touchés)
top10_states = df2.groupby("State")["Unemployment_Rate"].mean().nlargest(10).index
df2_top10 = df2[df2["State"].isin(top10_states)]
df2_top10.boxplot(column="Unemployment_Rate", by="State", ax=axes[1],
                  rot=45, grid=False,
                  boxprops=dict(color="#3498db"),
                  medianprops=dict(color="#e74c3c", linewidth=2))
axes[1].set_title("Distribution du chômage — Top 10 États")
axes[1].set_xlabel("État")
axes[1].set_ylabel("Taux de chômage (%)")
plt.suptitle("")

plt.tight_layout()
plt.savefig("unemployment_regional.png", bbox_inches="tight")
plt.show()
print(" Graphique régional sauvegardé : unemployment_regional.png")

# ─────────────────────────────────────────
# 7. INSIGHTS CLÉS
# ─────────────────────────────────────────
print("\n" + "=" * 60)
print("   INSIGHTS CLÉS")
print("=" * 60)
print(f"\n1. Taux de chômage moyen global    : {df1['Unemployment_Rate'].mean():.2f}%")
print(f"2. Taux maximum enregistré         : {df1['Unemployment_Rate'].max():.2f}%")
print(f"3. Taux minimum enregistré         : {df1['Unemployment_Rate'].min():.2f}%")
print(f"4. État le plus touché             : {top10.iloc[0]['State']} ({top10.iloc[0]['Unemployment_Rate']:.2f}%)")
print(f"5. Taux avant Covid                : {pre_covid:.2f}%")
print(f"6. Taux après Covid                : {post_covid:.2f}%")
print(f"7. Hausse due au Covid             : +{post_covid - pre_covid:.2f}%")

print("\n Tâche 2 terminée avec succès !")
print("=" * 60)
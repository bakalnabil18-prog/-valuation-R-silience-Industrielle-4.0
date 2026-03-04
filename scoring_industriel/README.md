# 🏭 Scoring Risque Industriel 4.0
### Prototype PFE — Évaluation de la Résilience Industrielle en Environnement Cyber-Physique

---

## 🎯 Objectif

Ce prototype est un **instrument d'orientation stratégique** pour la souscription IARD.
Il ne produit pas `Prime = X DH` — il produit une **radiographie technique** du risque industriel 4.0 :

- **Niveau de maturité globale**
- **Zones critiques** identifiées
- **Facteurs aggravants** pour la souscription
- **Recommandations techniques** priorisées

---

## 🧠 Logique de Scoring

> Un risque 4.0 n'est pas seulement `Probabilité × Gravité`
> C'est : **Complexité × Interdépendance × Capacité d'absorption**

### 3 Indices principaux

| Indice | Poids | Description |
|--------|-------|-------------|
| **Score de Maturité Mécatronique** (A) | 35% | Degré automatisation + CPS + capteurs + infrastructure |
| **Score de Résilience Opérationnelle** (B) | 45% | Maintenance + pièces + intervention + redondance |
| **Score de Vulnérabilité Systémique** (C) | 20% | Dépendance réseau + fragilité IT + fragilité électrique |

**Score Global = A × 0.35 + B × 0.45 + (100 - C) × 0.20**

### 4 Outputs

- **A** — Score de Maturité Mécatronique (0–100)
- **B** — Score de Résilience Opérationnelle (0–100)
- **C** — Score de Vulnérabilité Systémique (0–100, inversé)
- **D** — Carte des Points Sensibles (zones critiques + recommandations)

---

## 🗂️ Structure du Projet

```
scoring_industriel/
│
├── app.py                    ← Point d'entrée Streamlit
├── requirements.txt
├── README.md
├── GUIDE_FINAL.md
├── START_HERE.md
│
├── data/
│   ├── industry_reference.json    ← Référentiel sectoriel
│   ├── scoring_parameters.json    ← Poids et formules
│   ├── maintenance_benchmark.json ← Benchmarks maintenance
│   ├── equipment_catalog.json     ← Catalogue équipements
│   └── sample_input.json          ← Exemple de saisie complète
│
├── engine/                        ← Moteur de scoring pur
│   ├── data_models.py             ← Dataclasses 8 modules
│   ├── normaliser.py              ← Streamlit → FormData
│   ├── scoring_mecatronique.py    ← Indice A
│   ├── scoring_maintenance.py     ← Indice B
│   ├── scoring_gouvernance.py     ← Indice C (vulnérabilité)
│   ├── health_score.py            ← Scores 8 modules (radar)
│   ├── underwriting.py            ← Profil + synthèse IARD
│   ├── risk_matrix.py             ← Détection zones critiques
│   ├── recommendation_engine.py   ← Recommandations priorisées
│   └── pipeline.py                ← Orchestrateur principal
│
├── ui/                            ← Interface Streamlit
│   ├── theme.py                   ← Couleurs + CSS
│   ├── forms.py                   ← Formulaires 8 modules
│   ├── dashboard.py               ← Panneau résultats
│   ├── charts.py                  ← Gauge + radar + barres
│   └── layout.py                  ← Orchestrateur UI
│
└── utils/
    ├── logger.py
    ├── validators.py              ← Validation + complétude
    └── helpers.py                 ← Chargement JSON + utils
```

---

## 🚀 Installation et Lancement

```bash
# 1. Cloner ou dézipper le projet
cd scoring_industriel

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
```

L'application s'ouvre automatiquement sur `http://localhost:8501`

---

## 📊 Les 8 Modules

| # | Module | Poids | Blocs |
|---|--------|-------|-------|
| 1 | 🤖 Robots Industriels | 18% | Identification + Quantitatif + Scoring |
| 2 | ⚙️ Machines CNC & Usinage | 14% | Identification + Technique + Risque |
| 3 | 🌐 Système Cyber-Physique (CPS) | 18% | Architecture + Infrastructure IT + Assurantiel |
| 4 | ⚡ Infrastructure Électrique | 10% | Équipement + Données + Impact |
| 5 | 🔧 Système de Maintenance | 20% | Organisation + Indicateurs + Maturité |
| 6 | 🏗️ Équipements & Manutention | 8% | Équipements + Scoring |
| 7 | 📦 Stockage & Pièces de Rechange | 8% | Infrastructure + Gestion num. + Performance + Assurantiel |
| 8 | 🚨 Efficacité Intervention Maintenance | 4% | Organisation + Indicateurs + Digitalisation |

---

## 🎨 Design

Interface inspirée du design fourni :
- **Formulaire multi-étapes** (5 étapes avec stepper visuel)
- **Panneau résultats en temps réel** (droite)
- Jauge score final + 3 indices + Radar 8 axes + Feux tricolores
- Carte des points sensibles + Recommandations priorisées
- Synthèse souscripteur en langage naturel

---

## 📁 Technologies

- **Streamlit** — Interface web Python
- **Plotly** — Visualisations (jauge, radar, barres)
- **Dataclasses Python** — Modèles de données typés
- **JSON** — Base de données de référence

---

## 👤 Auteur

Projet PFE — Scoring Risque Industriel 4.0
Lien : Ingénierie Mécatronique × Gestion Maintenance × Logistique × Souscription IARD Moderne

{
  "version": "2.0",
  "description": "Paramètres de scoring — 8 modules × 3 indices × 4 outputs",

  "indices": {
    "maturite_mecatronique": {
      "label": "Score de Maturité Mécatronique",
      "description": "Mesure le degré d'automatisation, la qualité des capteurs, l'intégration CPS et la robustesse de l'infrastructure.",
      "poids_global": 0.35,
      "composantes": {
        "automatisation_robots": 0.28,
        "integration_cnc_mes":   0.18,
        "cps_scada_mes":         0.22,
        "capteurs_predictifs":   0.20,
        "manutention_agv":       0.12
      }
    },
    "resilience_operationnelle": {
      "label": "Score de Résilience Opérationnelle",
      "description": "Mesure l'efficacité de la maintenance, la disponibilité des pièces critiques, la rapidité d'intervention et la redondance.",
      "poids_global": 0.45,
      "composantes": {
        "systeme_maintenance":   0.35,
        "stockage_pieces":       0.25,
        "efficacite_intervention": 0.22,
        "redondance_systemes":   0.18
      }
    },
    "vulnerabilite_systemique": {
      "label": "Score de Vulnérabilité Systémique",
      "description": "Mesure la dépendance réseau, l'absence de redondance IT, la centralisation excessive et la fragilité électrique. Score inversé : plus élevé = plus vulnérable.",
      "poids_global": 0.20,
      "composantes": {
        "dependance_production": 0.30,
        "fragilite_it":          0.28,
        "fragilite_electrique":  0.22,
        "absence_redondance":    0.20
      },
      "note": "Ce score est soustrait : (100 - vulnerabilite) * 0.20 dans l'indice global"
    }
  },

  "modules": {
    "robots": {
      "label": "Robots Industriels",
      "poids": 0.18,
      "criticite_formule": "valeur_totale_parc × dependance_production × (1 - niveau_redondance)",
      "variables_cles": {
        "integration_reseau": {
          "Connecté Cloud": 25,
          "Connecté MES":   15,
          "Isolé":           0
        },
        "niveau_redondance": {
          "Élevé":  25,
          "Moyen":  12,
          "Faible":  0
        },
        "dependance_production": {
          "Critique": -20,
          "Moyenne":  -10,
          "Faible":    0
        },
        "historique_pannes": {
          "0 panne":     15,
          "1-2 pannes":   8,
          "3-5 pannes":   3,
          "> 5 pannes":   0
        },
        "contrat_maintenance": { "oui": 15, "non": 0 },
        "capteurs_predictifs":  { "oui": 20, "non": 0 },
        "cobots":               { "oui":  6, "non": 0 },
        "cellule_modulaire":    { "oui":  5, "non": 0 },
        "maj_firmware":         { "oui":  8, "non": 0 }
      }
    },

    "cnc": {
      "label": "Machines CNC & Usinage",
      "poids": 0.14,
      "impacts_principaux": ["Bris de machine", "Dommage électrique", "Perte d'exploitation"],
      "variables_cles": {
        "automation_cnc": {
          "Full auto":  25,
          "Semi-auto":  13,
          "Manuel":      0
        },
        "freq_maintenance_prev": {
          "Mensuelle":      15,
          "Trimestrielle":  10,
          "Semestrielle":    6,
          "Annuelle":        2,
          "Aucune":          0
        },
        "ups_dedie":            { "oui": 20, "non": 0 },
        "protection_surtension":{ "oui": 15, "non": 0 },
        "maintenance_pred_cnc": { "oui": 20, "non": 0 },
        "sensibilite_electrique":{ "oui": -10, "non": 0 },
        "interface_mes_erp":    { "oui": 10, "non": 0 }
      }
    },

    "cps": {
      "label": "Système Cyber-Physique",
      "poids": 0.18,
      "equation_risque": "centralisation × (1 - redondance)",
      "variables_cles": {
        "presence_scada":     { "oui": 12, "non": 0 },
        "mes_integre":        { "oui": 12, "non": 0 },
        "redondance_serveurs":{ "oui": 18, "non": -15 },
        "backup_quotidien":   { "oui": 12, "non": -8 },
        "parefeu_industriel": { "oui": 12, "non": -8 },
        "audit_cyber":        { "oui": 12, "non": -5 },
        "segmentation_reseau": {
          "Élevée":  10,
          "Moyenne":  5,
          "Faible":  -10
        },
        "plan_continuite":    { "oui": 12, "non": -10 },
        "simulation_crise":   { "oui":  8, "non": 0 },
        "dependance_cps": {
          "Critique": -20,
          "Moyen":    -10,
          "Faible":    0
        }
      }
    },

    "electrique": {
      "label": "Infrastructure Électrique",
      "poids": 0.10,
      "impacts_principaux": ["Vulnérabilité dommage électrique", "Risque court-circuit", "Risque propagation incendie"],
      "variables_cles": {
        "tableau_bt_mt":         { "oui": 15, "non": 0 },
        "protection_diff":       { "oui": 15, "non": 0 },
        "ups_industriel":        { "oui": 15, "non": -8 },
        "groupe_electrogene":    { "oui": 12, "non": 0 },
        "mise_a_la_terre":       { "oui": 15, "non": -10 },
        "incidents_electriques": {
          "0":    10,
          "1-2":  -5,
          "3-5": -15,
          "> 5": -25
        },
        "vulnerabilite_dom_elec": {
          "Faible":   10,
          "Modérée":   0,
          "Élevée":  -15
        }
      }
    },

    "maintenance": {
      "label": "Système de Maintenance",
      "poids": 0.20,
      "poids_score_global": "35-40%",
      "variables_cles": {
        "type_maintenance": {
          "Prédictive":  30,
          "Préventive":  18,
          "Corrective":   0
        },
        "gmao_utilisee":       { "oui": 15, "non": 0 },
        "existence_kpi":       { "oui":  8, "non": 0 },
        "ia_predictive":       { "oui": 20, "non": 0 },
        "maint_conditionnelle":{ "oui": 15, "non": 0 },
        "niveau_digitalisation": {
          "5": 20, "4": 16, "3": 10, "2": 5, "1": 0
        },
        "mtbf_global_seuils": {
          "description": "MTBF en heures — bonus si élevé",
          "> 3000":  15,
          "2000-3000": 10,
          "1000-2000":  5,
          "< 1000":     0
        },
        "mttr_global_seuils": {
          "description": "MTTR en heures — bonus si faible",
          "< 2":   12,
          "2-4":    8,
          "4-8":    4,
          "> 8":    0
        },
        "taux_planifie_seuils": {
          "> 80%": 10,
          "60-80%": 6,
          "< 60%":  0
        }
      }
    },

    "manutention": {
      "label": "Équipements & Manutention",
      "poids": 0.08,
      "impact_direct": "MTTR — Temps de Réparation",
      "variables_cles": {
        "presence_agv":          { "oui": 20, "non": 0 },
        "manutention_auto":      { "oui": 15, "non": 0 },
        "disponibilite_247":     { "oui": 20, "non": 0 },
        "redond_equip_crit":     { "oui": 15, "non": 0 },
        "dependance_prestataire":{ "oui": -15,"non": 10 },
        "atelier_interne":       { "oui": 10, "non": 0 },
        "disponibilite_pct": {
          "> 95%": 10,
          "85-95%": 6,
          "< 85%":  0
        }
      }
    },

    "stockage": {
      "label": "Stockage & Pièces de Rechange",
      "poids": 0.08,
      "impacts_principaux": ["Perte d'exploitation", "Allongement durée sinistre", "Coût aggravé BDM"],
      "variables_cles": {
        "pieces_crit_redond":    { "oui": 22, "non": -15 },
        "fournisseurs_multiples":{ "oui": 18, "non": -5 },
        "integration_erp_stock": { "oui": 12, "non": 0 },
        "analyse_abc":           { "oui": 10, "non": 0 },
        "stock_minimum_defini":  { "oui": 10, "non": 0 },
        "contrat_appro_prio":    { "oui": 10, "non": 0 },
        "simulation_penurie":    { "oui":  8, "non": 0 },
        "taux_rupture_stock": {
          "0%":    18,
          "< 5%":  10,
          "5-15%":  0,
          "> 15%": -15
        },
        "pct_pieces_crit_stock": {
          "> 90%": 10,
          "70-90%": 5,
          "< 70%":  0
        }
      }
    },

    "intervention": {
      "label": "Efficacité Intervention Maintenance",
      "poids": 0.04,
      "variables_cles": {
        "astreinte_247":         { "oui": 18, "non": 0 },
        "equipe_interne":        { "oui": 15, "non": 0 },
        "techniciens_certif":    { "oui": 12, "non": 0 },
        "gmao_mobile":           { "oui": 10, "non": 0 },
        "tracabilite_rt":        { "oui": 10, "non": 0 },
        "dashboard_kpi":         { "oui": 10, "non": 0 },
        "historique_pannes_analyse": { "oui": 8, "non": 0 },
        "pct_interv_4h_seuils": {
          "> 80%": 15,
          "60-80%": 8,
          "< 60%":  0
        },
        "taux_resolution_pp_seuils": {
          "> 85%": 10,
          "70-85%": 5,
          "< 70%":  0
        },
        "historique_arret_24h": {
          "0":      10,
          "1-3":     0,
          "> 3":   -10
        }
      }
    }
  },

  "outputs": {
    "A_score_maturite_mecatronique": {
      "description": "Score 0-100 mesurant degré automatisation, capteurs, CPS, infrastructure"
    },
    "B_score_resilience_operationnelle": {
      "description": "Score 0-100 mesurant efficacité maintenance, pièces, intervention, redondance"
    },
    "C_score_vulnerabilite_systemique": {
      "description": "Score 0-100 mesurant dépendance réseau, fragilité IT/électrique (inversé)"
    },
    "D_carte_points_sensibles": {
      "description": "Liste des zones critiques et majeures avec recommandations priorisées"
    }
  }
}

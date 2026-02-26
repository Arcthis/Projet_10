# Documentation du Workflow `reconciliation-vins`

## Objectif
Ce workflow Kestra a pour but de :
- Consolider des données issues de 3 sources distinctes :  
  - **ERP** : données produits (stock, prix, statut)  
  - **Web** : données issues du site e-commerce (ventes, produits, titres)  
  - **Liaison** : table de correspondance entre les identifiants ERP et Web  
- Nettoyer et dédupliquer les données  
- Réaliser la fusion ERP ↔ Web via la table de liaison  
- Calculer le chiffre d’affaires global et par produit  
- Détecter les incohérences de stock dans l’ERP  
- Identifier des vins "premium" vs "ordinaires" via une analyse statistique (z-score)  
- Générer des exports structurés (CSV et Excel) pour exploitation  

Le tout est exécuté de manière planifiée (cron mensuel).

---

## Déclencheur
- **Trigger :** `planification`  
- **Type :** `Schedule`  
- **Cron :** `0 9 15 * *` → Exécution automatique le 15 de chaque mois à 9h.

---

## Entrées
Le workflow attend 3 fichiers en entrée :
- `erp` → Extraction de l’ERP  
- `web` → Extraction du site e-commerce  
- `liaison` → Mapping entre `product_id` ERP et `sku` Web  

---

## Tâches principales

### `process_all` (Python script avec DuckDB)
Cœur du traitement, il effectue les étapes suivantes :

#### 1. Nettoyage et validation des données
- Suppression des doublons  
- Vérification de la présence des colonnes critiques (`product_id`, `sku`, `id_web`)  
- Détection des doublons et valeurs manquantes (exceptions levées en cas d’anomalies critiques)  

**Choix Python :**  
Le nettoyage et la validation sont plus simples en pandas (méthodes rapides et lisibles : `drop_duplicates`, `isnull`, `to_numeric`).

#### 2. Stockage intermédiaire et fusion des données
- Export vers CSV des données nettoyées  
- Utilisation de DuckDB pour :  
  - Création de tables dédupliquées  
  - Jointures entre ERP, Web et Liaison  
  - Calcul du chiffre d’affaires par produit et du chiffre d’affaires total  

**Choix SQL (DuckDB) :**  
- Syntaxe plus déclarative et concise qu’en pandas  
- Optimisé pour les jointures et agrégations  
- Plus lisible et maintenable pour ajouter de nouveaux indicateurs  

#### 3. Analyse statistique : premium vs ordinaire
- Calcul du z-score sur les prix produits  
- Classification :  
  - `premium` si z-score > 2  
  - `ordinaire` sinon  

**Choix Python :**  
Le calcul statistique (moyenne, écart-type, z-score) est plus simple et flexible en pandas/numpy qu’en SQL.

#### 4. Export et reporting
- CSV générés :  
  - `erp_clean.csv`, `web_clean.csv`, `liaison_clean.csv`  
  - `vins_premium.csv`, `vins_ordinaire.csv`, `stock_incoherences.csv`  
- Excel généré : `rapport_ca.xlsx` avec plusieurs onglets :  
  - CA par produit  
  - CA global  
  - Fusion complète  

#### 5. Contrôles de cohérence
- Vérification de l’unicité des identifiants (`product_id`, `sku`)  
- Concordance entre CA recalculé et CA global  
- Catégorisation correcte de tous les produits  
- Cohérence des statuts et quantités de stock  

---

## Sorties
Le workflow produit plusieurs fichiers :  
- **rapport_excel** → `rapport_ca.xlsx`  
- **vins_premium** → `vins_premium.csv`  
- **vins_ordinaire** → `vins_ordinaire.csv`  
- **stock_incoherences** → `stock_incoherences.csv`  

---

## Logique de conception

### Pourquoi Python ?
- Nettoyage et validation (pandas) → plus rapide et lisible que SQL  
- Statistiques (numpy/pandas) → calculs avancés difficiles à exprimer en SQL  
- Vérifications (exceptions, conditions complexes) → meilleure granularité en Python  

### Pourquoi SQL (DuckDB) ?
- Fusion des datasets (jointures multiples) → plus lisible en SQL  
- Agrégations globales (CA par produit, CA total) → plus naturel en SQL  
- Performance : DuckDB lit directement les CSV nettoyés  

---

## Bonnes pratiques et maintenance
- **Séparation des responsabilités :**  
  - Python → nettoyage, validations, statistiques  
  - SQL → fusion et agrégations  

- **Robustesse :**  
  - Exceptions levées en cas d’anomalies critiques  
  - Logs informatifs (`[INFO]`, `[WARNING]`) pour suivre l’exécution  

- **Facilité de maintenance :**  
  - Chaque bloc du script est autonome (nettoyage, fusion, analyse, contrôles)  
  - Nouveaux indicateurs → ajout dans les requêtes SQL  
  - Logique de classification → partie Python uniquement  

- **Planification automatisée :**  
  - Cron mensuel assure l’actualisation régulière du reporting  

---

## Résumé
Ce document permet à un mainteneur de comprendre :  
1. Comment le workflow fonctionne  
2. Pourquoi certains choix techniques (Python vs SQL) ont été faits  
3. Où intervenir pour ajouter ou modifier des règles

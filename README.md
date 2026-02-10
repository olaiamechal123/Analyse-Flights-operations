
# Analyse des Opérations de Vols (Flight Operations Analytics)

Projet de pipeline de données en temps réel pour l'analyse des opérations aériennes, utilisant **Apache Airflow**, l'API **OpenSky Network** et **Snowflake**.

<p align="center">
  <img src="https://img.shields.io/badge/Apache%20Airflow-2.x-017cee?style=for-the-badge&logo=apache-airflow&logoColor=white" alt="Airflow"/>
  <img src="https://img.shields.io/badge/OpenSky%20Network-API-blue?style=for-the-badge" alt="OpenSky"/>
  <img src="https://img.shields.io/badge/Snowflake-Data%20Cloud-249edc?style=for-the-badge&logo=snowflake&logoColor=white" alt="Snowflake"/>
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" alt="Docker"/>
</p>

## Aperçu du projet

Ce projet met en place un pipeline ETL/ELT automatisé qui :

- Récupère les positions des avions en temps réel via l’API publique **OpenSky Network**
- Traite les données selon l’architecture **médaille** (Bronze → Silver → Gold)
- Calcule des KPI par pays (nombre de vols, vitesse moyenne, avions au sol, etc.)
- Charge les résultats dans **Snowflake**
- Permet la création de tableaux de bord analytiques

## Objectifs analytiques
- Top pays par nombre de vols
- Top pays par nombre d’avions au sol
- Évolution de la vitesse moyenne (focus États-Unis → observation : stabilité)
## Architecture Pipeline

```text
[ OpenSky Network API ] 
       (temps réel ADS-B)
            │
            ▼
[ Apache Airflow ]
   (orchestration DAG)
            │
            ▼
[ Bronze ] ── JSON brut horodaté ── /opt/airflow/data/bronze
            │
            ▼
[ Silver ] ── CSV nettoyé & réduit ── /opt/airflow/data/silver
            │
            ▼
[ Gold   ] ── KPI agrégés par pays (CSV)
            │
            ▼
[ Snowflake ] ── table FLIGHTS_KPIS
            │
            ▼
[ Dashboards analytiques (Snowsight) ]
```

## Données sources

**OpenSky Network** — données ADS-B en temps réel  
Colonnes conservées :

- `icao24`          : identifiant unique 24 bits (hex)
- `origin_country`  : pays d'immatriculation
- `velocity`        : vitesse au sol (m/s)
- `on_ground`       : boolean – avion au sol ?
## Structure du projet

```text
flight-operations-analytics/
├── dags/
│   └── flights_pipeline.py           # DAG principal Airflow
├── scripts/
│   ├── bronze_ingested.py              # Récupération API → JSON brut
│   ├── sliver_transform.py             # Nettoyage → CSV silver
│   ├── gold_aggregation.py                # Agrégations KPI → CSV gold
│   └── load_gold_to_snowflake.py          # Chargement vers Snowflake
├── docker-compose.yml                # Configuration Docker Airflow + Postgres                     
├── requirements.txt                  # Dépendances Python (si nécessaire)
└── README.md
```


## Organisation des scripts

- **bronze_script** : Téléchargement en temps réel via l’API publique OpenSky Network → sauvegarde en fichier JSON horodaté → stockage dans /opt/airflow/data/bronze → transmission du chemin via XCom  
- **silver_script** : Transformation du JSON brut en CSV propre → sélection des colonnes (icao24, origin_country, velocity, on_ground) → stockage dans /opt/airflow/data/silver  
- **gold_script** : Transformation des observations individuelles en KPI par pays → génération du fichier CSV business  
- **load_to_snowflake** : Chargement du fichier CSV gold (agrégations par pays : nombre de vols, vitesse moyenne, avions au sol) dans la table FLIGHTS_KPIS de Snowflake  

## Pipeline Airflow

Fichier : **flights_pipeline.py** (situé dans le dossier dags/)  
Orchestration des quatre étapes : bronze → silver → gold → load

![Airflow Pipeline](https://github.com/olaiamechal123/Analyse-Flights-operations/blob/main/airflow_pipeline.PNG)

## Configuration Snowflake

- Création d’une base de données nommée **flights**  
- Création d’un schéma nommé **kpis**  
- Création d’une table nommée **flights_kpis**  

## Analyses et dashboard

1. Analyse des pays présentant le plus grand nombre de vols  : États-Unis
2. Analyse des pays présentant le plus grand nombre d’avions au sol  : États-Unis
3. Focus sur les États-Unis (pays réalisant le plus de vols) : observation de la stabilité de la vitesse moyenne au cours du temps


| Dataset Source (OpenSky) | Dashboard Final (Snowflake) |
| :---: | :---: |
| ![Dataset](https://github.com/olaiamechal123/Analyse-Flights-operations/blob/main/dataset.PNG) | ![Dashboard](https://github.com/olaiamechal123/Analyse-Flights-operations/blob/main/dashboard_simple.PNG) |


 

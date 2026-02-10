
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

- Pays réalisant le plus de vols → vitesse moyenne des avions
- Analyse détaillée des vols au **Maroc**
- Nombre d’avions en vol / au sol au Maroc
- Top pays par nombre de vols
- Top pays par nombre d’avions au sol
- Évolution de la vitesse moyenne (focus États-Unis → observation : stabilité)

## Données sources

**OpenSky Network** — données ADS-B en temps réel  
Colonnes conservées :

- `icao24`          : identifiant unique 24 bits (hex)
- `origin_country`  : pays d'immatriculation
- `velocity`        : vitesse au sol (m/s)
- `on_ground`       : boolean – avion au sol ?
- 

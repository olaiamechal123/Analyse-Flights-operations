import pandas as pd
from pathlib import Path

def run_gold_aggregate(**context):
    ti = context["ti"]
    
    # ───────────────────────────────────────────────
    # Récupération du fichier silver via XCom
    # ───────────────────────────────────────────────
    silver_file = ti.xcom_pull(
        key="silver_file",
        task_ids="sliver_transform"   # ← VÉRIFIE que c'est bien le task_id exact !
                                      # Souvent c'est "silver_transform" ou "silver_layer"
    )
    
    if silver_file is None:
        raise ValueError(
            "Impossible de récupérer 'silver_file' depuis XCom.\n"
            "→ La tâche 'sliver_transform' a-t-elle réussi ?\n"
            "→ A-t-elle bien fait xcom_push(key='silver_file', ...) ?\n"
            "→ Le task_ids est-il correct ?"
        )
    
    silver_path = Path(silver_file)
    
    if not silver_path.is_file():
        raise FileNotFoundError(f"Le fichier silver n'existe pas : {silver_file}")
    
    # Lecture
    print(f"[gold] Lecture du fichier : {silver_file}")
    df = pd.read_csv(silver_path)
    
    # Agrégation (corrigée et propre)
    agg = (
        df.groupby("origin_country", as_index=False)
          .agg(
              total_flights = ("icao24",   "count"),
              avg_velocity  = ("velocity", "mean"),
              on_ground     = ("on_ground", "sum")
          )
    )
    
    # ───────────────────────────────────────────────
    # Création du chemin gold – version robuste
    # ───────────────────────────────────────────────
    gold_dir = Path("/opt/airflow/data/gold")           # ou silver_path.parent.parent / "gold"
    gold_dir.mkdir(parents=True, exist_ok=True)
    
    # On remplace silver → gold dans le nom du fichier
    gold_filename = silver_path.name.replace("silver", "gold").replace("sliver", "gold")
    gold_path = gold_dir / gold_filename
    
    # Sauvegarde
    print(f"[gold] Sauvegarde vers : {gold_path}")
    agg.to_csv(gold_path, index=False, encoding="utf-8")
    
    # Push vers XCom pour les tâches suivantes
    ti.xcom_push(key="gold_file", value=str(gold_path))
    
    print(f"[gold] Succès – fichier créé et poussé : {gold_path}")
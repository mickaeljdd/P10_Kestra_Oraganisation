# Pipeline Kestra BottleNeck

Ce projet orchestre la reconciliation des donnees ERP et web avec Kestra, calcule le chiffre d'affaires par produit, classe les vins selon leur prix et genere un rapport Excel automatique.

## Lancer le pipeline

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python xlsxtocsv.py
docker compose up
```

L'interface Kestra est disponible sur `http://localhost:8080`.

## Tests de qualite

Le flow Kestra execute `pytest` dans la tache `run_data_quality_tests` avant de construire les rapports. En cas d'echec d'un test, l'execution du pipeline echoue.

Pour les executer egalement en local :

```bash
pytest
```

Les tests verifient notamment la presence des colonnes attendues, la qualite des cles de jointure, la reconciliation ERP / WEB et le calcul du chiffre d'affaires.

## Succession des etapes du flow

```mermaid
flowchart TD
    A[Fichiers Excel source] --> B[Conversion XLSX vers CSV]
    B --> T[Tests de qualite Pytest]
    T --> C[Chargement ERP dans DuckDB]
    B --> D[Chargement WEB dans DuckDB]
    B --> E[Chargement liaison dans DuckDB]
    C --> F[Nettoyage ERP]
    D --> G[Nettoyage WEB]
    E --> H[Nettoyage liaison]
    F --> I[Jointure ERP liaison WEB]
    G --> I
    H --> I
    I --> J[Calcul du chiffre affaires]
    J --> K[Calcul z-score prix]
    K --> L[Classification premium ordinaire]
    L --> M[Exports CSV]
    M --> N[Rapport Excel automatique]
    N --> O[Planification mensuelle Kestra]
```

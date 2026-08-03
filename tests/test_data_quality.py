from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "input"


def load_inputs():
    erp = pd.read_csv(INPUT_DIR / "Fichier_erp.csv")
    web = pd.read_csv(INPUT_DIR / "Fichier_web.csv")
    liaison = pd.read_csv(INPUT_DIR / "fichier_liaison.csv")
    return erp, web, liaison


def build_joined_dataset():
    erp, web, liaison = load_inputs()
    erp_clean = erp[erp["product_id"].notna()].drop_duplicates().copy()
    web_products = web[
        web["sku"].notna() & web["total_sales"].notna() & (web["post_type"] == "product")
    ].copy()
    liaison = liaison[
        liaison["product_id"].notna() & liaison["id_web"].notna()
    ].drop_duplicates().copy()

    web_products["sku"] = web_products["sku"].astype(str)
    liaison["id_web"] = liaison["id_web"].astype(str)

    return erp_clean.merge(liaison, on="product_id").merge(
        web_products,
        left_on="id_web",
        right_on="sku",
    )


def test_input_files_have_required_columns():
    erp, web, liaison = load_inputs()

    assert {"product_id", "price", "stock_quantity"}.issubset(erp.columns)
    assert {"sku", "total_sales", "post_type"}.issubset(web.columns)
    assert {"product_id", "id_web"}.issubset(liaison.columns)


def test_liaison_cleaning_removes_missing_keys_and_keeps_unique_products():
    _, _, liaison = load_inputs()
    cleaned = liaison[
        liaison["product_id"].notna() & liaison["id_web"].notna()
    ].drop_duplicates()

    assert cleaned["product_id"].notna().all()
    assert cleaned["id_web"].notna().all()
    assert not cleaned["product_id"].duplicated().any()


def test_reconciliation_join_is_not_empty():
    joined = build_joined_dataset()

    assert len(joined) > 0


def test_computed_revenue_is_never_negative():
    joined = build_joined_dataset()
    revenue = joined["price"] * joined["total_sales"]

    assert revenue.notna().all()
    assert (revenue >= 0).all()


def test_premium_classification_produces_both_categories():
    joined = build_joined_dataset()
    prices = joined["price"]
    z_scores = (prices - prices.mean()) / prices.std()
    categories = z_scores.apply(lambda score: "premium" if score > 2 else "ordinaire")

    assert {"premium", "ordinaire"}.issubset(set(categories))

def test_z_score_threshold_is_strictly_greater_than_two():
    z_scores = pd.Series([1.99, 2.0, 2.01])

    categories = z_scores.apply(
        lambda score: "premium" if score > 2 else "ordinaire"
    )

    assert categories.tolist() == [
        "ordinaire",
        "ordinaire",
        "premium",
    ]

def test_expected_row_counts():
    erp, web, liaison = load_inputs()

    # ERP : suppression des clés manquantes et des doublons
    erp_clean = (
        erp[
            erp["product_id"].notna()
        ]
        .drop_duplicates()
    )

    # Liaison dédoublonnée avant suppression des clés manquantes
    liaison_deduplicated = liaison.drop_duplicates()

    # Liaison réellement utilisable pour les jointures
    liaison_clean = (
        liaison[
            liaison["product_id"].notna()
            & liaison["id_web"].notna()
        ]
        .drop_duplicates()
    )

    # Web : uniquement les produits exploitables
    web_clean = (
        web[
            web["sku"].notna()
            & web["total_sales"].notna()
            & (web["post_type"] == "product")
        ]
        .drop_duplicates()
    )

    joined = build_joined_dataset()

    assert len(erp_clean) == 825
    assert len(liaison_deduplicated) == 825
    assert len(liaison_clean) == 734
    assert len(web_clean) == 714
    assert len(joined) == 714

def test_total_revenue_matches_expected_value():
    joined = build_joined_dataset()

    total_revenue = (
        joined["price"].astype(float)
        * joined["total_sales"].astype(float)
    ).sum()

    assert round(total_revenue, 2) == 70568.60
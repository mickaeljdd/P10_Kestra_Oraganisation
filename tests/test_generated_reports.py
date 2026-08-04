from pathlib import Path
import pandas as pd


def test_generated_reports():

    # ---------- Présence des fichiers ----------

    for file in [
        "ca_by_product.csv",
        "premium.csv",
        "ordinaires.csv",
        "revenue_report.xlsx",
    ]:

        assert Path(file).exists()
        assert Path(file).stat().st_size > 0

    # ---------- Lecture ----------

    ca = pd.read_csv("ca_by_product.csv")
    premium = pd.read_csv("premium.csv")
    ordinaires = pd.read_csv("ordinaires.csv")

    # ---------- Vérifications métier ----------

    assert len(ca) == 714
    assert len(premium) == 30
    assert len(ordinaires) == 684

    assert round(ca["total_ca"].sum(), 2) == 70568.60

    assert (premium["z_score"] > 2).all()
    assert (ordinaires["z_score"] <= 2).all()

    # ---------- Rapport Excel ----------

    xls = pd.ExcelFile("revenue_report.xlsx")

    assert "Synthese" in xls.sheet_names
    assert "CA par produit" in xls.sheet_names
    assert "Vins premium" in xls.sheet_names
    assert "Vins ordinaires" in xls.sheet_names
import pandas as pd

from xlsxtocsv import convert_excel_to_csv


def test_convert_excel_to_csv_preserves_columns_and_rows(tmp_path):
    source = tmp_path / "source.xlsx"
    target = tmp_path / "target.csv"
    expected = pd.DataFrame(
        {
            "product_id": [1, 2],
            "price": [10.5, 20.0],
            "stock_quantity": [3, 4],
        }
    )
    expected.to_excel(source, index=False)

    returned = convert_excel_to_csv(source, target)
    actual = pd.read_csv(target)

    pd.testing.assert_frame_equal(returned, expected)
    pd.testing.assert_frame_equal(actual, expected)

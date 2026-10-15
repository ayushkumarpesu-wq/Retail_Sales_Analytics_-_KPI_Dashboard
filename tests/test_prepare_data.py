import pandas as pd
import pytest

from src.prepare_data import clean_data


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["1001", "A1", " Widget ", 2, "2011-01-01", 5.0, 10, "United Kingdom"],
            ["1001", "A1", " Widget ", 2, "2011-01-01", 5.0, 10, "United Kingdom"],
            ["1002", "A1", None, -1, "2011-01-02", 5.0, None, "United Kingdom"],
            ["C1003", "B2", "Cancelled", -1, "2011-01-03", 3.0, 11, "France"],
            ["1004", "C3", "Invalid zero qty", 0, "2011-01-04", 2.0, 12, "France"],
            ["1005", "D4", "Invalid price", 1, "2011-01-05", -1.0, 13, "France"],
        ],
        columns=[
            "InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate",
            "UnitPrice", "CustomerID", "Country",
        ],
    )


def test_cleaning_deduplicates_but_retains_returns_and_cancellations(sample_transactions):
    cleaned, quality = clean_data(sample_transactions)

    assert len(cleaned) == 3
    assert quality["duplicate_rows_removed"] == 1
    assert quality["invalid_rows_removed"] == 2
    assert quality["missing_customer_id_rows_retained"] == 1
    assert quality["return_rows_retained"] == 1
    assert quality["cancellation_rows_retained"] == 1
    assert cleaned["revenue"].sum() == pytest.approx(2.0)
    assert "Unknown" in cleaned["description"].tolist()


def test_missing_required_columns_fail_clearly():
    with pytest.raises(ValueError, match="missing expected columns"):
        clean_data(pd.DataFrame({"InvoiceNo": ["1001"]}))

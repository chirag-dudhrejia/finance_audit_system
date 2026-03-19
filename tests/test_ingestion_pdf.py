import pandas as pd
from io import BytesIO
from unittest.mock import MagicMock, patch

from services.ingestion_service import IngestionService


def test_ingest_file_delegates_to_pdf_parser_and_inserts():
    # Prepare a fake parsed dataframe
    df = pd.DataFrame([
        {
            "transaction date": "2023-01-01",
            "descriptions": "Grocery",
            "debit": 50.0,
            "credit": None,
            "transaction amount": 50.0,
        },
        {
            "transaction date": "2023-01-02",
            "descriptions": "Salary",
            "debit": None,
            "credit": 1000.0,
            "transaction amount": -1000.0,
        },
    ])

    # Create a file-like object that looks like a PDF upload
    file_like = BytesIO(b"%PDF-1.4 test")
    file_like.name = "statement.pdf"

    with patch("services.ingestion_service.parse_pdf", return_value=df) as mock_parse:
        mock_repo = MagicMock()
        with patch(
            "services.ingestion_service.TransactionRepo", return_value=mock_repo
        ):
            service = IngestionService()
            processed = service.ingest_file(file_like, user_id="demo")

    assert processed == len(df)
    mock_parse.assert_called_once()
    mock_repo.insert_raw.assert_called_once()
    mock_repo.bulk_insert_clean.assert_called_once()

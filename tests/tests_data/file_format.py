from app.db.models.file.file_format import InputFormat

file_format_data = [
    {
        "file_id": "94fd971c-fa7d-4a9b-bedf-781622dc2741",
        "input_format": InputFormat.TABULAR,
        "id": "5230bb83-8f16-47ca-8925-6b5abee03f1c",
        "singular_tid_column_index": None,
        "singular_item_column_index": None,
        "tabular_has_tid": True,
    },
    {
        "file_id": "0589040a-1924-42f9-9c1d-e4c57756963f",
        "input_format": InputFormat.SINGULAR,
        "singular_tid_column_index": 3,
        "singular_item_column_index": 4,
        "tabular_has_tid": None,
    },
]

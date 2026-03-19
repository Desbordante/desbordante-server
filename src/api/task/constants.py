# Examples from desbordante-core/examples/basic/
# FD: mining_fd.py — university_fd.csv, HyFD
# AR: mining_ar.py — rules_book.csv, minsup=0.4, minconf=0.6
# MD: mining_md.py — animals_beverages.csv, Levenshtein per column
CREATE_TASK_OPENAPI_EXAMPLES = {
    "FD (university_fd.csv)": {
        "summary": "FD — Functional Dependencies",
        "description": "Dataset university_fd.csv. Replace dataset_id with your uploaded dataset ID.",
        "value": {
            "primitive_name": "fd",
            "config": {"algo_name": "hy_fd"},
            "datasets": {"table": "00000000-0000-0000-0000-000000000001"},
        },
    },
    "AR (rules_book.csv)": {
        "summary": "AR — Association Rules",
        "description": "Dataset rules_book.csv. minsup=0.4, minconf=0.6. Replace dataset_id.",
        "value": {
            "primitive_name": "ar",
            "config": {
                "algo_name": "apriori",
                "minsup": 0.4,
                "minconf": 0.6,
            },
            "datasets": {"table": "00000000-0000-0000-0000-000000000001"},
        },
    },
    "MD (animals_beverages.csv)": {
        "summary": "MD — Matching Dependencies",
        "description": "Dataset animals_beverages.csv. Compare each column to itself using Levenshtein. Replace left_table and right_table with your uploaded dataset ID (same for both).",
        "value": {
            "primitive_name": "md",
            "config": {
                "algo_name": "hy_md",
                "column_matches": [
                    {"left_column": 0, "right_column": 0, "metric": "levenshtein"},
                    {"left_column": 1, "right_column": 1, "metric": "levenshtein"},
                    {"left_column": 2, "right_column": 2, "metric": "levenshtein"},
                    {"left_column": 3, "right_column": 3, "metric": "levenshtein"},
                ],
            },
            "datasets": {
                "left_table": "00000000-0000-0000-0000-000000000001",
                "right_table": "00000000-0000-0000-0000-000000000001",
            },
        },
    },
}

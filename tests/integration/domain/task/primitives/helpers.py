"""Helper functions for primitive integration tests."""

import re
from pathlib import Path
from typing import Literal

import pandas as pd

from src.schemas.dataset_schemas import (
    DatasetSeparator,
    SingularTransactionalParams,
    TabularDatasetInfo,
    TabularDatasetParams,
    TabularDownloadedDatasetSchema,
    TabularTransactionalParams,
    TransactionalDatasetInfo,
    TransactionalDatasetParams,
    TransactionalDownloadedDatasetSchema,
)


def fd_to_key(
    lhs_indices: tuple[int, ...], rhs_index: int
) -> tuple[frozenset[int], int]:
    """Convert FD to comparable key (lhs indices as frozenset, rhs index)."""
    return (frozenset(lhs_indices), rhs_index)


def _parse_dd_string(
    dd_str: str,
) -> tuple[frozenset[tuple[str, tuple[int, int]]], tuple[str, tuple[int, int]]]:
    """Parse desbordante DD string to (lhs_set, rhs_tuple)."""
    pattern = r"^(.+?)\s*->\s*(.+?)$"
    match = re.match(pattern, dd_str.strip())
    if not match:
        raise ValueError(f"Invalid DD format: {dd_str}")
    lhs_part, rhs_part = match.groups()
    item_pattern = r"(\w+)\s*\[(\d+),\s*(\d+)\]"
    lhs_items = frozenset(
        (name, (int(start), int(end)))
        for name, start, end in re.findall(item_pattern, lhs_part)
    )
    rhs_match = re.search(item_pattern, rhs_part)
    if not rhs_match:
        raise ValueError(f"Invalid DD right part: {rhs_part}")
    rhs_name, rhs_start, rhs_end = rhs_match.groups()
    rhs_item = (rhs_name, (int(rhs_start), int(rhs_end)))
    return lhs_items, rhs_item


def dd_to_key_from_string(
    dd_str: str,
) -> tuple[frozenset[tuple[str, tuple[int, int]]], tuple[str, tuple[int, int]]]:
    """Convert desbordante DD string to comparable key."""
    return _parse_dd_string(dd_str)


def dd_to_key_from_item(
    lhs_items: list, rhs_item
) -> tuple[frozenset[tuple[str, tuple[int, int]]], tuple[str, tuple[int, int]]]:
    """Convert DdTaskResultItemSchema to comparable key."""
    lhs_set = frozenset(
        (item.name, tuple(item.distance_interval)) for item in lhs_items
    )
    rhs_tuple = (rhs_item.name, tuple(rhs_item.distance_interval))
    return lhs_set, rhs_tuple


def _md_side_item_to_tuple(item, metric_normalize=str) -> tuple:
    """Convert MdSideItemSchema to comparable tuple."""
    return (
        metric_normalize(item.metric),
        item.left_column.index,
        item.right_column.index,
        round(item.boundary, 10),
        item.max_invalid_boundary,
    )


def _normalize_metric(m) -> str:
    """Normalize metric name for comparison (desbordante may use different casing)."""
    return str(m).lower()


def md_to_key_from_item(lhs_items: list, rhs_item) -> tuple[frozenset[tuple], tuple]:
    """Convert MdTaskResultItemSchema to comparable key."""
    lhs_set = frozenset(_md_side_item_to_tuple(i, _normalize_metric) for i in lhs_items)  # type: ignore
    rhs_tuple = _md_side_item_to_tuple(rhs_item, _normalize_metric)  # type: ignore
    return lhs_set, rhs_tuple


def md_to_key_from_desbordante(md) -> tuple[frozenset[tuple], tuple]:
    """Convert desbordante MD object to comparable key."""
    desc = md.get_description()
    lhs_tuples = []
    for lhs in desc.lhs:
        boundary = lhs.decision_boundary
        metric = _normalize_metric(lhs.column_match_description.column_match_name)
        left_idx = lhs.column_match_description.left_column_description.column_index
        right_idx = lhs.column_match_description.right_column_description.column_index
        max_inv = lhs.max_invalid_bound if hasattr(lhs, "max_invalid_bound") else None
        lhs_tuples.append((metric, left_idx, right_idx, round(boundary, 10), max_inv))
    rhs = desc.rhs
    rhs_tuple = (
        _normalize_metric(rhs.column_match_description.column_match_name),
        rhs.column_match_description.left_column_description.column_index,
        rhs.column_match_description.right_column_description.column_index,
        round(rhs.decision_boundary, 10),
        rhs.max_invalid_bound if hasattr(rhs, "max_invalid_bound") else None,
    )
    return frozenset(lhs_tuples), rhs_tuple


def _nar_side_to_frozenset(side_items: list) -> frozenset:
    """Convert NAR side (lhs or rhs items) to comparable frozenset."""
    result = []
    for item in side_items:
        if item.type == "string":
            result.append((item.index, "string", tuple(sorted(item.values))))
        elif item.type == "integer":
            result.append((item.index, "integer", (item.range[0], item.range[1])))
        elif item.type == "float":
            result.append(
                (
                    item.index,
                    "float",
                    (round(item.range[0], 10), round(item.range[1], 10)),
                )
            )
    return frozenset(result)


def nar_to_key_from_item(item) -> tuple:
    """Convert NarTaskResultItemSchema to comparable key."""
    lhs_set = _nar_side_to_frozenset(item.lhs_items)
    rhs_set = _nar_side_to_frozenset(item.rhs_items)
    return (
        lhs_set,
        rhs_set,
        round(item.support, 10),
        round(item.confidence, 10),
        round(item.fitness, 10),
    )


def nar_to_key_from_desbordante(nar) -> tuple:
    """Convert desbordante NAR object to comparable key."""
    from desbordante.nar import (
        FloatValueRange,
        IntValueRange,
        StringValueRange,
    )

    def side_to_frozenset(side: dict) -> frozenset:
        result = []
        for idx, val in side.items():
            if isinstance(val, StringValueRange):
                result.append((idx, "string", tuple(sorted(val.string))))
            elif isinstance(val, IntValueRange):
                result.append((idx, "integer", (val.lower_bound, val.upper_bound)))
            elif isinstance(val, FloatValueRange):
                result.append(
                    (
                        idx,
                        "float",
                        (round(val.lower_bound, 10), round(val.upper_bound, 10)),
                    )
                )
        return frozenset(result)

    return (
        side_to_frozenset(nar.ante),
        side_to_frozenset(nar.cons),
        round(nar.support, 10),
        round(nar.confidence, 10),
        round(nar.fitness, 10),
    )


def load_tabular_dataset_from_csv(
    path: str | Path,
    *,
    sep: str = ",",
    has_header: bool = True,
    columns: list[str] | None = None,
) -> TabularDownloadedDatasetSchema:
    """Load CSV file into TabularDownloadedDatasetSchema."""
    df = pd.read_csv(path, sep=sep, header=0 if has_header else None)
    if columns is not None:
        df = df[columns]
    separator = (
        DatasetSeparator(sep)
        if sep in {s.value for s in DatasetSeparator}
        else DatasetSeparator.COMMA
    )
    return TabularDownloadedDatasetSchema(
        df=df,  # type: ignore
        params=TabularDatasetParams(
            has_header=has_header,
            separator=separator,
        ),
        info=TabularDatasetInfo(
            number_of_columns=df.shape[1],
            number_of_rows=len(df),
            column_names=list(df.columns.astype(str)),
        ),
    )


def load_transactional_dataset_from_csv(
    path: str | Path,
    *,
    sep: str = ",",
    has_header: bool = False,
    itemset_format: Literal["tabular", "singular"] = "tabular",
    has_transaction_id: bool = False,
    id_column: int = 0,
    itemset_column: int = 1,
) -> TransactionalDownloadedDatasetSchema:
    """Load CSV file into TransactionalDownloadedDatasetSchema."""
    df = pd.read_csv(path, sep=sep, header=0 if has_header else None)
    object_cols = df.select_dtypes(include=["object"])
    unique_values = [
        str(v) for v in object_cols.stack().unique() if pd.notna(v) and str(v).strip()
    ]
    separator = (
        DatasetSeparator(sep)
        if sep in {s.value for s in DatasetSeparator}
        else DatasetSeparator.COMMA
    )
    if itemset_format == "tabular":
        transactional_params = TabularTransactionalParams(
            itemset_format="tabular",
            has_transaction_id=has_transaction_id,
        )
    elif itemset_format == "singular":
        transactional_params = SingularTransactionalParams(
            itemset_format="singular",
            id_column=id_column,
            itemset_column=itemset_column,
        )
    else:
        raise ValueError(f"Unsupported itemset_format: {itemset_format}")
    return TransactionalDownloadedDatasetSchema(
        df=df,
        params=TransactionalDatasetParams(
            has_header=has_header,
            separator=separator,
            transactional_params=transactional_params,
        ),
        info=TransactionalDatasetInfo(
            number_of_columns=df.shape[1],
            number_of_rows=len(df),
            column_names=list(df.columns.astype(str)),
            unique_values=unique_values,
        ),
    )

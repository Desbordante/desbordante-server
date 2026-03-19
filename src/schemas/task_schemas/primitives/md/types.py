from enum import StrEnum, auto


class ColumnMatchMetric(StrEnum):
    LCS = auto()
    LEVENSHTEIN = auto()
    MONGE_ELKAN = auto()
    EQUALITY = auto()
    DATE_DIFFERENCE = auto()
    NUMBER_DIFFERENCE = auto()
    JACCARD = auto()

from enum import StrEnum, auto


class ColumnMatchMetrics(StrEnum):
    Lcs = auto()
    Levenshtein = auto()
    MongeElkan = auto()
    Equality = auto()
    LVNormDateDistance = auto()
    LVNormNumberDistance = auto()
    Jaccard = auto()

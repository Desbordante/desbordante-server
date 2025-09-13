from enum import StrEnum, auto


class ColumnMatchMetric(StrEnum):
    Lcs = auto()
    Levenshtein = auto()
    Monge_Elkan = auto()
    Equality = auto()
    Date_Difference = auto()
    Number_Difference = auto()
    Jaccard = auto()

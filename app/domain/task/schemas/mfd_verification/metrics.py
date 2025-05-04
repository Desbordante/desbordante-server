from enum import StrEnum, auto


class Metrics(StrEnum):
    Euclidean = auto()
    Cosine = auto()
    Levenshtein = auto()


class MetricAlgorith(StrEnum):
    Brute = auto()
    Approx = auto()
    Calipers = auto()

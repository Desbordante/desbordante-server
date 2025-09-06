from enum import StrEnum, auto


class MfdVerificationMetrics(StrEnum):
    Euclidean = auto()
    Cosine = auto()
    Levenshtein = auto()


class MfdVerificationMetricAlgorithm(StrEnum):
    Brute = auto()
    Approx = auto()
    Calipers = auto()

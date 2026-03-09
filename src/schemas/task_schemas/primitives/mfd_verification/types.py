from enum import StrEnum, auto


class MfdVerificationMetric(StrEnum):
    EUCLIDEAN = auto()
    COSINE = auto()
    LEVENSHTEIN = auto()


class MfdVerificationMetricAlgorithm(StrEnum):
    BRUTE = auto()
    APPROX = auto()
    CALIPERS = auto()

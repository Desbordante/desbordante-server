from enum import StrEnum, auto


class MFDVerificationMetrics(StrEnum):
    Euclidean = auto()
    Cosine = auto()
    Levenshtein = auto()


class MFDVerificationMetricAlgorithm(StrEnum):
    Brute = auto()
    Approx = auto()
    Calipers = auto()

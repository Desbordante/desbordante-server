class IncorrectAlgorithmName(Exception):
    def __init__(self, algo: str, primitive: str):
        super().__init__(f"{algo} is incorrect {primitive} algorithm name")

class IncorrectAFDAlgorithmName(Exception):
    def __init__(self, message: str):
        super().__init__(f"{message} is incorrect afd algorithm name")

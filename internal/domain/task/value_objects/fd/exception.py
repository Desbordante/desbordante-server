class IncorrectFDAlgorithmName(Exception):
    def __init__(self, message: str):
        super().__init__(f"{message} is incorrect fd algorithm name")

from enum import Enum


class FileFormat(str, Enum):
    """Supported file formats"""

    CSV = "csv"
    DOT = "dot"

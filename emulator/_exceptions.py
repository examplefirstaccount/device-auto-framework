class MemucIndexException(Exception):
    """Memuc index exception class"""

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


class MemucRunException(Exception):
    """Memuc run exception class"""

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)

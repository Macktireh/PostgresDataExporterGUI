

class DBConnectionException(Exception):
    def __init__(self, message) -> None:
        self.message = message

class DBQueryException(Exception):
    def __init__(self, message) -> None:
        self.message = message


class ExportCSVException(Exception):
    def __init__(self, message) -> None:
        self.message = message


class SaveImageException(Exception):
    def __init__(self, message) -> None:
        self.message = message

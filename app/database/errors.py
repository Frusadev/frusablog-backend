ELEMENT_NOT_FOUND = 10
UNABLE_TO_CREATE_ELEMENT = 11


class ElementNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UnableToCreateElementError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

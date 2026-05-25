class SignException(Exception):
    def __init__(self, message: str) -> None:
        self._message = message

    def __str__(self) -> str:
        return self._message

class SignInValidationError(SignException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
    
class UserNotFoundError(SignException):
    def __init__(self, message: str, id: str, password: str) -> None:
        super().__init__(message)
        self.__id = id
        self.__password = password
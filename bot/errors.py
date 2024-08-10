class CustomError(Exception):
    pass


class UserAlreadyExistsError(CustomError):
    pass


class UserNotFoundError(CustomError):
    pass


class AIModelNotFoundError(CustomError):
    pass

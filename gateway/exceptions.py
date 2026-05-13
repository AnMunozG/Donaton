class BffError(Exception):
    def __init__(self, message: str, status: int = 400):
        self.message = message
        self.status = status
        super().__init__(message)

class NotFoundError(BffError):
    def __init__(self, message="Recurso no encontrado"):
        super().__init__(message, status=404)

class ValidationError(BffError):
    def __init__(self, message):
        super().__init__(message, status=422)

class AuthError(BffError):
    def __init__(self, message="No autorizado"):
        super().__init__(message, status=401)

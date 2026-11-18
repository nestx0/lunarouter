class LunaError(Exception):
    """Excepción base para todos los errores de la aplicación."""

    default_message: str = "Unexpected error using the API"
    default_code: int = 0

    def __init__(
        self,
        message: str | None = None,
        error_code: int | None = None,
    ) -> None:
        self.message = message or self.default_message
        self.error_code = error_code if error_code is not None else self.default_code
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"[Error {self.error_code}] {self.message}"


class BadRequestError(LunaError):
    """Se lanza cuando la petición no es válida."""

    default_message = "API request is not correct (check payload and headers)"
    default_code = 1


class ContextWindowExceededError(LunaError):
    """Se lanza cuando se supera el límite de tokens del contexto."""

    default_message = "Context window is full"
    default_code = 2


class TokenLimitReached(LunaError):
    default_message = "Not enough tokens to complete the message"
    default_code = 3

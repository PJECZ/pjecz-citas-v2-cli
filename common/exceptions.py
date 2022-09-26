"""
Lib Exceptions
"""


class CLIAnyError(Exception):
    """Excepcion base para todas las excepciones del CLI"""


class CLIAuthenticationError(CLIAnyError):
    """Excepcion porque falla la autenticacion"""


class CLIConfigurationError(CLIAnyError):
    """Excepcion porque falta algo en la configuracion"""


class CLIConnectionError(CLIAnyError):
    """Excepcion porque falla la comunicacion o no llega la respuesta"""


class CLINoDataWarning(CLIAnyError):
    """Excepcion porque lo que llega no es lo esperado"""


class CLIRequestError(CLIAnyError):
    """Excepcion porque el status code no es 200"""


class CLIResponseError(CLIAnyError):
    """Excepcion porque lo que llega no es lo esperado"""


class CLIStatusCodeError(CLIAnyError):
    """Excepcion porque el status code no es 200"""

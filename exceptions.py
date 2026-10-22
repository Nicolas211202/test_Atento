class APIerror(Exception):
    """Error base de la integración con la API."""
    pass

class APIConnectionError(APIerror):
    """Error de conexión con la API."""
    pass

class APIRequestError(APIerror):
    """Error en la solicitud a la API."""
    pass

class NotFoundError(APIerror):
    """Error cuando no se encuentra el recurso solicitado."""
    pass

class APIResponseError(APIerror):
    """Error en la respuesta de la API."""
    pass


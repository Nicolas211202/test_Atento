import requests
import logging
from exceptions import APIConnectionError, APIRequestError, NotFoundError
Base_URL = "https://rickandmortyapi.com/api"
logger = logging.getLogger(__name__)

class RickAndMortyClient:
    def __init__(self, base_url: str = Base_URL,timeout: int=10):
        self.base_url = base_url
        self.timeout = timeout
        
    def _get(self, path: str, params: dict = None) -> dict:
        url = f"{self.base_url}{path}"
        logger.debug("Realizando solicitud GET a la URL: %s con parámetros: %s", url, params)
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
        except requests.exceptions.Timeout as exc:
            raise APIConnectionError(f"Tiempo de espera agotado al intentar conectarse a la API: {exc}")

        except requests.exceptions.RequestException as exc: 
            raise APIRequestError(f"Error en la solicitud a la API: {exc}") from exc
        
        if response.status_code == 404:
            raise NotFoundError(f"Sin resultado")
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise APIRequestError(f"El API respondio con error HTTP: {response.status_code}") from exc
        
        
        try:
            data = response.json()
        except ValueError as exc:
            raise APIRequestError("La respuesta de la API no es un JSON válido") from exc
        
        if not isinstance(data, dict):
            raise APIRequestError("La respuesta de la API en formanto no esperado")
        return data
        
           
    def get_character(self, character_id: int) -> dict:
        return self._get(f"/character/{character_id}")
    
    def get_characters(self, page: int = 1,**filters) -> dict:
        params = {key: value for key, value in filters.items() if value}
        params["page"] = page
        return self._get("/character", params=params)
        
if __name__ == "__main__":
    client = RickAndMortyClient()
    data = client.get_character() 
    print("Total de personajes:", data['info']['count'])
    print("Total de páginas:", data['info']['pages'])   
    print("Primer personaje:", data['results'][0]['name'])
    
    
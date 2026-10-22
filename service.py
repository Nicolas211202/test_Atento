import logging

from client import RickAndMortyClient
from exceptions import APIConnectionError, APIRequestError, NotFoundError
from models import Character

logger = logging.getLogger(__name__)

class CharacterService:
    """Logica de busqueda: usa el cliente y entrega modelos listos para mostrar."""
    
    def __init__(self, client: RickAndMortyClient, max_pages: int = 5):
        self.client = client
        self.max_pages = max_pages #5 paginas hasta 100 personajes
        
    def get_by_id(self, character_id: int) -> Character:
        return Character.from_api(self.client.get_character(character_id))
    
    def search(self, character_id: int = None, name: str = None, status: str = None, species: str = None, gender: str = None) -> list[Character]:
        characters: list[Character] = []
        page = 1
        while page <= self.max_pages:
            try:
                data = self.client.get_characters(page=page, name=name, status=status, species=species, gender=gender)
            except NotFoundError:
                #la API responde 404 cuando ninun persoaje coincide
                logger.info("No se encontraron personajes con los criterios de busqueda")
                return characters
            
            if data is None:
                return characters
            
            results = data.get("results")
            if not isinstance(results, list):
                raise APIRequestError("La respuesta de la API no contiene una lista de resultados")
            
            characters.extend(Character.from_api(character) for character in results)
            
            if not data.get("info") or not data["info"].get("next"):
                break
            page += 1
        return characters
import requests
Base_URL = "https://rickandmortyapi.com/api"

class RickAndMortyClient:
    def __init__(self, base_url: str = Base_URL,timeout: int=10):
        self.base_url = base_url
        self.timeout = timeout
        
    def get_character(self, page: int = 1):
        response = requests.get(f"{self.base_url}/character", params={"page": page}, timeout=self.timeout)
        
        response.raise_for_status()
        return response.json()
    
if __name__ == "__main__":
    client = RickAndMortyClient()
    data = client.get_character() 
    print("Total de personajes:", data['info']['count'])
    print("Total de páginas:", data['info']['pages'])   
    print("Primer personaje:", data['results'][0]['name'])
    
    
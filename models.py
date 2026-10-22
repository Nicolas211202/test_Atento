from dataclasses import dataclass

from exceptions import APIResponseError

@dataclass
class Character:
    id: int
    name: str
    status: str
    species: str
    gender: str
    @classmethod
    def from_api(cls, data: dict) -> "Character":
        try:
            return cls(
                id=data["id"],
                name=data["name"],
                status=data["status"],
                species=data["species"],
                gender=data["gender"]
            )
        except KeyError as e:
            raise APIResponseError(f"Falta la clave esperada en la respuesta de la API: {e}")
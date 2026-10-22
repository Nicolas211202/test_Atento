import argparse
import logging
import sys
from consulta import RickAndMortyClient
from exceptions import APIConnectionError, NotFoundError , APIerror
from models import Character
from service import CharacterService

logger = logging.getLogger("app")
def build_parser()-> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rick and Morty API Client")
    parser.add_argument("--character_id", type=int, help="ID del personaje para obtener detalles específicos")
    parser.add_argument("--page", type=int, default=1, help="Numero de página para obtener la lista de personajes")
    parser.add_argument("--name", type=str, help="Filtrar personajes por nombre")
    parser.add_argument("--status", type=str, choices=["alive", "dead", "unknown"], help="Filtrar personajes por estado")
    parser.add_argument("--species", type=str, help="Filtrar personajes por especie")
    parser.add_argument("--debug", action="store_true", help="Habilitar modo de depuración")
    parser.add_argument("--gender", type=str, choices=["female", "male", "genderless", "unknown"], help="Filtrar personajes por género")
    return parser



def has_criteria(args)-> bool:
    return any([args.name, args.status, args.species, args.gender, args.character_id])




def ask(args)-> None:
    print("Criterios de búsqueda:")
    id_text = input("Ingrese el ID del personaje (o presione Enter para omitir): ").strip()
    args.character_id = int(id_text) if id_text.isdigit() else None
    args.name = input("Ingrese el nombre del personaje (o presione Enter para omitir): ").strip() or None
    args.status = input("Ingrese el estado del personaje (o presione Enter para omitir): ").strip().lower() or None
    args.species = input("Ingrese la especie del personaje (o presione Enter para omitir): ").strip() or None
    args.gender = input("Ingrese el género del personaje (o presione Enter para omitir): ").strip().lower() or None
    
    
def print_character(c: Character)-> None:
    print(f"[{c.id}] {c.name}")
    print(f"  Estado: {c.status}")
    print(f"  Especie: {c.species}")
    print(f"  Género: {c.gender}")
    




def main()-> int:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.WARNING,
        format="%(levelname)s - %(message)s",
    )

    if not has_criteria(args):
        ask(args)
        
    if not has_criteria(args):
        parser.error("Debe indicar al menos un criterio de búsqueda: --character_id, --name, --status, --species o --gender")

    service = CharacterService(RickAndMortyClient())
    try:
        if args.character_id:
            print_character(service.get_by_id(args.character_id))
            return 0
            
        results = service.search(args.character_id, args.name, args.status, args.species, args.gender)
        if not results:
            print("No se encontraron personajes con los criterios especificados.")
            return 0
        
        print(f"Se encontraron {len(results)} personajes(s):\n")
        for character in results:
            print_character(character)
        return 0
    
    

    except NotFoundError:
        print("No se encontraron personajes con los criterios de búsqueda.")
        return 1
    
    except APIConnectionError as exc:
        logger.error("Error de conexión con la API: %s", exc)
        return 1
    
    except APIConnectionError as exc:
        logger.error("Error de conexión con la API: %s", exc)
        return 2
    
    except APIerror as exc:
        logger.error("Error en la solicitud a la API: %s", exc)
        return 3
    
    
if __name__ == "__main__":
    sys.exit(main())
    
# test_Atento — Cliente CLI de Rick and Morty

Aplicación de línea de comandos en Python para consultar personajes de la [Rick and Morty API](https://rickandmortyapi.com/). Permite buscar un personaje por ID o filtrar por nombre, estado, especie y género.

## Requisitos

- Python 3.13 (el entorno virtual incluido usa 3.13)
- [`requests`](https://pypi.org/project/requests/)

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate
pip install requests
```

## Uso

Debe indicarse al menos un criterio de búsqueda. Si se ejecuta sin argumentos, el programa pide los criterios de forma interactiva.

```bash
# Por ID
python main.py --character_id 1

# Por filtros (combinables)
python main.py --name rick --status alive
python main.py --species human --gender female

# Modo interactivo
python main.py

# Con logs de depuración
python main.py --name morty --debug
```

### Opciones

| Opción | Descripción |
|---|---|
| `--character_id` | ID del personaje (devuelve el detalle de uno solo) |
| `--name` | Filtrar por nombre |
| `--status` | `alive`, `dead` o `unknown` |
| `--species` | Filtrar por especie |
| `--gender` | `female`, `male`, `genderless` o `unknown` |
| `--page` | Número de página (por defecto 1) |
| `--debug` | Activa el log en nivel DEBUG |

### Ejemplo de salida

```
Se encontraron 2 personajes(s):

[1] Rick Sanchez
  Estado: Alive
  Especie: Human
  Género: Male
```

### Códigos de salida

| Código | Significado |
|---|---|
| `0` | Ejecución correcta |
| `1` | Sin resultados, o error de conexión (timeout) |
| `3` | Error de la solicitud o respuesta de la API |

## Estructura del proyecto

| Archivo | Rol |
|---|---|
| `main.py` | Punto de entrada: parser de argumentos, modo interactivo, impresión y manejo de errores |
| `consulta.py` | Cliente HTTP (`RickAndMortyClient`) con manejo de timeout, 404, errores HTTP y JSON inválido |
| `service.py` | `CharacterService`: lógica de búsqueda y paginación (máx. 5 páginas, ~100 personajes) |
| `models.py` | Modelo `Character` (dataclass) y validación de la respuesta |
| `exceptions.py` | Jerarquía de excepciones (`APIerror` y derivadas) |
| `client.py` | Versión inicial/simple del cliente (solo `get_character` paginado) |

## Arquitectura

```
main.py  ──►  CharacterService  ──►  RickAndMortyClient (consulta.py)  ──►  API
                    │
                    └──►  Character.from_api (models.py)
```

Los errores se traducen a excepciones propias (`APIConnectionError`, `APIRequestError`, `NotFoundError`, `APIResponseError`) que `main.py` convierte en mensajes y códigos de salida.

## Notas conocidas

- `main.py` usa el cliente de `consulta.py`; `client.py` quedó como versión anterior y solo se importa en `service.py` para tipado.
- En `main.py` el bloque `except APIConnectionError` aparece duplicado, por lo que el código de salida `2` nunca se alcanza.
- El bloque de prueba al final de `consulta.py` llama a `get_character()` sin ID y fallaría si se ejecuta directamente.
- `--page` se define en el parser pero la búsqueda actual siempre recorre desde la página 1.

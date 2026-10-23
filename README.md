# Rick and Morty CLI

Cliente de línea de comandos desarrollado en Python para consultar personajes de la [Rick and Morty API](https://rickandmortyapi.com/). Permite obtener un personaje por su identificador o buscar coincidencias mediante filtros combinables, desde la terminal o mediante un modo interactivo.

## Funcionalidades

- Consulta de personajes por ID.
- Búsqueda por nombre, estado, especie y género.
- Modo interactivo cuando no se proporcionan criterios de búsqueda.
- Recorrido automático de hasta cinco páginas por búsqueda.
- Presentación del ID, nombre, estado, especie y género de cada personaje.
- Manejo de errores de la API y registro de depuración opcional.

## Requisitos

- Python 3.13, versión utilizada en el entorno de desarrollo.
- La biblioteca `requests`.
- Conexión a Internet para realizar las consultas.

## Instalación

Desde la carpeta raíz del proyecto, crea un entorno virtual:

```console
python -m venv .venv
```

Actívalo según tu sistema operativo y terminal:

| Entorno | Comando |
| --- | --- |
| Windows · PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows · CMD | `.venv\Scripts\activate.bat` |
| macOS / Linux · Bash o Zsh | `source .venv/bin/activate` |

Instala la dependencia:

```console
python -m pip install requests
```

## Uso

Ejecuta los comandos desde la raíz del proyecto, con el entorno virtual activo.

### Consultar por ID

```console
python main.py --character_id 1
```

Salida de ejemplo:

```text
[1] Rick Sanchez
  Estado: Alive
  Especie: Human
  Género: Male
```

### Buscar con filtros

Los filtros se pueden combinar para acotar los resultados:

```console
python main.py --name rick --status alive
python main.py --species human --gender female
python main.py --name "Morty Smith"
```

Si se proporciona un ID junto con otros filtros, la consulta por ID tiene prioridad.

### Modo interactivo

```console
python main.py
```

El programa solicita los criterios de búsqueda. Presiona `Enter` para omitir un campo; debes completar al menos uno. Para estado y género, utiliza los valores en inglés indicados en la tabla de opciones.

### Ayuda y depuración

```console
python main.py --help
python main.py --name morty --debug
```

## Opciones disponibles

| Opción | Descripción | Valores / comportamiento |
| --- | --- | --- |
| `--character_id` | Consulta un personaje por ID. | Número entero. Tiene prioridad sobre los filtros. |
| `--name` | Filtra por nombre. | Texto; usa comillas si contiene espacios. |
| `--status` | Filtra por estado. | `alive`, `dead`, `unknown`. |
| `--species` | Filtra por especie. | Texto, por ejemplo `human`. |
| `--gender` | Filtra por género. | `female`, `male`, `genderless`, `unknown`. |
| `--page` | Parámetro de página declarado en la CLI. | Por defecto `1`; actualmente no modifica la búsqueda. |
| `--debug` | Activa los registros de depuración. | Bandera sin valor adicional. |
| `-h`, `--help` | Muestra la ayuda del programa. | Finaliza sin consultar la API. |

## Estructura del proyecto

```text
test_Atento/
├── main.py          # Entrada de la CLI y presentación de resultados
├── consulta.py      # Cliente HTTP utilizado por la aplicación
├── service.py       # Consultas y recorrido de páginas
├── models.py        # Modelo de datos Character
├── exceptions.py    # Excepciones de la integración
├── client.py        # Implementación inicial del cliente
└── README.md
```

### Flujo de una consulta

```text
main.py → CharacterService → RickAndMortyClient → Rick and Morty API
                 ↓
          Character.from_api
```

`main.py` procesa los argumentos o solicita datos al usuario. `CharacterService` coordina las consultas y convierte las respuestas en objetos `Character`. El cliente de `consulta.py` realiza las solicitudes HTTP, con un tiempo de espera de 10 segundos por solicitud, y traduce los errores a excepciones propias.

## Códigos de salida

| Código | Significado |
| --- | --- |
| `0` | Consulta completada, incluida una búsqueda por filtros sin coincidencias. |
| `1` | Personaje por ID no encontrado o tiempo de espera agotado. |
| `2` | Error de argumentos o ausencia de criterios después del modo interactivo. |
| `3` | Error de solicitud HTTP o de procesamiento de la respuesta de la API. |

## Limitaciones actuales

- Las búsquedas por filtros comienzan en la página 1 y consultan como máximo cinco páginas; pueden devolver solo una parte de las coincidencias. El argumento `--page` todavía no está conectado a este flujo.
- `client.py` conserva una implementación anterior. La aplicación utiliza `consulta.py`, aunque la anotación de tipo en `service.py` referencia el cliente anterior.
- `main.py` contiene un bloque duplicado para `APIConnectionError`; el segundo bloque no se ejecuta. Los tiempos de espera devuelven actualmente el código `1`.
- El bloque de ejecución directa de `consulta.py` requiere ajustes: llama a `get_character()` sin el ID obligatorio. Para utilizar la aplicación, ejecuta `main.py`.

## Referencia

Los datos de los personajes provienen de la [Rick and Morty API](https://rickandmortyapi.com/).

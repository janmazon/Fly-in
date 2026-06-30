*This project has been created as part of the 42 curriculum by jcamarer.*

# Fly-in

## Descripción

**Fly-in** es una simulación de enrutamiento de drones escrita en Python. El objetivo del proyecto es trasladar una flota de drones desde una zona `start_hub` hasta una zona `end_hub`, a través de una red de zonas conectadas (un grafo), en el menor número posible de turnos de simulación, respetando un conjunto de reglas de movimiento y de capacidad.

El mapa (el grafo de zonas y conexiones) se describe mediante un archivo de texto con un formato propio, que se parsea y se transforma en una representación interna totalmente orientada a objetos. Cada zona puede tener un tipo (`normal`, `restricted`, `priority`, `blocked`) que afecta al coste de atravesarla, así como un número máximo de drones que puede contener simultáneamente. Cada conexión entre dos zonas también puede limitar cuántos drones pueden circular por ella al mismo tiempo.

Una vez cargado el mapa, un buscador de caminos basado en el algoritmo A* calcula la mejor ruta para cada drone, teniendo en cuenta el coste de las zonas, sus capacidades y el estado en tiempo real de la simulación. A continuación, un motor de simulación por turnos mueve a cada drone paso a paso, gestionando las esperas, los conflictos de capacidad y los tránsitos de varios turnos a través de zonas restringidas, hasta que todos los drones llegan a la zona final. Una interfaz gráfica con Tkinter muestra el mapa y el movimiento de los drones en tiempo real.

### Características principales

- Parser de mapas personalizado, con mensajes de error detallados y precisos (indicando la línea exacta del fallo).
- Diseño totalmente orientado a objetos (`Graph`, `Zone`, `Connection`, `Drone`, `Pathfinder`, `Simulation`, `Visualizer`).
- Pathfinding mediante A*, que tiene en cuenta los costes de movimiento según el tipo de zona (`normal`, `restricted`, `priority`) y evita por completo las zonas `blocked`.
- Motor de simulación turno a turno que aplica las reglas de ocupación de zonas y de capacidad de las conexiones.
- Representación visual gráfica del mapa y del movimiento de los drones mediante Tkinter.
- Tipado estricto y obligatorio (type hints en todo el proyecto), validado con `mypy`.
- Estilo de código validado con `flake8`.
- No se utiliza ninguna librería externa de grafos (ni `networkx`, ni `graphlib`, etc.) — toda la lógica de grafos está implementada desde cero.

## Instrucciones

### Requisitos

- Python 3.10 o superior.
- `flake8` y `mypy` para el linting (ver `requirements.txt`).

### Instalación

```bash
make install
```

Este comando instala las dependencias de desarrollo del proyecto (`flake8`, `mypy`) listadas en `requirements.txt`.

### Ejecutar la simulación

```bash
make run
```

o directamente:

```bash
python3 flyin.py <map.txt>
```

Donde `<map.txt>` es la ruta a un archivo de mapa que siga el formato descrito más abajo (puedes ver `simple_map.txt` como ejemplo). El programa imprime, turno a turno, los movimientos realizados por cada drone; al finalizar, imprime el número total de turnos y abre una ventana gráfica que muestra la simulación.

### Depuración

```bash
make debug
```

Ejecuta el script principal usando el depurador integrado de Python (`pdb`).

### Linting

```bash
make lint
```

Ejecuta `flake8 .` y `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`.

```bash
make lint-strict
```

Ejecuta `flake8 .` y `mypy . --strict` para una verificación más estricta (opcional).

### Limpieza

```bash
make clean
```

Elimina los archivos temporales y las cachés (`__pycache__`, `.mypy_cache`, etc.).

### Formato del archivo de mapa

```
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]

connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```

- La primera línea (sin contar comentarios) debe definir el número de drones con `nb_drones: <entero_positivo>`.
- Las zonas se declaran con `start_hub:`, `end_hub:` o `hub:`, seguido de un nombre único, las coordenadas enteras `x` e `y`, y metadatos opcionales entre corchetes (`zone`, `color`, `max_drones`).
- Las conexiones se declaran con `connection: <zona1>-<zona2>` y un metadato opcional `max_link_capacity`.
- Las líneas que empiezan por `#` son comentarios y se ignoran.

### Tipos de zona

| Tipo | Coste de movimiento | Descripción |
|---|---|---|
| `normal` | 1 turno (por defecto) | Zona estándar, sin restricciones. |
| `restricted` | 2 turnos | Zona sensible o peligrosa; el drone tarda 2 turnos en atravesarla y, una vez ha empezado el tránsito, debe llegar obligatoriamente en el turno siguiente (no puede esperar a mitad de camino). |
| `priority` | 1 turno | Zona preferente; cuesta lo mismo que una zona normal, pero el pathfinder la prioriza. |
| `blocked` | — | Zona inaccesible; ningún camino puede pasar por ella. |

## Descripción del algoritmo y estrategia de implementación

- **Representación del grafo (`graph.py`)**: `Zone`, `Connection` y `Graph` son clases de datos simples y autocontenidas, construidas sin ninguna librería externa de grafos, cumpliendo así con la restricción del enunciado de no usar librerías como `networkx` o `graphlib`.

- **Parseo (`parser.py`)**: la clase `MapParser` lee el archivo de mapa línea a línea, validando estrictamente el formato y lanzando un `ParseError` con el número de línea y un mensaje claro ante cualquier entrada incorrecta (zonas duplicadas, metadatos inválidos, hubs ausentes o duplicados, conexiones que referencian zonas inexistentes, conexiones duplicadas, etc.).

- **Pathfinding (`pathfinder.py`)**: la clase `Pathfinder` implementa el algoritmo de búsqueda A*. El coste de entrar en una zona depende de su tipo (`restricted` cuesta más, `priority` cuesta menos, `blocked` nunca se explora), y la heurística utilizada es la distancia de Manhattan hasta el hub final. El algoritmo también tiene en cuenta el tráfico actual de cada conexión, de modo que las rutas evitan de forma natural los enlaces congestionados.

- **Comportamiento de los drones (`drone.py`)**: cada `Drone` mantiene su zona actual, su camino planificado, y el estado de cualquier tránsito en curso de varios turnos a través de una zona restringida. En cada turno, un drone intenta avanzar por su camino respetando la capacidad de zonas y conexiones; si no puede moverse, espera.

- **Motor de simulación (`simulation.py`)**: la clase `Simulation` dirige todo el proceso turno a turno. Los drones sin camino asignado solicitan uno al `Pathfinder`. Si un drone permanece bloqueado durante demasiado tiempo, su camino se descarta para que pueda recalcularse, lo cual ayuda a resolver congestiones locales y evitar bloqueos (deadlocks). Todos los movimientos realizados en un turno se imprimen en el formato requerido `D<ID>-<zona>` / `D<ID>-<conexión>`.

- **Complejidad y rendimiento**: en cada turno, el pathfinder se ejecuta (en el peor caso) con una complejidad de `O(E log V)` aproximada gracias a A* (donde `E` es el número de conexiones y `V` el de zonas), y solo se recalcula el camino de un drone cuando no tiene uno asignado o cuando ha quedado bloqueado, evitando recálculos innecesarios en cada turno. El uso de memoria es proporcional al número de zonas, conexiones y drones activos, sin estructuras adicionales costosas.

- **Visualización (`visualizer.py`)**: la clase `Visualizer` utiliza Tkinter para dibujar las zonas (como círculos de colores, usando el color declarado de cada zona), las conexiones (como líneas) y los drones (como pequeños marcadores numerados), refrescando el canvas después de cada turno de simulación. Esto permite observar en tiempo real cómo se distribuyen los drones por la red, cómo se forman (o evitan) las congestiones, y cómo el algoritmo de pathfinding va adaptando las rutas, lo que facilita mucho la comprensión del comportamiento del sistema durante la evaluación entre pares.

## Recursos

- [PEP 257 — Convenciones de docstrings](https://peps.python.org/pep-0257/)
- [Documentación del módulo `typing` de Python](https://docs.python.org/3/library/typing.html)
- [Documentación de mypy](https://mypy.readthedocs.io/)
- [Documentación de flake8](https://flake8.pycqa.org/)
- [Algoritmo de búsqueda A* — resumen](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Documentación de Tkinter](https://docs.python.org/3/library/tkinter.html)

### Uso de IA

Durante este proyecto se utilizó IA (Claude) como herramienta de apoyo y revisión, no como sustituto de la comprensión del código:

- Revisión y discusión de la estructura de la implementación de A* en `pathfinder.py` (función de coste, elección de la heurística), para asegurar que reflejaba correctamente las reglas de coste por tipo de zona del enunciado.
- Ayuda para depurar casos límite en la lógica de movimiento por turnos en `drone.py` y `simulation.py`, en particular el manejo de los tránsitos de varios turnos a través de zonas `restricted`.
- Revisión del manejo de errores del parser en `parser.py`, para asegurar que cualquier línea mal formada genera un mensaje de error claro y con la línea exacta.
- Apoyo en la redacción y el formato de este `README.md`.

Todas las sugerencias generadas por la IA fueron revisadas, probadas y adaptadas antes de integrarse, siguiendo las directrices de uso de IA del proyecto.

---

**Nota:** el enunciado del proyecto (Fly-in) exige que el `README.md` esté escrito en inglés. Esta versión se ha redactado en español a petición explícita del autor; si la evaluación lo requiere, puede ser necesario aportar también una versión en inglés.
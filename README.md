*Este proyecto ha sido creado como parte del currículo de 42 por jcamarer.*

# Fly-in

## Descripción

**Fly-in** es una simulación de enrutamiento de flotas de drones escrita en Python, desarrollada como proyecto del currículo 42. El objetivo central del programa es trasladar un conjunto de drones desde una zona de partida (`start_hub`) hasta una zona de llegada (`end_hub`), navegando a través de una red de zonas interconectadas representadas como un **grafo**, en el **mínimo número de turnos** posible.

El mapa (la red de zonas y conexiones) se describe mediante un archivo de texto con un formato propio. El programa lo parsea y lo transforma en una representación interna completamente orientada a objetos, sin utilizar ninguna librería externa de grafos (está prohibido el uso de `networkx`, `graphlib`, etc.).

Cada zona de la red puede pertenecer a uno de cuatro tipos, que determinan el coste de movimiento de los drones al atravesarla:

| Tipo | Coste | Descripción |
|---|---|---|
| `normal` | 1 turno | Zona estándar, sin restricciones especiales. |
| `priority` | 1 turno | Zona preferente; el pathfinder la prioriza frente a otras del mismo coste. |
| `restricted` | 2 turnos | Zona peligrosa; el drone tarda 2 turnos en llegar y no puede detenerse a mitad del tránsito. |
| `blocked` | Inaccesible | Ningún drone puede entrar ni atravesarla. Cualquier ruta que la use es inválida. |

Además, tanto las zonas como las conexiones entre ellas tienen **capacidades**: una zona puede estar limitada a contener un solo drone a la vez (por defecto), o hasta N drones si se configura con `max_drones=N`; una conexión puede limitarse a un solo drone en tránsito simultáneo (por defecto) o más con `max_link_capacity=N`. El `start_hub` y el `end_hub` son excepciones: pueden contener cualquier número de drones.

Teniendo esto en cuenta, el programa:
1. **Parsea** el archivo de mapa y construye el grafo en memoria, validando el formato con mensajes de error detallados (línea exacta y causa del error).
2. **Calcula rutas** para cada drone usando el algoritmo de búsqueda A*, que tiene en cuenta los costes de las zonas, la heurística y el tráfico en tiempo real de las conexiones.
3. **Simula** el movimiento turno a turno, gestionando esperas, conflictos de capacidad y tránsitos de doble turno por zonas restringidas, hasta que todos los drones llegan al destino.
4. **Visualiza** el proceso en tiempo real mediante una interfaz gráfica con Tkinter.

---

## Instrucciones

### Requisitos previos

- Python 3.10 o superior.
- `flake8` y `mypy` (herramientas de linting, incluidas en `requirements.txt`).
- Tkinter (incluido con Python en la mayoría de sistemas. En Linux puede requerirse instalar `python3-tk`).

```bash
sudo apt install python3-tk
```

### Instalación

Clona el repositorio y ejecuta:

```bash
make install
```

Este comando instala las dependencias de desarrollo del proyecto (`flake8`, `mypy`) listadas en `requirements.txt` usando `pip`.

También puede hacer directamente:

```bash
pip install -r requirements.txt
```

### Ejecución de la simulación

```bash
make run
```

o directamente desde la raíz del proyecto:

```bash
python3 flyin.py <ruta_al_mapa.txt>
```

**Ejemplo con el mapa incluido:**

```bash
python3 flyin.py simple_map.txt
```

El programa:
1. Parsea el mapa indicado.
2. Imprime en consola, turno a turno, los movimientos de cada drone.
3. Imprime el número total de turnos al finalizar.
4. Abre una ventana gráfica con Tkinter mostrando el estado final de la simulación.

### Depuración

```bash
make debug
```

Ejecuta el script principal bajo el depurador integrado de Python (`pdb`), permitiendo inspeccionar el estado del programa paso a paso.

### Linting y verificación de tipos

```bash
make lint
```

Ejecuta `flake8 .` y `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`

```bash
make lint-strict
```

Ejecuta `flake8 .` y `mypy . --strict` para una verificación aún más estricta (opcional pero recomendada).

### Limpieza

```bash
make clean
```

Elimina los archivos temporales y las cachés generadas por Python y mypy (`__pycache__`, `.mypy_cache`, `*.pyc`, etc.).

### Estructura del proyecto

```
.
├── flyin.py              # Punto de entrada del programa
├── Makefile              # Automatización de tareas
├── requirements.txt      # Dependencias de desarrollo
├── simple_map.txt        # Mapa de ejemplo (nivel fácil)
├── README.md             # Este archivo
├── graph.py              # Clases Zone, Connection y Graph
├── parser.py             # Parser del archivo de mapa (MapParser, ParseError)
├── pathfinder.py         # Algoritmo A* (Pathfinder)
├── drone.py              # Lógica de movimiento de cada drone (Drone)
├── simulation.py         # Motor de simulación turno a turno (Simulation)
└── visualizer.py         # Interfaz gráfica Tkinter (Visualizer)
```

### Formato del archivo de mapa

```
# Los comentarios comienzan con '#' y son ignorados
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub:   goal 10 10 [color=yellow]
hub: roof1     3 4 [zone=restricted color=red]
hub: roof2     6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB   7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]

connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```

Reglas del formato:
- La primera línea (sin contar comentarios) debe ser `nb_drones: <entero_positivo>`.
- Las zonas se declaran con `start_hub:`, `end_hub:` o `hub:`, seguido del nombre (sin guiones ni espacios), las coordenadas enteras `x` e `y`, y metadatos opcionales entre corchetes.
- Las conexiones se declaran con `connection: <zona1>-<zona2>` y opcionalmente `[max_link_capacity=N]`.
- Debe haber exactamente un `start_hub` y un `end_hub`.
- Los nombres de zona son únicos y no pueden contener guiones (ya que el guion separa zonas en las conexiones).

---

## Ejemplo de entrada y salida esperada

### Archivo de entrada: `simple_map.txt`

```
# Easy Level 1: Simple linear path
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

Este mapa define una red lineal sencilla: `start → waypoint1 → waypoint2 → goal`, con 2 drones y una capacidad por defecto de 1 drone por zona y por conexión.

### Ejecución

```bash
python3 flyin.py simple_map.txt
```

### Salida esperada en consola

```
D1-waypoint1
D2-waypoint1 D1-waypoint2
D2-waypoint2 D1-goal
D2-goal
4
```

### Interpretación de la salida

| Turno | Salida | Explicación |
|---|---|---|
| 1 | `D1-waypoint1` | D1 avanza a `waypoint1`. D2 no puede moverse porque `waypoint1` ya está ocupado (capacidad 1). |
| 2 | `D2-waypoint1 D1-waypoint2` | D1 sale de `waypoint1` liberando espacio; D2 entra. Ambos se mueven en el mismo turno. |
| 3 | `D2-waypoint2 D1-goal` | D1 llega al destino y queda entregado. D2 avanza. |
| 4 | `D2-goal` | D2 llega al destino. Simulación completada. |
| — | `4` | Número total de turnos. |

El formato de cada línea es `D<ID>-<nombre_zona>`. Los drones que no se mueven en un turno se omiten. Los drones que alcanzan `goal` dejan de aparecer en los turnos siguientes.

### Ejemplo con zona restringida

Si `waypoint1` fuera de tipo `restricted`, el drone tardaría 2 turnos en cruzarla. Durante el primer turno, la salida mostraría el nombre de la **conexión** (no la zona destino), indicando que el drone está en tránsito:

```
D1-start-waypoint1
D1-waypoint1
...
```

---

## Algoritmo y decisiones de diseño

### Visión general

La base del proyecto es el algoritmo **A\*** (*A-star*), implementado en `pathfinder.py`. A* es un algoritmo de búsqueda que encuentra el camino de menor coste entre dos nodos de un grafo, combinando el coste real acumulado desde el origen (`g`) con una estimación heurística del coste restante hasta el destino (`h`). La suma `f = g + h` determina en qué orden se exploran los nodos.

A* garantiza encontrar el camino óptimo siempre que la heurística sea **admisible** (no sobreestime el coste real). En este proyecto se utiliza la **distancia de Manhattan** entre la zona actual y el `end_hub`, lo que es admisible porque el grafo puede tener conexiones en cualquier dirección y el coste mínimo de cualquier movimiento es 1 turno.

### Función de coste

El coste de entrar en una zona vecina se calcula como:

```
coste_al_vecino = coste_real_actual + coste_base + tráfico_actual_de_la_conexión
```

Donde `coste_base` depende del tipo de zona destino:
- `normal` → 1.0
- `priority` → 0.5 (favorece que el pathfinder elija estas zonas)
- `restricted` → 2.0
- `blocked` → nunca se explora (se descarta directamente)

Añadir el tráfico actual de la conexión (`connection.current_traffic`) hace que el pathfinder tienda a evitar rutas congestionadas, distribuyendo mejor la flota.

### Recálculo dinámico de rutas

Los drones no recalculan su ruta en cada turno (lo que sería costoso e innecesario). El `Pathfinder` solo se invoca cuando un drone no tiene camino asignado o cuando ha permanecido bloqueado durante más de un turno seguido. En ese caso, la ruta se descarta y se recalcula teniendo en cuenta el estado actual del grafo (tráfico y ocupación). Este mecanismo permite al sistema adaptarse a congestiones locales y resolver situaciones de bloqueo mutuo (*deadlock*) sin necesidad de lógica adicional.

### Mecánica de zonas restringidas

Cuando el próximo paso de un drone es una zona `restricted`, el movimiento ocupa **2 turnos**:

- **Turno 1**: el drone sale de su zona actual, entra en la conexión y queda "en tránsito" (`transit_timer = 1`). La zona destino queda reservada. La salida imprime el nombre de la conexión (`D1-zonaA-zonaB`).
- **Turno 2**: el drone llega obligatoriamente a la zona restringida, sin posibilidad de detenerse a mitad del tránsito. La zona origen ya no lo cuenta, pero la zona destino debe tener capacidad libre en ese segundo turno.

### Gestión de capacidades

Antes de que un drone intente moverse, se verifican dos condiciones:
1. `connection.current_traffic < connection.max_link_capacity` → la conexión tiene espacio.
2. `next_zone.current_drones < next_zone.max_drones` → la zona destino tiene espacio (excepto si es el `end_hub`).

Los drones que salen de una zona **liberan su espacio en el mismo turno** en que se mueven, lo que permite que otro drone entre en esa misma zona en el mismo turno (siempre que el movimiento sea válido). Esto es esencial para que múltiples drones puedan avanzar simultáneamente en redes con capacidad 1 por zona.

---

## Representación visual

La clase `Visualizer` (en `visualizer.py`) utiliza **Tkinter** para dibujar el estado del mapa y de los drones en una ventana gráfica, que se actualiza en tiempo real después de cada turno de simulación.

### Qué se muestra

- **Conexiones**: dibujadas como líneas grises que unen las zonas. Permiten visualizar la red de un vistazo.
- **Zonas**: dibujadas como círculos de colores. El color de cada zona es el declarado en el archivo de mapa (por ejemplo, `color=green` para el `start_hub`, `color=red` para las zonas restringidas, etc.). Si una zona no tiene color asignado, se dibuja en gris claro. Debajo de cada círculo aparece el nombre de la zona (en mapas con menos de 45 zonas).
- **Drones**: dibujados como pequeños círculos negros con el número de ID del drone en blanco en su interior. Se sitúan sobre la zona en la que se encuentran en ese turno. Si varios drones están en la misma zona, se colocan uno al lado del otro formando una fila, evitando que se solapen.

### Escalado automático

El `Visualizer` calcula automáticamente la escala y el centrado del mapa para que ocupe toda la ventana disponible (que se abre en modo maximizado), independientemente del tamaño o la dispersión de las coordenadas del mapa. Esto hace que la visualización sea igualmente legible tanto para mapas pequeños de 4 nodos como para mapas grandes con decenas de zonas.

### Cómo mejora la comprensión

La representación gráfica aporta un valor significativo durante la simulación y la evaluación:

- **Observación del flujo**: es visible cómo los drones se distribuyen por distintas rutas cuando existen varios caminos, y cómo se forman colas en zonas o conexiones con poca capacidad.
- **Identificación de cuellos de botella**: las zonas donde se acumulan drones durante varios turnos seguidos son visualmente obvias, lo que facilita entender por qué el pathfinder elige ciertas rutas alternativas.
- **Verificación intuitiva**: al poder seguir visualmente cada drone numerado de zona en zona, es fácil comprobar que el algoritmo respeta las reglas de capacidad y los tipos de zona, sin necesidad de leer línea a línea la salida de consola.
- **Depuración**: durante el desarrollo, la ventana gráfica permitió detectar rápidamente situaciones anómalas (drones que no avanzaban, zonas que se saturaban incorrectamente, etc.) que habrían sido muy difíciles de encontrar solo con la salida de texto.

---

## Recursos

- [PEP 257 — Convenciones de docstrings](https://peps.python.org/pep-0257/)
- [Documentación del módulo `typing` de Python](https://docs.python.org/3/library/typing.html)
- [Algoritmo A* — Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Heurísticas admisibles — Wikipedia](https://en.wikipedia.org/wiki/Admissible_heuristic)
- [Distancia de Manhattan](https://en.wikipedia.org/wiki/Taxicab_geometry)
- [Documentación de Tkinter](https://docs.python.org/3/library/tkinter.html)

### Uso de inteligencia artificial

Durante el desarrollo de este proyecto se utilizó IA como herramienta de apoyo y revisión, no como sustituto de la comprensión del código:

- Revisión de la función de coste y la elección de heurística en el algoritmo A* de `pathfinder.py`, para confirmar que reflejaba correctamente las reglas de coste por tipo de zona del enunciado.
- Discusión de casos límite en la mecánica de movimiento por turnos en `drone.py` y `simulation.py`, en particular el comportamiento de los tránsitos de dos turnos a través de zonas `restricted`.
- Revisión del manejo de errores en el parser (`parser.py`) para asegurar que cualquier línea mal formada genera un mensaje de error claro y con el número de línea exacto.
- Apoyo en la redacción y el formato de este `README.md`.
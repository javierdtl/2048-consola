# 2048 en consola

Versión del juego 2048 en Python que se juega desde la terminal. La hice originalmente como práctica del grado de Ingeniería Matemática (UCM) y la he revisado posteriormente para que se pueda jugar de principio a fin. 

```
     .     .     .     .
     .     .     .     .
     .     .     4     2
     .     .     2     4
Max: 4   Score: 8
```

## Cómo jugar

Solo hace falta Python 3, sin librerías externas.

```
python game2048.py
```

Se mueve con `w` (arriba), `a` (izquierda), `s` (abajo) y `d` (derecha), pulsando Enter después de cada tecla. Con `q` se sale. Si un movimiento no cambia el tablero, el juego lo avisa y no añade ficha nueva.

El tablero puede ser de cualquier tamaño. Para jugar en uno de 5x5:

```
python game2048.py 5
```

## Cómo está hecho

Todo está en `game2048.py`:

- La clase `Game2048` guarda el tablero (una lista de listas) y la puntuación. Tiene un método por dirección (`up`, `down`, `left`, `right`), `add_new_cell` para sacar un 2 o un 4 en una casilla vacía e `is_blocked` para saber si la partida ha terminado.
- Las cuatro direcciones usan la misma función, `_merge_line`, que junta los números de una fila o columna y suma los que son iguales. Cada dirección solo cambia el orden en que se leen las casillas.
- `play()` es el bucle de la partida: enseña el tablero, lee la tecla, mueve y añade una ficha.

## Tests

`test_game2048.py` comprueba las sumas, que una ficha no se sume dos veces en el mismo movimiento, que un movimiento sin efecto devuelva `False` y los casos de fin de partida. Se ejecutan con pytest:

```
pip install pytest
python -m pytest
```

## Autor

Javier de Torres

# Restaurante App - Semana 11

**Estudiante:** Cristofer Daniel Zambrano valderramo 
**Asignatura:** Programación Orientada a Objetos
**Actividad:** Semana 11 - Colecciones, relaciones entre objetos y persistencia JSON

## Descripción

`restaurante_app` es una aplicación de consola desarrollada en Python para administrar productos y usuarios de un restaurante.

Esta versión corresponde a la evolución del proyecto de la Semana 11. Se incorporan nuevas funcionalidades relacionadas con el uso de colecciones, el manejo de stock, la entidad `Venta`, la relación entre usuarios y productos, la consulta de ventas por usuario y la persistencia de información mediante archivos JSON.

La lógica de negocio se encuentra en `Restaurante`, la persistencia se concentra en `ArchivoServicio` y `main.py` se encarga de la interacción con el usuario mediante `input()`.

## Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
```

## Responsabilidad de los componentes

### `modelos/producto.py`

Contiene la clase `Producto`, sus atributos y validaciones. Además, incorpora el atributo `stock` y el método `vender()` para disminuir la cantidad disponible.

### `modelos/usuario.py`

Contiene la clase `Usuario`, sus validaciones y la información necesaria para identificar a los usuarios registrados.

### `modelos/venta.py`

Contiene la clase `Venta`, que representa la relación entre un usuario y un producto vendido.

La clase maneja como mínimo:

* `usuario_id`
* `producto_codigo`
* `cantidad`

### `servicios/restaurante.py`

Administra las colecciones de objetos `Producto`, `Usuario` y `Venta`.

También contiene las reglas de negocio para:

* Registrar productos.
* Registrar usuarios.
* Buscar productos.
* Buscar usuarios.
* Realizar ventas.
* Validar cantidades y stock.
* Consultar las ventas de un usuario.

### `servicios/archivo_servicio.py`

Centraliza la lectura y escritura de los archivos JSON:

* `productos.json`
* `usuarios.json`
* `ventas.json`

Utiliza `json.dump()`, `json.load()`, `with open()` y codificación UTF-8.

### `datos/`

Contiene únicamente los archivos JSON utilizados para conservar la información del sistema.

### `main.py`

Es el punto de entrada de la aplicación. Presenta el menú, solicita información mediante `input()` y ejecuta las operaciones utilizando los métodos de `Restaurante`.

### `README.md`

Documenta las características, estructura, funcionamiento, persistencia y pruebas realizadas durante la Semana 11.

## Manejo del stock

Cada producto posee un atributo `stock` que representa la cantidad disponible.

El sistema valida que:

1. El usuario exista.
2. El producto exista.
3. La cantidad solicitada sea mayor que cero.
4. La cantidad solicitada no supere el stock disponible.

Cuando la venta es válida, se crea una instancia de `Venta`, se registra en la colección de ventas y se disminuye el stock del producto.

Ejemplo:

```text
Antes de la venta:

Producto: Hamburguesa
Stock: 10
Cantidad solicitada: 2

Después de la venta:

Producto: Hamburguesa
Stock: 8

Venta registrada correctamente.
```

Las ventas con cantidades inválidas o superiores al stock disponible son rechazadas y no modifican la información.

## Relación Usuario + Producto → Venta

La operación de venta relaciona un usuario registrado con un producto existente.

```text
Usuario registrado
        ↓
Producto existente
        ↓
Validar cantidad
        ↓
Validar stock
        ↓
Crear Venta
        ↓
Agregar Venta a la colección
        ↓
Disminuir stock
        ↓                
Guardar información en JSON
```

La clase `Venta` conserva la identificación del usuario, el código del producto y la cantidad vendida.

Las colecciones internas utilizan objetos `Producto`, `Usuario` y `Venta`. Los diccionarios se utilizan únicamente como representación para guardar y recuperar información desde JSON.

## Operación `vender_producto()`

La venta se realiza mediante una operación equivalente a:

```python
vender_producto(codigo_producto, identificacion_usuario, cantidad)
```

Antes de realizar la operación se comprueba que el usuario y el producto existan, que la cantidad sea válida y que exista stock suficiente.

Si todas las condiciones se cumplen:

* Se crea un objeto `Venta`.
* Se agrega la venta a la colección.
* Se disminuye el stock.
* Se guarda `ventas.json`.
* Se actualiza `productos.json`.

## Consulta de ventas por usuario

El sistema permite consultar las ventas asociadas a un usuario.

La operación recorre la colección de ventas y compara la identificación del usuario con `venta.usuario_id`.

Las coincidencias se agregan a una nueva lista para mostrar únicamente las ventas correspondientes al usuario consultado.

La consulta permite visualizar información como:

* Identificación del usuario.
* Código del producto.
* Nombre del producto.
* Cantidad adquirida.

## Persistencia JSON

La aplicación utiliza tres archivos para conservar la información:

```text
datos/
├── productos.json
├── usuarios.json
└── ventas.json
```

### `productos.json`

Conserva los productos registrados y su stock actualizado.

### `usuarios.json`

Conserva los usuarios registrados.

### `ventas.json`

Conserva las ventas realizadas, relacionando usuarios y productos.

El proceso de persistencia funciona de la siguiente manera:

```text
OBJETOS
   ↓
Convertir a diccionario
   ↓
Lista de diccionarios
   ↓
json.dump()
   ↓
Archivo JSON
```

Para recuperar la información:

```text
Archivo JSON
   ↓
json.load()
   ↓
Diccionarios
   ↓
Reconstrucción de objetos
```

Al iniciar nuevamente la aplicación, los productos, usuarios y ventas son recuperados desde sus respectivos archivos JSON.

## Manejo de excepciones

El proyecto controla errores específicos relacionados con archivos y validaciones:

* `FileNotFoundError`: permite iniciar con una colección vacía cuando el archivo todavía no existe.
* `json.JSONDecodeError`: controla archivos que contienen información JSON inválida.
* `PermissionError`: controla problemas de permisos de lectura o escritura.
* `KeyError`: controla registros JSON que no contienen una clave requerida.
* `ValueError`: se utiliza para controlar errores de validación en los modelos.

No se utiliza `except: pass` para ocultar errores.

## Cómo ejecutar el proyecto

Se requiere Python 3.10 o una versión superior recomendada.

Desde una terminal ubicada en la carpeta del proyecto:

```bash
cd restaurante_app
python main.py
```

En algunos sistemas puede utilizarse:

```bash
python3 main.py
```

El programa mostrará un menú en consola desde el cual se pueden realizar las diferentes operaciones disponibles.

## Pruebas realizadas

### 1. Registro y persistencia de productos

Se registró un producto con stock disponible y se verificó que la información fuera almacenada correctamente en `productos.json`.

Después de cerrar y ejecutar nuevamente el programa, se comprobó que el producto fuera recuperado.

### 2. Registro y persistencia de usuarios

Se registró un usuario y se verificó que la información fuera almacenada en `usuarios.json`.

Posteriormente se reinició el programa para comprobar la recuperación del usuario.

### 3. Venta válida

Se realizó una venta verificando previamente que existieran el usuario y el producto.

Se comprobó que:

* La venta fuera registrada.
* El stock disminuyera correctamente.
* `ventas.json` almacenara la nueva venta.
* `productos.json` conservara el stock actualizado.

### 4. Consulta de ventas por usuario

Se utilizó la opción correspondiente del menú para consultar las ventas de un usuario.

Se comprobó que la colección de ventas fuera recorrida y filtrada utilizando la identificación del usuario.

### 5. Venta con stock insuficiente

Se intentó realizar una venta con una cantidad superior al stock disponible.

El sistema rechazó la operación y se verificó que:

* El stock no disminuyera.
* No se registrara una nueva venta.
* Los datos permanecieran consistentes.

### 6. Persistencia después del reinicio

Se cerró completamente la aplicación y se ejecutó nuevamente `main.py`.

Se comprobó que los productos, usuarios y ventas fueran recuperados desde sus respectivos archivos JSON.

## Conclusión

La Semana 11 amplía el proyecto `restaurante_app` mediante el uso de colecciones de objetos y relaciones entre las entidades del sistema.

La incorporación de `Venta` permite relacionar usuarios con productos, controlar el stock disponible y conservar las operaciones realizadas mediante archivos JSON.

El proyecto mantiene una organización modular, separando los modelos, la lógica de negocio, la persistencia y la interacción con el usuario.

## Entrega

El proyecto debe publicarse en un repositorio **nuevo y público de GitHub**.

El repositorio debe contener el código completo del proyecto, los archivos JSON y este `README.md`.

Finalmente, se debe entregar en Moodle únicamente el enlace del repositorio público correspondiente a la Semana 11.
"# restaurante_app11" 

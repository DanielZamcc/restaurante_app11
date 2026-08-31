from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante


BASE = Path(__file__).resolve().parent
RUTA_PRODUCTOS = BASE / "datos" / "productos.json"
RUTA_USUARIOS = BASE / "datos" / "usuarios.json"
RUTA_VENTAS = BASE / "datos" / "ventas.json"


def mostrar_menu() -> None:
    print("\n========== RESTAURANTE APP - SEMANA 11 ==========")
    print("1. Registrar producto")
    print("2. Buscar producto")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Listar productos")
    print("6. Registrar usuario")
    print("7. Listar usuarios")
    print("8. Vender producto")
    print("9. Consultar ventas de un usuario")
    print("10. Listar ventas")
    print("0. Salir")


def pedir_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: ingrese un número entero válido.")


def pedir_precio() -> float:
    while True:
        try:
            return float(input("Precio: $"))
        except ValueError:
            print("Error: ingrese un precio numérico válido.")


def registrar_producto(
    restaurante: Restaurante, archivo: ArchivoServicio
) -> None:
    try:
        codigo = input("Código: ")
        nombre = input("Nombre: ")
        precio = pedir_precio()
        categoria = input("Categoría: ")
        stock = pedir_entero("Stock inicial: ")

        producto = Producto(codigo, nombre, precio, categoria, stock)

        if restaurante.registrar_producto(producto):
            if archivo.guardar_productos(restaurante.listar_productos()):
                print("Producto registrado y guardado correctamente.")
            else:
                print("Producto registrado, pero no se pudo guardar el archivo.")
        else:
            print("Ya existe un producto con ese código.")
    except ValueError as error:
        print(f"No se pudo registrar el producto: {error}")


def buscar_producto(restaurante: Restaurante) -> None:
    codigo = input("Código del producto: ")
    producto = restaurante.buscar_producto(codigo)
    if producto is None:
        print("Producto no encontrado.")
    else:
        print(producto.mostrar_informacion())


def actualizar_producto(
    restaurante: Restaurante, archivo: ArchivoServicio
) -> None:
    codigo = input("Código del producto a actualizar: ")
    if restaurante.buscar_producto(codigo) is None:
        print("Producto no encontrado.")
        return

    try:
        nombre = input("Nuevo nombre: ")
        precio = pedir_precio()
        categoria = input("Nueva categoría: ")
        stock = pedir_entero("Nuevo stock: ")

        if restaurante.actualizar_producto(
            codigo, nombre, precio, categoria, stock
        ):
            if archivo.guardar_productos(restaurante.listar_productos()):
                print("Producto actualizado y guardado correctamente.")
            else:
                print("Producto actualizado, pero no se pudo guardar el archivo.")
    except ValueError as error:
        print(f"No se pudo actualizar el producto: {error}")


def eliminar_producto(
    restaurante: Restaurante, archivo: ArchivoServicio
) -> None:
    codigo = input("Código del producto a eliminar: ")
    if restaurante.eliminar_producto(codigo):
        if archivo.guardar_productos(restaurante.listar_productos()):
            print("Producto eliminado y archivo actualizado.")
        else:
            print("Producto eliminado, pero no se pudo guardar el archivo.")
    else:
        print("Producto no encontrado.")


def listar_productos(restaurante: Restaurante) -> None:
    productos = restaurante.listar_productos()
    if not productos:
        print("No hay productos registrados.")
        return

    print("\n----- PRODUCTOS -----")
    for producto in productos:
        print(producto.mostrar_informacion())


def registrar_usuario(
    restaurante: Restaurante, archivo: ArchivoServicio
) -> None:
    try:
        identificacion = input("Identificación: ")
        nombre = input("Nombre: ")
        correo = input("Correo: ")

        usuario = Usuario(identificacion, nombre, correo)

        if restaurante.registrar_usuario(usuario):
            if archivo.guardar_usuarios(restaurante.listar_usuarios()):
                print("Usuario registrado y guardado correctamente.")
            else:
                print("Usuario registrado, pero no se pudo guardar el archivo.")
        else:
            print("Ya existe un usuario con esa identificación.")
    except ValueError as error:
        print(f"No se pudo registrar el usuario: {error}")


def listar_usuarios(restaurante: Restaurante) -> None:
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    print("\n----- USUARIOS -----")
    for usuario in usuarios:
        print(usuario.mostrar_informacion())


def vender_producto(
    restaurante: Restaurante, archivo: ArchivoServicio
) -> None:
    identificacion = input("Identificación del usuario: ")
    codigo = input("Código del producto: ")
    cantidad = pedir_entero("Cantidad a comprar: ")

    usuario = restaurante.buscar_usuario(identificacion)
    producto = restaurante.buscar_producto(codigo)

    if usuario is None:
        print("Venta rechazada: el usuario no existe.")
        return
    if producto is None:
        print("Venta rechazada: el producto no existe.")
        return
    if cantidad <= 0:
        print("Venta rechazada: la cantidad debe ser mayor que cero.")
        return
    if producto.stock < cantidad:
        print(
            f"Venta rechazada: stock insuficiente. "
            f"Stock disponible: {producto.stock}."
        )
        return

    if restaurante.vender_producto(codigo, identificacion, cantidad):
        ventas_guardadas = archivo.guardar_ventas(restaurante.listar_ventas())
        productos_guardados = archivo.guardar_productos(
            restaurante.listar_productos()
        )
        if ventas_guardadas and productos_guardados:
            print("Venta registrada correctamente.")
            print(f"Nuevo stock de {producto.nombre}: {producto.stock}")
        else:
            print(
                "La venta se registró en memoria, pero hubo un problema "
                "al guardar uno de los archivos."
            )


def consultar_ventas_usuario(restaurante: Restaurante) -> None:
    identificacion = input("Identificación del usuario: ")
    usuario = restaurante.buscar_usuario(identificacion)

    if usuario is None:
        print("Usuario no encontrado.")
        return

    ventas = restaurante.ventas_de_usuario(identificacion)
    if not ventas:
        print("El usuario no tiene ventas registradas.")
        return

    print(f"\n----- VENTAS DE {usuario.nombre} -----")
    for venta in ventas:
        producto = restaurante.buscar_producto(venta.producto_codigo)
        nombre_producto = producto.nombre if producto is not None else "No disponible"
        print(
            f"Producto: {venta.producto_codigo} - {nombre_producto} | "
            f"Cantidad: {venta.cantidad}"
        )


def listar_ventas(restaurante: Restaurante) -> None:
    ventas = restaurante.listar_ventas()
    if not ventas:
        print("No hay ventas registradas.")
        return

    print("\n----- VENTAS -----")
    for venta in ventas:
        print(venta)


def main() -> None:
    archivo = ArchivoServicio(
        RUTA_PRODUCTOS, RUTA_USUARIOS, RUTA_VENTAS
    )

    productos = archivo.cargar_productos()
    usuarios = archivo.cargar_usuarios()
    ventas = archivo.cargar_ventas()

    restaurante = Restaurante(productos, usuarios, ventas)

    print(
        f"Datos recuperados: {len(productos)} producto(s), "
        f"{len(usuarios)} usuario(s), {len(ventas)} venta(s)."
    )

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_producto(restaurante, archivo)
        elif opcion == "2":
            buscar_producto(restaurante)
        elif opcion == "3":
            actualizar_producto(restaurante, archivo)
        elif opcion == "4":
            eliminar_producto(restaurante, archivo)
        elif opcion == "5":
            listar_productos(restaurante)
        elif opcion == "6":
            registrar_usuario(restaurante, archivo)
        elif opcion == "7":
            listar_usuarios(restaurante)
        elif opcion == "8":
            vender_producto(restaurante, archivo)
        elif opcion == "9":
            consultar_ventas_usuario(restaurante)
        elif opcion == "10":
            listar_ventas(restaurante)
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()

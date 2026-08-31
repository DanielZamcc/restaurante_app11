from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """Administra productos, usuarios y ventas y aplica las reglas de negocio."""

    def __init__(
        self,
        productos: list[Producto] | None = None,
        usuarios: list[Usuario] | None = None,
        ventas: list[Venta] | None = None,
    ) -> None:
        self._productos: list[Producto] = productos if productos is not None else []
        self._usuarios: list[Usuario] = usuarios if usuarios is not None else []
        self._ventas: list[Venta] = ventas if ventas is not None else []

    # Productos
    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto(producto.codigo) is not None:
            return False
        self._productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo = str(codigo).strip().lower()
        for producto in self._productos:
            if producto.codigo.lower() == codigo:
                return producto
        return None

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int | None = None,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        producto.nombre = nombre
        producto.precio = precio
        producto.categoria = categoria
        if stock is not None:
            producto.stock = stock
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        return True

    def listar_productos(self) -> list[Producto]:
        return list(self._productos)

    # Usuarios
    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.buscar_usuario(usuario.identificacion) is not None:
            return False
        self._usuarios.append(usuario)
        return True

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        identificacion = str(identificacion).strip().lower()
        for usuario in self._usuarios:
            if usuario.identificacion.lower() == identificacion:
                return usuario
        return None

    def listar_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    # Ventas
    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int,
    ) -> bool:
        """Registra una venta y descuenta stock si todas las validaciones pasan."""
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        producto.vender(cantidad)
        return True

    def listar_ventas(self) -> list[Venta]:
        return list(self._ventas)

    def ventas_de_usuario(self, identificacion_usuario: str) -> list[Venta]:
        """Recorre y filtra la colección para obtener ventas de un usuario."""
        ventas_usuario: list[Venta] = []

        for venta in self._ventas:
            if venta.usuario_id.lower() == str(identificacion_usuario).strip().lower():
                ventas_usuario.append(venta)

        return ventas_usuario

class Venta:
    """Representa la relación entre un usuario y un producto vendido."""

    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int,
    ) -> None:
        usuario_id = str(usuario_id).strip()
        producto_codigo = str(producto_codigo).strip()

        if not usuario_id:
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not producto_codigo:
            raise ValueError("El código del producto no puede estar vacío.")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ValueError("La cantidad debe ser un número entero.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    def a_diccionario(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
        }

    def __str__(self) -> str:
        return (
            f"Usuario: {self.usuario_id} | "
            f"Producto: {self.producto_codigo} | Cantidad: {self.cantidad}"
        )

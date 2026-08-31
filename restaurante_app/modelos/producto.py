class Producto:
    """Representa un producto del restaurante."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int = 0,
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El código no puede estar vacío.")
        self._codigo = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            precio = float(valor)
        except (TypeError, ValueError) as error:
            raise ValueError("El precio debe ser numérico.") from error
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        self._precio = precio

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor:
            raise ValueError("La categoría no puede estar vacía.")
        self._categoria = valor

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if isinstance(valor, bool):
            raise ValueError("El stock debe ser un número entero.")
        try:
            stock = int(valor)
        except (TypeError, ValueError) as error:
            raise ValueError("El stock debe ser un número entero.") from error
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = stock

    def vender(self, cantidad: int) -> None:
        """Disminuye el stock únicamente si la cantidad es válida y disponible."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ValueError("La cantidad debe ser un número entero.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if cantidad > self.stock:
            raise ValueError("No existe stock suficiente.")
        self.stock -= cantidad

    def a_diccionario(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "stock": self.stock,
        }

    def mostrar_informacion(self) -> str:
        return (
            f"Código: {self.codigo} | Nombre: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | Categoría: {self.categoria} | "
            f"Stock: {self.stock}"
        )

    def __str__(self) -> str:
        return self.mostrar_informacion()

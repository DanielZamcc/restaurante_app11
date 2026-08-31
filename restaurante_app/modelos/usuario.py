class Usuario:
    """Representa a una persona registrada que puede realizar compras."""

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        identificacion = str(identificacion).strip()
        nombre = str(nombre).strip()
        correo = str(correo).strip()

        if not identificacion:
            raise ValueError("La identificación no puede estar vacía.")
        if not nombre:
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not correo:
            raise ValueError("El correo del usuario no puede estar vacío.")

        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    def a_diccionario(self) -> dict:
        """Convierte el objeto a una estructura compatible con JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    def mostrar_informacion(self) -> str:
        return (
            f"Identificación: {self.identificacion} | "
            f"Nombre: {self.nombre} | Correo: {self.correo}"
        )

    def __str__(self) -> str:
        return self.mostrar_informacion()

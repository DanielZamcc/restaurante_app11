import json
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    """Centraliza la lectura y escritura de productos, usuarios y ventas en JSON."""

    def __init__(
        self,
        ruta_productos: str | Path,
        ruta_usuarios: str | Path,
        ruta_ventas: str | Path,
    ) -> None:
        self.ruta_productos = Path(ruta_productos)
        self.ruta_usuarios = Path(ruta_usuarios)
        self.ruta_ventas = Path(ruta_ventas)

    def _cargar_lista_json(self, ruta: Path, nombre: str) -> list[dict]:
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            if not isinstance(datos, list):
                raise ValueError(f"{nombre} debe contener una lista JSON.")

            return datos

        except FileNotFoundError:
            print(f"No existe {ruta.name}. Se iniciará con una colección vacía.")
            return []
        except json.JSONDecodeError:
            print(f"El archivo {ruta.name} no contiene un JSON válido.")
            return []
        except PermissionError:
            print(f"No hay permisos suficientes para leer {ruta.name}.")
            return []
        except ValueError as error:
            print(f"Error en la estructura de {ruta.name}: {error}")
            return []

    def _guardar_lista_json(self, ruta: Path, datos: list[dict], nombre: str) -> bool:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
            return True
        except PermissionError:
            print(f"No hay permisos suficientes para escribir {nombre}.")
            return False
        except OSError as error:
            print(f"No fue posible guardar {nombre}: {error}")
            return False

    def cargar_productos(self) -> list[Producto]:
        productos: list[Producto] = []
        for numero, registro in enumerate(
            self._cargar_lista_json(self.ruta_productos, "productos.json"), start=1
        ):
            try:
                if not isinstance(registro, dict):
                    raise ValueError("El registro no es un objeto JSON.")
                # stock=0 permite leer registros antiguos de Semana 10.
                producto = Producto(
                    codigo=registro["codigo"],
                    nombre=registro["nombre"],
                    precio=registro["precio"],
                    categoria=registro["categoria"],
                    stock=registro.get("stock", 0),
                )
                productos.append(producto)
            except KeyError as error:
                print(f"Advertencia: producto {numero} incompleto. Falta {error}.")
            except ValueError as error:
                print(f"Advertencia: producto {numero} inválido: {error}.")
        return productos

    def guardar_productos(self, productos: list[Producto]) -> bool:
        datos = [producto.a_diccionario() for producto in productos]
        return self._guardar_lista_json(
            self.ruta_productos, datos, "productos.json"
        )

    def cargar_usuarios(self) -> list[Usuario]:
        usuarios: list[Usuario] = []
        for numero, registro in enumerate(
            self._cargar_lista_json(self.ruta_usuarios, "usuarios.json"), start=1
        ):
            try:
                if not isinstance(registro, dict):
                    raise ValueError("El registro no es un objeto JSON.")
                usuario = Usuario(
                    identificacion=registro["identificacion"],
                    nombre=registro["nombre"],
                    correo=registro["correo"],
                )
                usuarios.append(usuario)
            except KeyError as error:
                print(f"Advertencia: usuario {numero} incompleto. Falta {error}.")
            except ValueError as error:
                print(f"Advertencia: usuario {numero} inválido: {error}.")
        return usuarios

    def guardar_usuarios(self, usuarios: list[Usuario]) -> bool:
        datos = [usuario.a_diccionario() for usuario in usuarios]
        return self._guardar_lista_json(
            self.ruta_usuarios, datos, "usuarios.json"
        )

    def cargar_ventas(self) -> list[Venta]:
        ventas: list[Venta] = []
        for numero, registro in enumerate(
            self._cargar_lista_json(self.ruta_ventas, "ventas.json"), start=1
        ):
            try:
                if not isinstance(registro, dict):
                    raise ValueError("El registro no es un objeto JSON.")
                venta = Venta(
                    usuario_id=registro["usuario_id"],
                    producto_codigo=registro["producto_codigo"],
                    cantidad=registro["cantidad"],
                )
                ventas.append(venta)
            except KeyError as error:
                print(f"Advertencia: venta {numero} incompleta. Falta {error}.")
            except ValueError as error:
                print(f"Advertencia: venta {numero} inválida: {error}.")
        return ventas

    def guardar_ventas(self, ventas: list[Venta]) -> bool:
        datos = [venta.a_diccionario() for venta in ventas]
        return self._guardar_lista_json(
            self.ruta_ventas, datos, "ventas.json"
        )

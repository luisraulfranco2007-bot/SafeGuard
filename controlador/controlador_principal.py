from modelo.aseguradora import Aseguradora
from modelo.poliza import Poliza
from modelo.siniestro import Siniestro
from modelo.manejador_datos import ManejadorDatos


class ControladorPrincipal:
   

    def __init__(self):
        self.__manejador = ManejadorDatos()
        self.__aseguradora = Aseguradora("SafeGuard S.A.")
        self.__siniestros = []
        self.__cargar_datos()

    def __cargar_datos(self):
        """Carga pólizas y siniestros del Excel al iniciar."""
        for poliza in self.__manejador.cargar_polizas():
            self.__aseguradora.agregar_poliza(poliza)
        self.__siniestros = self.__manejador.cargar_siniestros()

    def registrar_poliza(
        self, numero, titular, monto, tipo, f_ini, f_ven
    ) -> str:
        """Valida, crea y registra una nueva póliza."""
        if not all([numero, titular, monto, tipo, f_ini, f_ven]):
            return "ERROR: Todos los campos son obligatorios."
        try:
            monto = float(monto)
            if monto <= 0:
                return "ERROR: El monto debe ser un número positivo."
        except ValueError:
            return "ERROR: El monto debe ser un número."
        if f_ven <= f_ini:
            return "ERROR: La fecha de vencimiento debe ser posterior a la de inicio."

        poliza = Poliza(numero, titular, monto, tipo, f_ini, f_ven)
        mensaje = self.__aseguradora.agregar_poliza(poliza)
        if not mensaje.startswith("ERROR") and not mensaje.startswith("Ya"):
            self.__manejador.guardar_polizas(
                self.__aseguradora.get_lista_polizas()
            )
        return mensaje

    def buscar_polizas(self, criterio: str) -> list:
        if not criterio.strip():
            return self.__aseguradora.get_lista_polizas()
        return self.__aseguradora.buscar(criterio)

    def eliminar_vencidas(self) -> str:
        n = self.__aseguradora.eliminar_vencidas()
        self.__manejador.guardar_polizas(
            self.__aseguradora.get_lista_polizas()
        )
        return f"{n} póliza(s) vencida(s) eliminada(s)."

    def get_todas_polizas(self) -> list:
        return self.__aseguradora.get_lista_polizas()

    def aplicar_descuento(self, numero: str, porcentaje=None, cupon=None) -> str:
        poliza = self.__aseguradora.get_poliza_por_numero(numero)
        if poliza is None:
            return f"ERROR: No se encontró la póliza {numero}."
        resultado = poliza.aplicar_descuento(porcentaje=porcentaje, cupon=cupon)
        self.__manejador.guardar_polizas(
            self.__aseguradora.get_lista_polizas()
        )
        return resultado


    def registrar_siniestro(
        self, titular, fecha, descripcion, numero_poliza
    ) -> str:
        if not all([titular, fecha, descripcion, numero_poliza]):
            return "ERROR: Todos los campos son obligatorios."

        poliza = self.__aseguradora.get_poliza_por_numero(numero_poliza)
        if poliza is None:
            return "ERROR: La póliza ingresada no existe."
        if not poliza.esta_vigente():
            return "ERROR: La póliza está vencida, no se puede registrar el siniestro."

        id_rep = self.__manejador.siguiente_id_siniestro()
        siniestro = Siniestro(id_rep, titular, fecha, descripcion, numero_poliza)
        self.__siniestros.append(siniestro)
        self.__manejador.guardar_siniestros(self.__siniestros)
        return siniestro.registrar()

    def get_todos_siniestros(self) -> list:
        return self.__siniestros
    
    
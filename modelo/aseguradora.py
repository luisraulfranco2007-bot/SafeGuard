from modelo.poliza import Poliza


class Aseguradora:


    def __init__(self, nombre_empresa: str):
        self.__nombre_empresa = nombre_empresa
        self.__lista_polizas = []


    def agregar_poliza(self, poliza: Poliza) -> str:
        """Agrega una póliza si su número no existe ya en la lista."""
        for p in self.__lista_polizas:
            if p.get_numero() == poliza.get_numero():
                return f"Ya existe una póliza con el número {poliza.get_numero()}."
        self.__lista_polizas.append(poliza)
        return f"Póliza {poliza.get_numero()} registrada correctamente."

    def buscar(self, criterio: str) -> list:
        """Busca por número o titular (parcial, sin distinguir mayúsculas)."""
        criterio = criterio.lower()
        return [
            p for p in self.__lista_polizas
            if criterio in p.get_numero().lower()
            or criterio in p.get_titular().lower()
        ]

    def eliminar_vencidas(self) -> int:
        """Elimina pólizas vencidas. Devuelve cuántas se eliminaron."""
        antes = len(self.__lista_polizas)
        self.__lista_polizas = [
            p for p in self.__lista_polizas if p.esta_vigente()
        ]
        return antes - len(self.__lista_polizas)

    def eliminar_poliza(self, numero: str) -> str:
        """Elimina una póliza específica por número."""
        for i, p in enumerate(self.__lista_polizas):
            if p.get_numero() == numero:
                self.__lista_polizas.pop(i)
                return f"Póliza {numero} eliminada."
        return f"No se encontró la póliza {numero}."

    def get_lista_polizas(self) -> list:
        return self.__lista_polizas

    def get_nombre(self) -> str:
        return self.__nombre_empresa

    def get_poliza_por_numero(self, numero: str):
        """Devuelve el objeto Poliza con ese número, o None si no existe."""
        for p in self.__lista_polizas:
            if p.get_numero() == numero:
                return p
        return None
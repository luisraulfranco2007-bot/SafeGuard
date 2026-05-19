from modelo.contrato import Contrato


class Siniestro(Contrato):
    """
    Representa un incidente reportado por un asegurado.
    Hereda de Contrato e implementa calcular_prima() devolviendo 0
    porque los siniestros no tienen prima propia.
    """

    def __init__(
        self,
        id_reporte: str,
        titular: str,
        fecha: str,
        descripcion: str,
        numero_poliza: str,
    ):
        super().__init__(id_reporte, titular)
        self.__id_reporte = id_reporte
        self.__fecha = fecha
        self.__descripcion = descripcion
        self.__numero_poliza = numero_poliza


    def calcular_prima(self) -> float:
    
        return 0.0

    def registrar(self) -> str:
        return (
            f"Siniestro {self.__id_reporte} registrado el {self.__fecha}. "
            f"Póliza afectada: {self.__numero_poliza}."
        )

    def get_info(self) -> str:
        return (
            f"{self.__id_reporte} | {self.get_titular()} | "
            f"{self.__fecha} | {self.__descripcion[:40]}..."
        )

    def get_id_reporte(self) -> str:
        return self.__id_reporte

    def get_fecha(self) -> str:
        return self.__fecha

    def get_descripcion(self) -> str:
        return self.__descripcion

    def get_numero_poliza(self) -> str:
        return self.__numero_poliza
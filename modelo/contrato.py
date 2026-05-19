from abc import ABC, abstractmethod


class Contrato(ABC):


    def __init__(self, numero: str, titular: str):
        self.__numero = numero
        self.__titular = titular

    @abstractmethod
    def calcular_prima(self) -> float:
        """
        Cada tipo de contrato calcula su prima de forma diferente.
        Las subclases están obligadas a implementarlo.
        """
        pass

   
    def get_info(self) -> str:
        return f"Contrato: {self.__numero} | Titular: {self.__titular}"

   
    def get_numero(self) -> str:
        return self.__numero

    def get_titular(self) -> str:
        return self.__titular
from modelo.contrato import Contrato
from datetime import date



FACTORES = {
    "Auto": 0.008,
    "Vida": 0.005,
    "Gastos médicos": 0.007,
    "Hogar": 0.004,
}

CUPONES = {
    "PROMO2025": 10,
    "BIENVENIDO": 15,
    "ANUAL20": 20,
}


class Poliza(Contrato):
    """
    Representa un contrato de seguro individual.
    Hereda de Contrato e implementa calcular_prima().
    """

    def __init__(
        self,
        numero: str,
        titular: str,
        monto_asegurado: float,
        tipo_seguro: str,
        fecha_inicio: str,
        fecha_vencimiento: str,
    ):
        super().__init__(numero, titular)
        self.__monto_asegurado = monto_asegurado
        self.__tipo_seguro = tipo_seguro
        self.__fecha_inicio = fecha_inicio
        self.__fecha_vencimiento = fecha_vencimiento
        self.__prima_mensual = self.calcular_prima()

    def calcular_prima(self) -> float:
        factor = FACTORES.get(self.__tipo_seguro, 0.006)
        self.__prima_mensual = round(self.__monto_asegurado * factor, 2)
        return self.__prima_mensual


    def aplicar_descuento(self, porcentaje=None, cupon=None):
        """
        Versión 1 — sin argumentos:    descuento estándar del 5%
        Versión 2 — con porcentaje:    descuento personalizado
        Versión 3 — con cupón:         descuento según código
        """
        if cupon is not None:
            
            if cupon in CUPONES:
                pct = CUPONES[cupon]
                self.__prima_mensual = round(
                    self.__prima_mensual * (1 - pct / 100), 2
                )
                return f"Cupón '{cupon}' aplicado: {pct}% de descuento."
            else:
                return "Cupón inválido o expirado."

        elif porcentaje is not None:
            # Versión 2: porcentaje personalizado
            if not (1 <= porcentaje <= 100):
                return "El porcentaje debe estar entre 1 y 100."
            self.__prima_mensual = round(
                self.__prima_mensual * (1 - porcentaje / 100), 2
            )
            return f"Descuento del {porcentaje}% aplicado."

        else:
           
            self.__prima_mensual = round(self.__prima_mensual * 0.95, 2)
            return "Descuento estándar del 5% aplicado."

  
    def esta_vigente(self) -> bool:
        hoy = date.today().isoformat()
        return self.__fecha_vencimiento >= hoy

    def get_info(self) -> str:
        estado = "Vigente" if self.esta_vigente() else "Vencida"
        return (
            f"{self.get_numero()} | {self.get_titular()} | "
            f"{self.__tipo_seguro} | ${self.__prima_mensual} | {estado}"
        )

   
    def get_monto(self) -> float:
        return self.__monto_asegurado

    def get_prima(self) -> float:
        return self.__prima_mensual

    def get_tipo(self) -> str:
        return self.__tipo_seguro

    def get_fecha_inicio(self) -> str:
        return self.__fecha_inicio

    def get_fecha_vencimiento(self) -> str:
        return self.__fecha_vencimiento
from controlador.controlador_principal import ControladorPrincipal
from vista.ventana_principal import VentanaPrincipal

def main():
    controlador = ControladorPrincipal()
    app = VentanaPrincipal(controlador)
    app.mainloop()

if __name__ == "__main__":
    main()
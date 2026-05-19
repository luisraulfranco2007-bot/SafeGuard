import tkinter as tk
from tkinter import ttk, messagebox

from vista.ventana_formularios import (
    VentanaRegistroPoliza,
    VentanaRegistroSiniestro,
    VentanaDescuento
)


class VentanaPrincipal(tk.Tk):

    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador

        self.title("SafeGuard - Sistema de Seguros")
        self.geometry("800x500")

        self._construir()
        self._cargar_tabla()

    def _construir(self):

        frame_top = ttk.Frame(self, padding=10)
        frame_top.pack(fill="x")

        ttk.Button(frame_top, text="Nueva póliza", command=self._nueva_poliza).pack(side="left", padx=5)
        ttk.Button(frame_top, text="Registrar siniestro", command=self._nuevo_siniestro).pack(side="left", padx=5)
        ttk.Button(frame_top, text="Eliminar vencidas", command=self._eliminar_vencidas).pack(side="left", padx=5)

  
        self.buscar_var = tk.StringVar()
        ttk.Entry(frame_top, textvariable=self.buscar_var, width=30).pack(side="left", padx=10)
        ttk.Button(frame_top, text="Buscar", command=self._buscar).pack(side="left")


        columnas = ("numero", "titular", "tipo", "prima", "estado")

        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, anchor="center")

        # 🔻 Botones inferiores
        frame_bottom = ttk.Frame(self, padding=10)
        frame_bottom.pack(fill="x")

        ttk.Button(frame_bottom, text="Aplicar descuento", command=self._descuento).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="Refrescar", command=self._cargar_tabla).pack(side="left", padx=5)



    def _cargar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())

        for p in self.controlador.get_todas_polizas():
            info = p.get_info().split(" | ")
            self.tabla.insert("", "end", values=info)

    def _buscar(self):
        criterio = self.buscar_var.get()
        resultados = self.controlador.buscar_polizas(criterio)

        self.tabla.delete(*self.tabla.get_children())

        for p in resultados:
            info = p.get_info().split(" | ")
            self.tabla.insert("", "end", values=info)

    def _nueva_poliza(self):
        ventana = VentanaRegistroPoliza(self, self.controlador)
        ventana.bind("<<PolizaRegistrada>>", lambda e: self._cargar_tabla())

    def _nuevo_siniestro(self):
        VentanaRegistroSiniestro(self, self.controlador)

    def _eliminar_vencidas(self):
        mensaje = self.controlador.eliminar_vencidas()
        messagebox.showinfo("Resultado", mensaje)
        self._cargar_tabla()

    def _descuento(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una póliza primero.")
            return

        numero = self.tabla.item(seleccion[0])["values"][0]
        ventana = VentanaDescuento(self, self.controlador, numero)
        ventana.bind("<<DescuentoAplicado>>", lambda e: self._cargar_tabla())
import tkinter as tk
from tkinter import ttk, messagebox


class VentanaRegistroPoliza(tk.Toplevel):
    """Formulario para registrar una nueva póliza."""

    TIPOS = ["Auto", "Vida", "Gastos médicos", "Hogar"]

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.title("Nueva póliza")
        self.resizable(False, False)
        self.grab_set()  # Modal
        self._construir()

    def _construir(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        campos = [
            ("Número de póliza", "numero"),
            ("Titular", "titular"),
            ("Monto asegurado ($)", "monto"),
            ("Fecha inicio (AAAA-MM-DD)", "f_ini"),
            ("Fecha vencimiento (AAAA-MM-DD)", "f_ven"),
        ]

        self.vars = {}
        for i, (etiqueta, clave) in enumerate(campos):
            ttk.Label(frame, text=etiqueta).grid(
                row=i, column=0, sticky="w", pady=4
            )
            var = tk.StringVar()
            ttk.Entry(frame, textvariable=var, width=30).grid(
                row=i, column=1, padx=(10, 0), pady=4
            )
            self.vars[clave] = var

        # Tipo de seguro
        ttk.Label(frame, text="Tipo de seguro").grid(
            row=len(campos), column=0, sticky="w", pady=4
        )
        self.tipo_var = tk.StringVar(value=self.TIPOS[0])
        ttk.Combobox(
            frame,
            textvariable=self.tipo_var,
            values=self.TIPOS,
            state="readonly",
            width=28,
        ).grid(row=len(campos), column=1, padx=(10, 0), pady=4)

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(campos) + 1, column=0, columnspan=2, pady=(16, 0))
        ttk.Button(btn_frame, text="Registrar", command=self._registrar).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(
            side="left", padx=4
        )

    def _registrar(self):
        mensaje = self.controlador.registrar_poliza(
            numero=self.vars["numero"].get(),
            titular=self.vars["titular"].get(),
            monto=self.vars["monto"].get(),
            tipo=self.tipo_var.get(),
            f_ini=self.vars["f_ini"].get(),
            f_ven=self.vars["f_ven"].get(),
        )
        if mensaje.startswith("ERROR") or mensaje.startswith("Ya"):
            messagebox.showerror("Error", mensaje, parent=self)
        else:
            messagebox.showinfo("Éxito", mensaje, parent=self)
            self.event_generate("<<PolizaRegistrada>>", when="tail")
            self.destroy()


class VentanaRegistroSiniestro(tk.Toplevel):
    """Formulario para registrar un siniestro."""

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.title("Registrar siniestro")
        self.resizable(False, False)
        self.grab_set()
        self._construir()

    def _construir(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        campos = [
            ("Número de póliza", "num_poliza"),
            ("Titular", "titular"),
            ("Fecha del siniestro (AAAA-MM-DD)", "fecha"),
        ]

        self.vars = {}
        for i, (etiqueta, clave) in enumerate(campos):
            ttk.Label(frame, text=etiqueta).grid(
                row=i, column=0, sticky="w", pady=4
            )
            var = tk.StringVar()
            ttk.Entry(frame, textvariable=var, width=30).grid(
                row=i, column=1, padx=(10, 0), pady=4
            )
            self.vars[clave] = var

        ttk.Label(frame, text="Descripción").grid(
            row=len(campos), column=0, sticky="nw", pady=4
        )
        self.desc_text = tk.Text(frame, width=30, height=4)
        self.desc_text.grid(
            row=len(campos), column=1, padx=(10, 0), pady=4
        )

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(
            row=len(campos) + 1, column=0, columnspan=2, pady=(16, 0)
        )
        ttk.Button(
            btn_frame, text="Guardar siniestro", command=self._guardar
        ).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(
            side="left", padx=4
        )

    def _guardar(self):
        mensaje = self.controlador.registrar_siniestro(
            titular=self.vars["titular"].get(),
            fecha=self.vars["fecha"].get(),
            descripcion=self.desc_text.get("1.0", "end").strip(),
            numero_poliza=self.vars["num_poliza"].get(),
        )
        if mensaje.startswith("ERROR"):
            messagebox.showerror("Error", mensaje, parent=self)
        else:
            messagebox.showinfo("Éxito", mensaje, parent=self)
            self.destroy()


class VentanaDescuento(tk.Toplevel):
    """Ventana para aplicar descuento a una póliza seleccionada."""

    def __init__(self, parent, controlador, numero_poliza: str):
        super().__init__(parent)
        self.controlador = controlador
        self.numero_poliza = numero_poliza
        self.title(f"Aplicar descuento — {numero_poliza}")
        self.resizable(False, False)
        self.grab_set()
        self._construir()

    def _construir(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text=f"Póliza: {self.numero_poliza}",
            font=("", 10, "bold"),
        ).pack(anchor="w", pady=(0, 12))

        self.modo = tk.StringVar(value="estandar")

        # Versión 1
        ttk.Radiobutton(
            frame, text="Descuento estándar (5%)",
            variable=self.modo, value="estandar"
        ).pack(anchor="w")

        # Versión 2
        v2 = ttk.Frame(frame)
        v2.pack(anchor="w", pady=4)
        ttk.Radiobutton(
            v2, text="Porcentaje personalizado:",
            variable=self.modo, value="porcentaje"
        ).pack(side="left")
        self.pct_var = tk.StringVar()
        ttk.Entry(v2, textvariable=self.pct_var, width=6).pack(
            side="left", padx=(6, 0)
        )
        ttk.Label(v2, text="%").pack(side="left")

        # Versión 3
        v3 = ttk.Frame(frame)
        v3.pack(anchor="w", pady=4)
        ttk.Radiobutton(
            v3, text="Cupón:",
            variable=self.modo, value="cupon"
        ).pack(side="left")
        self.cupon_var = tk.StringVar()
        ttk.Entry(v3, textvariable=self.cupon_var, width=16).pack(
            side="left", padx=(6, 0)
        )

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=(16, 0))
        ttk.Button(
            btn_frame, text="Aplicar", command=self._aplicar
        ).pack(side="left", padx=4)
        ttk.Button(
            btn_frame, text="Cancelar", command=self.destroy
        ).pack(side="left", padx=4)

    def _aplicar(self):
        modo = self.modo.get()
        if modo == "estandar":
            mensaje = self.controlador.aplicar_descuento(self.numero_poliza)
        elif modo == "porcentaje":
            try:
                pct = float(self.pct_var.get())
            except ValueError:
                messagebox.showerror(
                    "Error", "Ingresa un número válido.", parent=self
                )
                return
            mensaje = self.controlador.aplicar_descuento(
                self.numero_poliza, porcentaje=pct
            )
        else:
            mensaje = self.controlador.aplicar_descuento(
                self.numero_poliza, cupon=self.cupon_var.get().strip()
            )

        if mensaje.startswith("ERROR"):
            messagebox.showerror("Error", mensaje, parent=self)
        else:
            messagebox.showinfo("Éxito", mensaje, parent=self)
            self.event_generate("<<DescuentoAplicado>>", when="tail")
            self.destroy()
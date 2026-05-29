import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from DominioTerror import Usuario, Admin, Cliente, Producto
from Conexion import Conexion

class Ventana_usuario:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Tiendas Terror - Usuario")
        self.ventana.geometry("800x650")
        self.ventana.resizable(False, False)

        self.contenedor = tk.Frame(self.ventana, padx=25, pady=30)
        self.contenedor.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = tk.Label(self.contenedor, text="Bienvenido a la Tienda Terror.\n Por favor inicie sesion", font=("Comic Sans MS", 16, "bold"))
        lbl_titulo.pack(pady=20)

        tk.Label(self.contenedor, text="Tipo de Usuario:", font=("Comic Sans MS", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.cmb_tipo_usuario = ttk.Combobox(self.contenedor, values=["Cliente", "Administrador"], state="readonly")
        self.cmb_tipo_usuario.pack(fill=tk.X, pady=5)
        self.cmb_tipo_usuario.current(0)

        tk.Label(self.contenedor, text="Nombre del usuario", font=("Comic Sans MS", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.txt_nombre = tk.Entry(self.contenedor, font=("Comic Sans MS", 10))
        self.txt_nombre.pack(fill=tk.X, pady=10)

        tk.Label(self.contenedor, text="Correo", font=("Comic Sans MS", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.txt_correo = tk.Entry(self.contenedor, font=("Comic Sans MS", 10))
        self.txt_correo.pack(fill=tk.X, pady=10)

        tk.Label(self.contenedor, text="Contraseña", font=("Comic Sans MS", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.txt_contrasena = tk.Entry(self.contenedor, font=("Comic Sans MS", 10), show="*")
        self.txt_contrasena.pack(fill=tk.X, pady=10)

        ingresar_btn = tk.Button(
            self.contenedor, 
            text="Ingresar", 
            font=("Comic Sans MS", 11, "bold"), 
            bg="#04853A", 
            fg="white", 
            activebackground="#219653",
            activeforeground="white",
            command=self.comprobar_usuario
        )
        ingresar_btn.pack(fill=tk.X, pady=20, ipady=4)

    def comprobar_usuario(self):
        tipo_usuario = self.cmb_tipo_usuario.get()
        nombre = self.txt_nombre.get().strip()
        correo = self.txt_correo.get().strip()
        contrasena = self.txt_contrasena.get().strip()

        # 1. Validaciones básicas en la interfaz
        if not nombre or not correo or not contrasena:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return
        if not Usuario.validar_correo(correo):
            messagebox.showerror("Error", "Por favor ingrese un correo válido (debe incluir @ y .com).")
            return

        db = Conexion()
        usuario_bd = db.consultar_usuario(correo, contrasena, tipo_usuario)

        if usuario_bd:
            if tipo_usuario == "Administrador":
                
                objeto_admin = Admin.crear_desde_bd(usuario_bd)
                objeto_admin.iniciar_sesion()
                messagebox.showinfo("Éxito", f"¡Acceso Permitido!\nBienvenido Admin {objeto_admin.nombre}")
                
                self.ventana.withdraw()
                Ventana_admin(self.ventana, objeto_admin)
            else:
                
                objeto_cliente = Cliente.crear_desde_la_bd(usuario_bd)
                objeto_cliente.iniciar_sesion()
                messagebox.showinfo("Éxito", f"¡Acceso Permitido!\nBienvenido Cliente {objeto_cliente.nombre}")
                
                self.ventana.withdraw()
                Ventana_cliente(self.ventana, objeto_cliente)
        else:
            messagebox.showerror("Error de Autenticación", "Las credenciales no coinciden o no corresponden al rol seleccionado.")

class Ventana_admin:
    def __init__(self, ventana_usuario, admin_objeto):
        self.ventana_usuario = ventana_usuario
        self.admin_objeto = admin_objeto

        self.ventana = tk.Toplevel()
        self.ventana.title("Tienda de Terror - Administrador")
        self.ventana.geometry("800x650")
        self.ventana.resizable(False, False)


        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_todo)

        contenedor = tk.Frame(self.ventana, padx=25, pady=30)
        contenedor.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = tk.Label(contenedor, text=f"Gestion Inventario - Tiendas Terror {self.admin_objeto.nombre}", font=("Comic Sans MS", 16, "bold"))
        lbl_titulo.pack(pady=20)

        columnas = ("id", "nombre", "precio", "stock")
        self.tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", height=12)
    
        self.tabla.heading("id", text="ID Producto")
        self.tabla.heading("nombre", text="Nombre Producto")
        self.tabla.heading("precio", text="Precio Unitario")
        self.tabla.heading("stock", text="Cantidad en Stock")
        
    
        self.tabla.column("id", width=100, anchor="center")
        self.tabla.column("nombre", width=250, anchor="w")
        self.tabla.column("precio", width=150, anchor="center")
        self.tabla.column("stock", width=150, anchor="center")
        
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=10)

        
        btn_actualizar = tk.Button(
            contenedor, 
            text="🔄 Actualizar Inventario", 
            font=("Comic Sans MS", 10, "bold"), 
            bg="#0713BA", 
            fg="white",
            command=self.cargar_inventario
        )
        btn_actualizar.pack(side=tk.LEFT, padx=5, pady=10)

        btn_agregar = tk.Button(
            contenedor, 
            text="➕ Registrar Producto", 
            font=("Comic Sans MS", 10, "bold"), 
            bg="#0713BA", 
            fg="white",
            command=self.abrir_formulario_producto
        )
        btn_agregar.pack(side=tk.LEFT, padx=5)

        self.cargar_inventario()
        self.cargar_inventario()

    def cargar_inventario(self):
    
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
            

        db = Conexion()
        lista_productos_bd = db.obtener_todos_los_productos()
        
        for fila_bd in lista_productos_bd:
           
            prod_objeto = Producto.crear_desde_bd(fila_bd)
           
            self.tabla.insert("", tk.END, values=(
                prod_objeto.get_id_producto(),
                prod_objeto.nombre, 
                f"${prod_objeto.get_precio():,.2f}",
                prod_objeto.get_stock()
            ))


    def abrir_formulario_producto(self):
        subventana = tk.Toplevel(self.ventana)
        subventana.title("Registrar Nuevo Producto")
        subventana.geometry("350x400")
        subventana.resizable(False, False)
        subventana.transient(self.ventana)
        subventana.grab_set()

        lbl_form = tk.Label(subventana, text="Nuevo Producto", font=("Comic Sans MS", 12, "bold"), fg="#27AE60")
        lbl_form.pack(pady=15)

        tk.Label(subventana, text="Nombre del Producto:", font=("Comic Sans MS", 10, "bold")).pack(anchor="w", padx=30, pady=2)
        txt_nom = tk.Entry(subventana, font=("Comic Sans MS", 10))
        txt_nom.pack(fill=tk.X, padx=30, pady=5)

        tk.Label(subventana, text="Precio Unitario ($):", font=("Comic Sans MS", 10, "bold")).pack(anchor="w", padx=30, pady=2)
        txt_pre = tk.Entry(subventana, font=("Comic Sans MS", 10))
        txt_pre.pack(fill=tk.X, padx=30, pady=5)

        tk.Label(subventana, text="Cantidad Inicial (Stock):", font=("Comic Sans MS", 10, "bold")).pack(anchor="w", padx=30, pady=2)
        txt_sto = tk.Entry(subventana, font=("Comic Sans MS", 10))
        txt_sto.pack(fill=tk.X, padx=30, pady=5)

        def guardar_datos():
            nombre = txt_nom.get().strip()
            precio_str = txt_pre.get().strip()
            stock_str = txt_sto.get().strip()

            if not nombre or not precio_str or not stock_str:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                precio = float(precio_str)
                stock = int(stock_str)
                if precio <= 0 or stock < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser un número positivo y Stock un entero válido.")
                return

            db = Conexion()
            if db.insertar_producto(nombre, precio, stock):
                messagebox.showinfo("Éxito", f"¡Producto '{nombre}' registrado correctamente!")
                subventana.destroy()
                self.cargar_inventario()

        btn_guardar = tk.Button(
            subventana, 
            text="💾 Guardar Producto", 
            font=("Comic Sans MS", 11, "bold"), 
            bg="#07D255", 
            fg="white",
            command=guardar_datos
        )
        btn_guardar.pack(fill=tk.X, padx=30, pady=25, ipady=3)
    
    def cerrar_todo(self):
        self.ventana_usuario.destroy()
    


class Ventana_cliente:
    def __init__(self, ventana_usuario, cliente_objeto):
        self.ventana_usuario = ventana_usuario
        self.cliente_objeto = cliente_objeto

        self.ventana = tk.Toplevel()
        self.ventana.title("Tienda de Terror - Comprar Productos")
        self.ventana.geometry("800x650")
        self.ventana.resizable(False, False)
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_todo)

        contenedor = tk.Frame(self.ventana, padx=25, pady=30)
        contenedor.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = tk.Label(contenedor, text=f"Productos Disponibles - Cliente: {self.cliente_objeto.nombre}", font=("Comic Sans MS", 16, "bold"), fg="#0713BA")
        lbl_titulo.pack(pady=20)

        columnas = ("id", "nombre", "precio", "stock")
        self.tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", height=12)
        
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Producto")
        self.tabla.heading("precio", text="Precio Unitario")
        self.tabla.heading("stock", text="Disponible")
        
        self.tabla.column("id", width=80, anchor="center")
        self.tabla.column("nombre", width=300, anchor="w")
        self.tabla.column("precio", width=150, anchor="center")
        self.tabla.column("stock", width=120, anchor="center")
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=10)

        btn_comprar = tk.Button(
            contenedor, 
            text="🛍️ Comprar Producto Seleccionado", 
            font=("Comic Sans MS", 11, "bold"), 
            bg="#07D255", 
            fg="white",
            command=self.comprar
        )
        btn_comprar.pack(pady=5, ipady=4, fill=tk.X)

        btn_salir = tk.Button(
            contenedor, 
            text="Finalizar y Salir", 
            font=("Comic Sans MS", 11, "bold"), 
            bg="#DE0D3A", 
            fg="white",
            command=self.finalizar_compra
        )
        btn_salir.pack(pady=5, ipady=4, fill=tk.X)

        self.cargar_catalogo()

    def cargar_catalogo(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        db = Conexion()
        lista_productos_bd = db.obtener_todos_los_productos()
        
        for fila_bd in lista_productos_bd:
            prod_objeto = Producto.crear_desde_bd(fila_bd)
            self.tabla.insert("", tk.END, values=(
                prod_objeto.get_id_producto(),
                prod_objeto.nombre, 
                f"${prod_objeto.get_precio():,.2f}",
                prod_objeto.get_stock()
            ))

    def comprar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, seleccione un producto de la tabla.")
            return

        valores_fila = self.tabla.item(seleccion[0], "values")
        id_prod = int(valores_fila[0])
        nombre_prod = valores_fila[1]
        precio_prod = float(valores_fila[2].replace("$", "").replace(",", ""))
        stock_actual = int(valores_fila[3])

        if stock_actual <= 0:
            messagebox.showerror("Sin Stock", f"Lo sentimos, '{nombre_prod}' se encuentra agotado.")
            return

        cantidad_comprar = 1
        nuevo_stock = stock_actual - cantidad_comprar
       
        id_cliente = self.cliente_objeto.get_id_usuario() 

        db = Conexion()
        if db.registrar_venta(id_cliente, id_prod, cantidad_comprar, precio_prod, nuevo_stock):
            
            detalle_recibo = (
                f"===============================\n"
                f"        TIENDAS TERROR        \n"
                f"===============================\n"
                f"Cliente: {self.cliente_objeto.nombre}\n"
                f"Producto: {nombre_prod}\n"
                f"ID Producto: {id_prod}\n"
                f"Cantidad: {cantidad_comprar}\n"
                f"Precio Unitario: ${precio_prod:,.2f}\n"
                f"-------------------------------\n"
                f"TOTAL PAGADO: ${precio_prod:,.2f}\n"
                f"===============================\n"
                f"¡Su detalle de venta ha sido registrado!"
            )
            
            messagebox.showinfo("DETALLE DE COMPRA", detalle_recibo)
            self.cargar_catalogo()
    def finalizar_compra(self):
        messagebox.showinfo("Tiendas Terror", "¡Gracias por visitarnos! Vuelve pronto.")
        self.ventana.destroy()
        self.ventana_usuario.deiconify()

    def cerrar_todo(self):
        self.ventana_usuario.destroy()

app = Ventana_usuario()
app.ventana.mainloop()
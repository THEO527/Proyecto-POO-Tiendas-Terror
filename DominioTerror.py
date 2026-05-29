class Usuario:
    def __init__(self, id_usuario, nombre, contrasena, email, tipoUsuario):
        self.nombre = nombre
        self.__id_usuario = id_usuario
        self.__email = email  
        self.__contrasena = contrasena
        self.tipoUsuario = tipoUsuario
        if not self.validar_correo(email):
            raise ValueError("Correo electrónico no válido")

    def get_id_usuario(self):
        return self.__id_usuario

    def get_email(self):
        return self.__email

    def get_contrasena(self):
        return self.__contrasena

    def iniciar_sesion(self):
        pass

    @staticmethod
    def validar_correo(correo: str) -> bool:
        return "@" in correo and ".com" in correo
    

class Admin(Usuario):
    def __init__(self, id_usuario, nombre, contrasena, email):
        super().__init__(id_usuario, nombre, contrasena, email, "ADMINISTRADOR")

    def iniciar_sesion(self):
        print(f"Admin {self.nombre} ha iniciado sesión de administrador.")

    def gestionar_productos(self):
        print(f"[ADMIN] {self.nombre} está gestionando el inventario de Tiendas Terror.")

    @classmethod
    def crear_desde_bd(cls, fila_bd):
        return cls(
            id_usuario=fila_bd["idUsuario"],
            nombre=fila_bd["nombre"],
            contrasena=fila_bd["contrasena"], 
            email=fila_bd["correo"]
        )
        

class Cliente(Usuario):
    
    def __init__(self, id_usuario, nombre, contrasena, email, direccion="", telefono=""):
        super().__init__(id_usuario, nombre, contrasena, email, "CLIENTE")
        self.__direccion = direccion
        self.__telefono = telefono

    def get_direccion(self):
        return self.__direccion

    def get_telefono(self):
        return self.__telefono
    
    def iniciar_sesion(self):
        print(f"Cliente {self.nombre} ha iniciado sesión para realizar compras.")

    def realizar_compra(self, producto):
        print(f"[CLIENTE] {self.nombre} ha comprado el producto: {producto}.")

    @classmethod
    def crear_desde_la_bd(cls, fila_bd):
       

        return cls(
            id_usuario=fila_bd["idUsuario"],
            nombre=fila_bd["nombre"],
            contrasena=fila_bd["contrasena"],
            email=fila_bd["correo"],
            direccion=fila_bd.get("direccion", ""),
            telefono=fila_bd.get("telefono", "")
        )

class Producto:
    def __init__(self, id_producto, nombre, precio, stock):
        self.__id_producto = id_producto
        self.nombre = nombre
        self.__precio = precio
        self.__stock = stock

    def get_id_producto(self): 
        return self.__id_producto
    
    def get_precio(self): 
        return self.__precio
    
    def get_stock(self):
        return self.__stock

    def reducir_stock(self, cantidad):
        if cantidad > self.__stock:
            raise ValueError(f"No hay suficiente stock para {self.nombre}")
        self.__stock -= cantidad

    @classmethod
    def crear_desde_bd(cls, fila_bd):
       
        return cls(
            id_producto=fila_bd["idProducto"],
            nombre=fila_bd["nombre"], 
            precio=float(fila_bd["precio"]),
            stock=int(fila_bd["cantidadEnStock"]) 
        )


class Recibo:
    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad
        self.__precio_unitario = producto.get_precio()
        self.__subtotal = self.__precio_unitario * cantidad

    def get_subtotal(self):
        return self.__subtotal

    def get_precio_unitario(self):
        return self.__precio_unitario
    

class Venta:
    def __init__(self, id_venta, cliente: Cliente, detalles: list[Recibo]):
        self.__id_venta = id_venta
        self.cliente = cliente
        self.detalles = detalles
        self.__total = sum(detalle.get_subtotal() for detalle in detalles)

    def get_id_venta(self):
        return self.__id_venta

    def get_total(self):
        return self.__total
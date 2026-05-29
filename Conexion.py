import mysql.connector
from tkinter import messagebox

class Conexion:
    def __init__(self):
        self.configurar_conexion = {
            'host': 'localhost',
            'user': 'root',
            'password': '527101',
            'database': 'sistema_ventas'
        }
        
    def obtner_conexion(self):
        
        try:
            nueva_conexion = mysql.connector.connect(**self.configurar_conexion)
            print("Conexión a la base de datos establecida.")
            return nueva_conexion
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
            print(f"Error al conectar a la base de datos: {err}")
            return None

    def consultar_usuario(self, correo, contrasena, tipoUsuario):
        conexion = self.obtner_conexion()
        if not conexion:
            return None 
        
        tipoUsuario = "ADMINISTRADOR" if tipoUsuario == "Administrador" else "CLIENTE"
        CURSOR = conexion.cursor(dictionary=True)

        try:
            consulta = "SELECT * FROM Usuario WHERE correo = %s AND contrasena = %s AND tipoUsuario = %s"
            CURSOR.execute(consulta, (correo, contrasena, tipoUsuario))
            resultado = CURSOR.fetchone()
            return resultado
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Consulta", f"No se pudo consultar el usuario: {err}")
            print(f"Error al consultar el usuario: {err}")
            return None
        finally:
            CURSOR.close()
            conexion.close() 

    def obtener_todos_los_productos(self):
        conexion = self.obtner_conexion()
        if not conexion:
            return [] 
        
        CURSOR = conexion.cursor(dictionary=True)
        try:
            consulta = "SELECT * FROM producto"
            CURSOR.execute(consulta)
            resultados = CURSOR.fetchall() 
            return resultados
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los productos: {err}")
            return []
        finally:
            CURSOR.close()
            conexion.close()

    def insertar_producto(self, nombre, precio, stock):
        conexion = self.obtner_conexion()
        if not conexion:
            return False 
        
        CURSOR = conexion.cursor()
        try:
           
            consulta = "INSERT INTO producto (nombre, precio, cantidadEnStock) VALUES (%s, %s, %s)"
            CURSOR.execute(consulta, (nombre, precio, stock))
            conexion.commit() 
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error al Guardar", f"No se pudo registrar el producto: {err}")
            return False
        finally:
            CURSOR.close()
            conexion.close()

    def actualizar_stock_producto(self, id_producto, nueva_cantidad):
        conexion = self.obtner_conexion()
        if not conexion:
            return False
        
        CURSOR = conexion.cursor()
        try:
            consulta = "UPDATE producto SET cantidadEnStock = %s WHERE idProducto = %s"
            CURSOR.execute(consulta, (nueva_cantidad, id_producto))
            conexion.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo actualizar el inventario: {err}")
            return False
        finally:
            CURSOR.close()
            conexion.close()

    def registrar_venta(self, id_cliente, id_producto, cantidad, precio, nuevo_stock):
        conexion = self.obtner_conexion()
        if not conexion:
            return False
            
        cursor = conexion.cursor()
        try:
            total_venta = precio * cantidad
            consulta_venta = "INSERT INTO Venta (fecha, total, idCliente) VALUES (CURDATE(), %s, %s)"
            cursor.execute(consulta_venta, (total_venta, id_cliente))
            
            id_venta_generado = cursor.lastrowid
            
            consulta_detalle = """
                INSERT INTO DetalleVenta (cantidad, precioUnitario, idVenta, idProducto) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(consulta_detalle, (cantidad, precio, id_venta_generado, id_producto))
            
            consulta_stock = "UPDATE Producto SET cantidadEnStock = %s WHERE idProducto = %s"
            cursor.execute(consulta_stock, (nuevo_stock, id_producto))
            
            conexion.commit()
            return True
        except mysql.connector.Error as err:
            conexion.rollback() 
            messagebox.showerror("Error en Venta", f"No se pudo completar la transacción: {err}")
            return False
        finally:
            cursor.close()
            conexion.close()
import json
import mysql.connector
from mysql.connector import Error
from decouple import config


'''


Desafío 1: Sistema de Gestión de Productos
Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:

-ok-Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
-Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
-Implementar operaciones CRUD para gestionar productos del inventario.
-ok-Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
-Persistir los datos en archivo JSON.
'''
#----------------------------definición de clase base-----------------------------#
class productos:
    def __init__ (self, nombre, precio, cantidad_stock):
      
        self.__nombre = nombre
        self.__precio = self.validar_precio (precio)
        self.__cantidad_stock = self.validar_cantidad (cantidad_stock)
        
   
    @property
    def nombre (self):
        return self.__nombre
    
    @property
    def precio (self):
        return self.__precio
    
    @property
    def cantidad_stock (self):
        return self.__cantidad_stock
    

#-----control de datos -----#

        
    @cantidad_stock.setter
    def cantidad_stock (self, nueva_cantidad_stock):
        self.__cantidad_stock = self.validar_cantidad (nueva_cantidad_stock)
        
    def validar_cantidad (self, cantidad_stock):
        try:
            
            cantidad_stock = int (cantidad_stock)
            if cantidad_stock < 0:
                
                raise ValueError ("la cantidad stock debe ser un número positivo  \n")
            return cantidad_stock
        except ValueError:
            raise ValueError("la cantidad debe ser un número valido mayor a cero \n")
    
    @precio.setter
    def precio (self, nuevo_precio):
        self.__precio = self.validar_precio (nuevo_precio)
        
    def validar_precio (self, valor):
        try:
            valor_producto = float (valor)
            if valor_producto < 0:
                raise ValueError ("el valor debe ser un número positivo \n")
            return valor_producto
        except ValueError:
            raise ValueError("el valor debe ser un número valido mayor a cero \n")
            

        
    '''def __str__(self):
        return f"{self.__id}{self.__nombre} {self.__precio} {self.__cantidad_stock}"'''
        
#---------subclases------------------------#
class producto_electronicos (productos):
    def __init__(self, nombre, precio, cantidad_stock, garantia):
        super().__init__(nombre, precio, cantidad_stock)
        self.__garantia = self.validar_garantia (garantia)
                
    @property
    def garantia (self):
        return self.__garantia
    
    def validar_garantia (self, meses):
        try:
            cantidad_garantia = int (meses)
            if cantidad_garantia < 0:
                raise ValueError ("la cantidad debe ser un número positivo \n")
            return cantidad_garantia
        except ValueError:
            raise ValueError("la cantidad debe ser un número valido mayor a cero \n")
        
    @garantia.setter
    def garantia (self, nueva_garantia):
        self.__garantia = self.validar_garantia (nueva_garantia)
        
    '''def to_dict(self):
        data = super().to_dict()
        data ['Garantia'] = self.__garantia
        return data'''
    
    '''def __str__(self):
        return f"{super().__str__()} - Garantia: {self.__garantia}"'''
    
   
class producto_vestimenta (productos):
    def __init__(self, nombre, precio, cantidad_stock, categoria):
        super().__init__(nombre, precio, cantidad_stock)
        self.__categoria = categoria
                
    @property
    def categoria (self):
        return self.__categoria
    
    @categoria.setter
    def categoria (self, nueva_categoria):
        self.__categoria = nueva_categoria
        
   
    
   
   
   
#------gestion de productos-----------#    
class Gestion_Productos:
    def __init__(self):
        self.host = config ('DB_HOST')
        self.database=config ('DB_NAME')
        self.user=config ('DB_USER')
        self.password=config ('DB_PASSWORD')
        
    def connect (self):
        try:
            connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password
            )
            if connection.is_connected():
                return connection    
        except Error as e:
            print (f'Error al conectar a la base de datos: {e}')
            return None
      
    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                nombre_producto = producto.nombre.lower()
                
                verificar_consulta = "SELECT * FROM productos WHERE LOWER(nombre) =%s"
                cursor.execute(verificar_consulta,(nombre_producto,))
                resultado = cursor.fetchone()
                
                if resultado is not None:
                    print(f"El producto '{producto.nombre}' ya existe en la base de datos.")
                else:
                    
                    # Determinar el tipo de producto
                    tipo_producto = 'electronico' if isinstance(producto, producto_electronicos) else 'vestimenta'
                # Insertar el nuevo producto
                    insertar_producto_verificado = """
                    INSERT INTO productos (nombre, precio, cantidad_stock, tipo_producto)
                    VALUES (%s, %s, %s, %s)
                    """
                    values = (nombre_producto, producto.precio, producto.cantidad_stock,tipo_producto)
                    cursor.execute(insertar_producto_verificado, values)
                    
                
                # Obtener el ID del producto recién insertado
                    producto_id = cursor.lastrowid
                
                # Insertar en la tabla correspondiente según el tipo de producto
                    if isinstance(producto, producto_electronicos):
                        insertar_electronico = """
                        INSERT INTO productos_electronicos (id, garantia)
                        VALUES (%s, %s)
                        """
                        cursor.execute(insertar_electronico, (producto_id, producto.garantia))

                    elif isinstance(producto, producto_vestimenta):

                        insertar_vestimenta = """
                        INSERT INTO productos_vestimenta (id, categoria)
                        VALUES (%s, %s)
                        """
                        cursor.execute(insertar_vestimenta, (producto_id, producto.categoria))

                # Confirmar los cambios en la base de datos
                    connection.commit()
                    print(f"Producto {producto.nombre} creado correctamente.")
            #Cerrar la conexión y el cursor
                cursor.close()
                connection.close()
                print("Adios.")
            
            else:
                print("Error: No se pudo establecer conexión con la base de datos.")
                
            
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')


    def buscar_producto_por_nombre(self, nombre):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                nombre_producto = nombre.lower()
                
                verificar_consulta = "SELECT * FROM productos WHERE LOWER(nombre) =%s"
                cursor.execute(verificar_consulta,(nombre_producto,))
                resultados = cursor.fetchone()
                
                #CODIGO AGREGADO
                 # Obtener los nombres de las columnas
                columnas = [desc[0] for desc in cursor.description]
                
                if resultados is not None:
                     print("Productos encontrados:")
                 # Mostrar los nombres de las columnas
                     print("\t".join(columnas))  # Imprimir nombres de columnas separados por tabulaciones
                    
                    # Mostrar los valores de cada producto
                     print("\t".join([str(valor) for valor in resultados]))  # Corregido: No iterar sobre resultados
                  #CODIGO AGREGADO ARRIBA
                
                 #LO DE AQUI ABAJO
                
                    #LO DE AQUI ARRIBA
                else:
                    print("prudcto no encontrado")   

                    #Cerrar la conexión y el cursor
                cursor.close()
                connection.close()
                print("Adios.")
            
            else:
                print("Error: No se pudo establecer conexión con la base de datos.")
                 
            
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')
    

 
        
    def eliminar_producto (self,id_producto):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                
                id_producto_buscar = int (id_producto)
                
                verificar_consulta_id = "SELECT * FROM productos WHERE id = %s"
                cursor.execute(verificar_consulta_id,(id_producto_buscar,))
                resultado = cursor.fetchone()
                #print( f'termine busqueda de producto resultado: {resultado}')
                if resultado is not None:
                    eliminar_producto = "DELETE FROM productos WHERE id = %s"
                    cursor.execute(eliminar_producto, (id_producto,))
                    connection.commit()
                    print(f"Producto con ID {id_producto} eliminado correctamente1.")
                else:
                    print("Producto no encontrado.")
                    
               
            #Cerrar la conexión y el cursor
                cursor.close()
                connection.close()
                print("Adios.")
            
            else:
                print("Error: No se pudo establecer conexión con la base de datos.")
                  
            
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')

    def modificar_stock(self, id_producto, nuevo_stock):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                
                id_producto_buscar = int (id_producto)
                
                
                verificar_consulta_id = "SELECT * FROM productos WHERE id = %s"
                cursor.execute(verificar_consulta_id,(id_producto_buscar,))
                resultado = cursor.fetchone()
                
                if resultado is not None:
                    modificar_stock_producto = "UPDATE productos SET cantidad_stock = %s WHERE id = %s"
                    cursor.execute(modificar_stock_producto, (nuevo_stock, id_producto,))
                    connection.commit()
                    print(f"Producto con ID {id_producto} modificado correctamente.")
                else:
                    print("Producto no encontrado.")
                    
               
            #Cerrar la conexión y el cursor
                cursor.close()
                connection.close()
                print("Adios.")
            
            else:
                print("Error: No se pudo establecer conexión con la base de datos.")
               
            
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')
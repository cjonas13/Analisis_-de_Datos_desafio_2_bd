import os
import platform


from laboratorio import (
    producto_electronicos,
    producto_vestimenta,
    Gestion_Productos,
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs

def mostrar_menu():
    print("========== Menú de Gestión de Colaboradores ==========")
    print('1. Agregar Producto Electronico')
    print('2. Agregar Producto Vestimenta')
    print('3. Buscar Producto por Nombre')
    print('4. Eliminar Producto por ID')
    print('5. Moficiar cantidad de stock')
    print('7. Salir del programa')
    
    
def agregar_producto (Gestion_Productos, tipo_producto):
  
    try:

        if tipo_producto == '1':
            nombre = input('Ingrese nombre del producto electrónico: ').strip().lower()  # Convertir a minúsculas
            while True:
                try:
                    cantidad_stock = int(input('Ingrese cantidad de stock: '))
                    producto_electronicos("", 0, cantidad_stock, 0)  #validar stock
                    break  # Si pasa la validación, salgo del while
                except ValueError as e:
                    print(f"Error: {e}. Intente de nuevo.")
            precio = float(input('Ingrese precio del producto: '))
            garantia = int(input('Ingrese garantia en cantidad de meses: '))
            
            
            
            producto = producto_electronicos(nombre, precio, cantidad_stock, garantia)
            
            
        elif tipo_producto == '2':
            nombre = input('Ingrese nombre del producto de vestimenta: ').strip().lower()  # Convertir a minúsculas
            cantidad_stock = int(input('Ingrese cantidad de stock: '))
            precio = float(input('Ingrese precio del producto: '))
            categoria = input('Ingrese categoria de la vestimenta: ').strip().lower()  # Convertir a minúsculas
           
            producto = producto_vestimenta(nombre, precio, cantidad_stock, categoria)
            
            
        else:
            print('Opción inválida')
            return

        Gestion_Productos.crear_producto(producto)
        input('Presione enter para continuar ...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}') 

def encontrar_producto(nombre):
    
    resultados = Gestion_Productos.buscar_producto_por_nombre(nombre)
    if resultados:
        print("Productos encontrados:")
        #for producto in resultados:
         #   print(producto)
    else:
        
        input('Presione enter para continuar...')
    
def borrar_producto (Gestion_Productos):   
    id_producto = input('Ingrese el ID del producto a eliminar: ')
    Gestion_Productos.eliminar_producto(id_producto)
    

def modificar_cantidad_stock (Gestion_Productos):   
    id_producto = input('Ingrese el ID del producto a modificar: ')
    nuevo_stock = input ('Ingrese el nuevo Stock: ')
    Gestion_Productos.modificar_stock(id_producto, nuevo_stock)
    
    
if __name__ == "__main__":
    
    Gestion_Productos = Gestion_Productos()

        
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_producto(Gestion_Productos, opcion)
        
        elif opcion == '3':  
            nombre = input('Ingrese el nombre del producto a buscar: ')
            resultados = encontrar_producto(nombre)
        
        elif opcion == '4':    
            borrar_producto (Gestion_Productos)
            input('Presione enter para continuar...')
        
        elif opcion == '5':    
            modificar_cantidad_stock(Gestion_Productos)
            input('Presione enter para continuar...')
            
        elif opcion == '7':
            print('Saliendo del programa...')
            break
        
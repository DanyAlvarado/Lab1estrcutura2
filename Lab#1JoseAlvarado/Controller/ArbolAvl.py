import json
import os

class cliente:
    def __init__(self, Nombre, Dpi, fecha_nacimiento, Direccion):
        self.Nombre = Nombre
        self.Dpi = Dpi
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = Direccion

class Nodo:
    def __init__(self, cliente):
        # "dato" puede ser de cualquier tipo, incluso un objeto si se sobrescriben los operadores de comparación
        self.cliente = cliente
        self.izquierda = None
        self.derecha = None

class ArbolAvl:
    def __init__(self):
        self.raiz = None
        self.clientes_eliminados = []
        self.clientes_actualizados = []
         
    
    # Insertar un cliente en el árbol AVL
    def agregar(self, cliente):
        if not self.raiz:
            self.raiz = Nodo(cliente)
        else:
            self.raiz = self.__agregar_recursivo(self.raiz, cliente)
    
    def __agregar_recursivo(self, nodo, cliente):
        if nodo is None:
            return Nodo(cliente)
        
        if cliente.Dpi < nodo.cliente.Dpi:
            nodo.izquierda = self.__agregar_recursivo(nodo.izquierda, cliente)
        else:
            nodo.derecha = self.__agregar_recursivo(nodo.derecha, cliente)
        
        # Calcular el factor de equilibrio
        factor_equilibrio = self.__calcular_factor_equilibrio(nodo)
        
        # Rotaciones para reequilibrar el árbol AVL
        if factor_equilibrio > 1:
            if cliente.Dpi < nodo.izquierda.cliente.Dpi:
                return self.__rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.__rotacion_izquierda(nodo.izquierda)
                return self.__rotacion_derecha(nodo)
        if factor_equilibrio < -1:
            if cliente.Dpi > nodo.derecha.cliente.Dpi:
                return self.__rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.__rotacion_derecha(nodo.derecha)
                return self.__rotacion_izquierda(nodo)
        
        return nodo
    
    def buscar(self, dpi):
        return self.__buscar_recursivo(self.raiz, dpi)

    def __buscar_recursivo(self, nodo, dpi):
        if nodo is None:
            return None

        if dpi == nodo.cliente.Dpi:
            return nodo  # Devuelve el nodo completo

        if dpi < nodo.cliente.Dpi:
            return self.__buscar_recursivo(nodo.izquierda, dpi)
        else:
            return self.__buscar_recursivo(nodo.derecha, dpi)

    def __calcular_factor_equilibrio(self, nodo):
        return self.__altura(nodo.izquierda) - self.__altura(nodo.derecha)
    
    def __altura(self, nodo):
        if nodo is None:
            return 0
        return max(self.__altura(nodo.izquierda), self.__altura(nodo.derecha)) + 1
    
    def __rotacion_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        
        y.derecha = z
        z.izquierda = T3
        
        return y
    
    def __rotacion_izquierda(self, y):
        x = y.derecha
        T2 = x.izquierda
        
        x.izquierda = y
        y.derecha = T2
        
        return x
    
    def eliminar(self, dpi):
        cliente_eliminado, self.raiz = self.__eliminar_recursivo(self.raiz, dpi)
        if cliente_eliminado:
            self.clientes_eliminados.append(cliente_eliminado)
        return cliente_eliminado



    def __eliminar_recursivo(self, nodo, dpi):
        if nodo is None:
            # No se encontró el nodo a eliminar
            return False, nodo

        if dpi < int(nodo.cliente.Dpi):  # Convertir nodo.cliente.Dpi en un entero para comparar
            eliminado, nodo.izquierda = self.__eliminar_recursivo(nodo.izquierda, dpi)
        elif dpi > int(nodo.cliente.Dpi):  # Convertir nodo.cliente.Dpi en un entero para comparar
            eliminado, nodo.derecha = self.__eliminar_recursivo(nodo.derecha, dpi)
        else:
            # Nodo encontrado, eliminarlo y agregar el DPI a la lista de eliminados
            eliminado = True
            self.clientes_eliminados.append(nodo.cliente.Dpi)  # Agregar solo el DPI

            # Resto del código para eliminar el nodo, sin cambios

        # Resto del código para mantener el balance del árbol, sin cambios
        return eliminado, nodo



    def __encontrar_sucesor(self, nodo):
        if nodo.izquierda is None:
            return nodo
        return self.__encontrar_sucesor(nodo.izquierda)

    

    def __actualizar_factor_equilibrio(self, nodo):
        factor_equilibrio = self.__calcular_factor_equilibrio(nodo)

        if factor_equilibrio > 1:
            if self.__calcular_factor_equilibrio(nodo.izquierda) >= 0:
                return self.__rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.__rotacion_izquierda(nodo.izquierda)
                return self.__rotacion_derecha(nodo)
        elif factor_equilibrio < -1:
            if self.__calcular_factor_equilibrio(nodo.derecha) <= 0:
                return self.__rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.__rotacion_derecha(nodo.derecha)
                return self.__rotacion_izquierda(nodo)

        return nodo
    
    def actualizar_datos_por_dpi(self, dpi, nueva_fecha_nacimiento=None, nueva_direccion=None):
        nodo, _ = self.__buscar_por_dpi_recursivo(self.raiz, dpi, None)  # Cambia esta línea
        if nodo is not None:
            # Actualizar fecha de nacimiento si se proporciona
            if nueva_fecha_nacimiento is not None:
                nodo.cliente.fecha_nacimiento = nueva_fecha_nacimiento

            # Actualizar dirección si se proporciona
            if nueva_direccion is not None:
                nodo.cliente.direccion = nueva_direccion

            # Agregar el DPI a la lista de clientes actualizados
            self.clientes_actualizados.append(dpi)  # Agregar DPI actualizado
            print(f"Datos actualizados para DPI {dpi}")
        else:
            print(f"No se encontró ningún cliente con DPI {dpi}, no se realizaron actualizaciones.")
    
    def __buscar_por_dpi_recursivo(self, nodo, dpi, padre):
        if nodo is None:
            return None, padre

        if dpi == nodo.cliente.Dpi:
            return nodo, padre
        elif dpi < nodo.cliente.Dpi:
            return self.__buscar_por_dpi_recursivo(nodo.izquierda, dpi, nodo)
        else:
            return self.__buscar_por_dpi_recursivo(nodo.derecha, dpi, nodo)
    
    def buscar_por_nombre(self, nombre):
        clientes_encontrados = []
        self.__buscar_por_nombre_recursivo(self.raiz, nombre.lower(), clientes_encontrados)
        return clientes_encontrados

    def __buscar_por_nombre_recursivo(self, nodo, nombre, clientes_encontrados):
        if nodo is None:
            return

        # Compara el nombre (ignora mayúsculas y minúsculas)
        if nombre == nodo.cliente.Nombre.lower():
            clientes_encontrados.append(nodo)

        self.__buscar_por_nombre_recursivo(nodo.izquierda, nombre, clientes_encontrados)
        self.__buscar_por_nombre_recursivo(nodo.derecha, nombre, clientes_encontrados)


class leerjason:
    def procesar_json_y_agregar_al_arbol(self, file_path, arbol):
        with open(file_path, "r") as f:
            for line in f:
                if line.startswith("INSERT; "):
                    json_data = line[len("INSERT; "):]

                    try:
                        data = json.loads(json_data)
                
                        Nombre = data["name"]
                        Dpi = data["dpi"]
                        Fecha_nacimiento = data["dateBirth"]
                        Direccion = data["address"]
                        nuevo_cliente = cliente(Nombre, Dpi, Fecha_nacimiento, Direccion)
                        arbol.agregar(nuevo_cliente)  # Agregar el cliente al árbol AVL

                        print("Insertado:")
                        print("name: " + Nombre)
                        print("dpi: " + Dpi)
                        print("date_birth: " + Fecha_nacimiento)
                        print("address: " + Direccion)
                
                    except json.JSONDecodeError:
                        print("Error al decodificar JSON en la línea:", line)

                if line.startswith("DELETE; "):
                    json_data = line[len("DELETE; "):]

                    try:
                        data = json.loads(json_data)
                    
                        dpi = int(data["dpi"])  # Convierte el DPI del JSON a un entero
                        # Eliminar el cliente del árbol por DPI
                        eliminado = arbol.eliminar(dpi)
                        if eliminado:
                            print(f"Cliente con DPI {dpi} eliminado exitosamente.")
                        else:
                            print(f"Cliente con DPI {dpi} no encontrado para eliminar.")
                    
                    except json.JSONDecodeError:
                        print("Error al decodificar JSON en la línea:", line)
                
                elif line.startswith("PATCH;"):
                    json_data = line[len("PATCH;"):]
                    date_birth = None
                    addres = None

                    try:
                        data = json.loads(json_data)
                        dpi = data.get("dpi")
                        fecha_nacimiento = data.get("dateBirth")
                        direccion = data.get("address")

                        if fecha_nacimiento is not None or direccion is not None:
                            arbol.actualizar_datos_por_dpi(dpi, nueva_fecha_nacimiento=fecha_nacimiento, nueva_direccion=direccion)
                        else:
                            print(f"No se proporcionaron datos válidos para actualizar en la línea: {line}")
                            
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar JSON en la línea: {line}")
                        print(f"Detalles del error: {e}")


def limpiar_consola():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print('\n' * 100)





class menu_principal:
    def __init__(self, arbol):
        self.arbol = arbol
        self.clientes_eliminados = []
        self.clientes_actualizados = []
            
    def mostrar_menu(self):
        while True:
            print("---------------------------")
            print("1. Ver bitácora de clientes")
            print("---------------------------")
            print("2. Eliminar clientes")
            print("---------------------------")
            print("3. Actualizar")
            print("---------------------------")
            print("4. Buscar cliente por DPI")
            print("---------------------------")
            print("5. Buscar cliente por Nombre")
            print("---------------------------")
            print("6. Salir")
            op = input("Ingrese la opción a la que desea ingresar: ")

            if op == "1":
                print("Estos son los clientes existentes:")
                self.mostrar_clientes()
                op1 = input("Ingrese 'Si' si desea volver a realizar esta acción: ")
                if op1 != "Si":
                    limpiar_consola()

            elif op == "2":
                print('Estos son los clientes eliminados:')
                self.mostrar_clientes_eliminados()
                op1 = input("Ingrese 'Si' si desea volver a realizar esta acción: ")
                if op1 != "Si":
                    limpiar_consola()
                    

            elif op == "3":
                print('Estos son los clientes actualizados:')
                self.mostrar_clientes_actualizados()
                op1 = input("Ingrese 'Si' si desea volver a realizar esta acción: ")
                if op1 != "Si":
                    limpiar_consola()
            
            elif op == "4":
                self.buscar_cliente_por_dpi()
            
            elif op == "5":
                self.buscar_cliente_por_nombre()
                

            elif op == "6":
                # Salir del programa
                break
                
        
        
    def mostrar_clientes(self):
        # Recorrer el árbol AVL e imprimir los datos de los clientes
        self.__mostrar_clientes_recursivo(self.arbol.raiz)

    def __mostrar_clientes_recursivo(self, nodo):
        if nodo is not None:
            self.__mostrar_clientes_recursivo(nodo.izquierda)
            cliente = nodo.cliente
            print("Nombre:", cliente.Nombre)
            print("DPI:", cliente.Dpi)
            print("Fecha de nacimiento:", cliente.fecha_nacimiento)
            print("Dirección:", cliente.direccion)
            print("---------------------------")
            self.__mostrar_clientes_recursivo(nodo.derecha)
        
    def mostrar_clientes_eliminados(self):
        print("Clientes eliminados:")
        for dpi in self.arbol.clientes_eliminados:  # Recorre la lista de DPI eliminados
            print("DPI:", dpi)
            print("---------------------------")


    def mostrar_clientes_actualizados(self):
        if self.clientes_actualizados:
            print('Clientes Actualizados:')
            for dpi in self.clientes_actualizados:
                print('DPI:', dpi)
            print("---------------------------")
        else:
            print('No hay clientes actualizados.')
    
    def buscar_cliente_por_dpi(self):
        while True:
            dpi = input("Ingrese el DPI del cliente que desea buscar (o 'menu' para volver al menú principal): ")
            
            if dpi.lower() == 'menu':
                break
            
            try:
                dpi = str(int(dpi))  # Convierte el DPI ingresado a un entero y luego a cadena de texto para la búsqueda
                cliente_encontrado = self.arbol.buscar(dpi)
            
                if cliente_encontrado:
                    print("Cliente encontrado:")
                    print("Nombre:", cliente_encontrado.cliente.Nombre)
                    print("DPI:", cliente_encontrado.cliente.Dpi)
                    print("Fecha de nacimiento:", cliente_encontrado.cliente.fecha_nacimiento)
                    print("Dirección:", cliente_encontrado.cliente.direccion)
                else:
                    print(f"No se encontró ningún cliente con DPI {dpi}.")
            except ValueError:
                print("Por favor, ingrese un número de DPI válido.")
    
    def buscar_cliente_por_nombre(self):
        while True:
            nombre = input("Ingrese el nombre del cliente que desea buscar (o 'menu' para volver al menú principal): ")
            
            if nombre.lower() == 'menu':
                break
            
            clientes_encontrados = self.arbol.buscar_por_nombre(nombre)
            
            if clientes_encontrados:
                print("Clientes encontrados:")
                for cliente_encontrado in clientes_encontrados:
                    print("Nombre:", cliente_encontrado.cliente.Nombre)
                    print("DPI:", cliente_encontrado.cliente.Dpi)
                    print("Fecha de nacimiento:", cliente_encontrado.cliente.fecha_nacimiento)
                    print("Dirección:", cliente_encontrado.cliente.direccion)
                    print("---------------------------")
            else:
                print(f"No se encontraron clientes con el nombre '{nombre}'.")
    
    



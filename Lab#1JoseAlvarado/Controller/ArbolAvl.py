import json
import os
from io import StringIO
from os.path import isfile, join
import math






class cliente:
    def __init__(self, Nombre, Dpi, fecha_nacimiento, Direccion, companies, mensaje, rcifrado, dcifrado):

        self.Nombre = Nombre
        self.Dpi = Dpi
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = Direccion
        self.companies = companies if companies is not None else []
        self.mensaje = mensaje if mensaje is not None else []
        self.rcifrado = rcifrado
        self.dcifrado = dcifrado
        # self.encode = encode
        # self.decode = decode
        # self.nuevo_dpi = nuevo_dpi
        # self.solo_empresas = solo_empresas if solo_empresas is not None else []
        
        
        

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
        if z is None or z.izquierda is None:
            return z

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



    def eliminar(self, Dpi):
        eliminado, self.raiz = self.__eliminar_recursivo(self.raiz, Dpi)
        dpi = Dpi
        if eliminado:
            self.clientes_eliminados.append(dpi)  
        return eliminado

    def __eliminar_recursivo(self, nodo, Dpi):
        if nodo is None:
            # No se encontró el nodo a eliminar
            return False, nodo

        if Dpi < nodo.cliente.Dpi:
            eliminado, nodo.izquierda = self.__eliminar_recursivo(nodo.izquierda, Dpi)
        elif Dpi > nodo.cliente.Dpi:
            eliminado, nodo.derecha = self.__eliminar_recursivo(nodo.derecha, Dpi)
        else:
            # Nodo encontrado, realizar eliminación
            if nodo.izquierda is None:
                return True, nodo.derecha
            elif nodo.derecha is None:
                return True, nodo.izquierda

            # Nodo con dos hijos, encontrar sucesor inorden
            sucesor = self.__encontrar_sucesor(nodo.derecha)
            nodo.cliente = sucesor.cliente
            eliminado, nodo.derecha = self.__eliminar_recursivo(nodo.derecha, sucesor.cliente.Dpi)

        # Actualizar el factor de equilibrio y equilibrar el árbol
        nodo = self.__actualizar_factor_equilibrio(nodo)

        return eliminado, nodo
    
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



    def __encontrar_sucesor(self, nodo):
        if nodo.izquierda is None:
            return nodo
        return self.__encontrar_sucesor(nodo.izquierda)

    
    def actualizar_datos_por_dpi(self, dpi, nueva_fecha_nacimiento=None, nueva_direccion=None, nuevas_companies = None):
        nodo = self.__buscar_por_dpi_recursivo(self.raiz, dpi)  # Cambia esta línea

        if nodo is not None:
            # Actualizar fecha de nacimiento si se proporciona
            if nueva_fecha_nacimiento is not None:
                nodo.cliente.fecha_nacimiento = nueva_fecha_nacimiento

            # Actualizar dirección si se proporciona
            if nueva_direccion is not None:
                nodo.cliente.direccion = nueva_direccion

            if nuevas_companies is not None:
                nodo.cliente.companies = nuevas_companies if nuevas_companies is not None else [] 

            if nueva_fecha_nacimiento is not None or nueva_direccion is not None or nuevas_companies is not None:
                self.clientes_actualizados.append(dpi)  # Agregar DPI actualizado

            print(f"Datos actualizados para DPI {dpi}")
        else:
            print("Datos no actualizados")
    
    def buscar_por_dpi(self, dpi):
        return self.__buscar_por_dpi_recursivo(self.raiz, dpi)

    def __buscar_por_dpi_recursivo(self, nodo, dpi):
        if nodo is None:
            return None

        if dpi == nodo.cliente.Dpi:
            return nodo  # Devuelve el nodo completo

        if dpi < nodo.cliente.Dpi:
            return self.__buscar_por_dpi_recursivo(nodo.izquierda, dpi)
        else:
            return self.__buscar_por_dpi_recursivo(nodo.derecha, dpi)





   
class lz78:
    
    @staticmethod
    def comprimir(no_comprimido):
        """"""

        # Construir el diccionario.
        tamaño_diccionario = 1000
        diccionario = dict((chr(i), chr(i)) for i in range(tamaño_diccionario))

        w = ""
        resultado = []
        for c in no_comprimido:
            wc = w + c
            if wc in diccionario:
                w = wc
            else:
                resultado.append(diccionario[w])
                # Agregar wc al diccionario.
                diccionario[wc] = tamaño_diccionario
                tamaño_diccionario += 1
                w = c

        # Salida del código para w.
        if w:
            resultado.append(diccionario[w])
        return resultado

    @staticmethod
    def descomprimir(comprimido):
        tamaño_diccionario = 1000
        diccionario = dict((chr(i), chr(i)) for i in range(tamaño_diccionario))

        resultado = StringIO()
        w = comprimido.pop(0)
        resultado.write(w)
        for k in comprimido:
            if k in diccionario:
                entrada = diccionario[k]
            elif k == tamaño_diccionario:
                entrada = w + w[0]
            else:
                raise ValueError('No se puede descomprimir: %s' % k)
            resultado.write(entrada)

            diccionario[tamaño_diccionario] = w + entrada[0]
            tamaño_diccionario += 1

            w = entrada
        return resultado.getvalue()

class cifrado:

    # Encry

    @staticmethod
    def encryptMessage(msg): 
        key = "HACKER"
        cipher = "" 
    
        # track key indices 
        k_indx = 0
    
        msg_len = float(len(msg)) 
        msg_lst = list(msg) 
        key_lst = sorted(list(key)) 
    
        # calculate column of the matrix 
        col = len(key) 
        
        # calculate maximum row of the matrix 
        row = int(math.ceil(msg_len / col)) 
    
        # add the padding character '_' in empty 
        # the empty cell of the matix  
        fill_null = int((row * col) - msg_len) 
        msg_lst.extend('_' * fill_null) 
    
        # create Matrix and insert message and  
        # padding characters row-wise  
        matrix = [msg_lst[i: i + col]  
                for i in range(0, len(msg_lst), col)] 
    
        # read matrix column-wise using key 
        for _ in range(col): 
            curr_idx = key.index(key_lst[k_indx]) 
            cipher += ''.join([row[curr_idx]  
                            for row in matrix]) 
            k_indx += 1
    
        return cipher 
    
    # Decryption 
    @staticmethod
    def decryptMessage(cipher): 
        key = "HACKER"
        msg = "" 
    
        # track key indices 
        k_indx = 0
    
        # track msg indices 
        msg_indx = 0
        msg_len = float(len(cipher)) 
        msg_lst = list(cipher) 
    
        # calculate column of the matrix 
        col = len(key) 
        
        # calculate maximum row of the matrix 
        row = int(math.ceil(msg_len / col)) 
    
        # convert key into list and sort  
        # alphabetically so we can access  
        # each character by its alphabetical position. 
        key_lst = sorted(list(key)) 
    
        # create an empty matrix to  
        # store deciphered message 
        dec_cipher = [] 
        for _ in range(row): 
            dec_cipher += [[None] * col] 
    
        # Arrange the matrix column wise according  
        # to permutation order by adding into new matrix 
        for _ in range(col): 
            curr_idx = key.index(key_lst[k_indx]) 
    
            for j in range(row): 
                dec_cipher[j][curr_idx] = msg_lst[msg_indx] 
                msg_indx += 1
            k_indx += 1
    
        # convert decrypted msg matrix into a string 
        try: 
            msg = ''.join(sum(dec_cipher, [])) 
        except TypeError: 
            raise TypeError("This program cannot", 
                            "handle repeating words.") 
    
        null_count = msg.count('_') 
    
        if null_count > 0: 
            return msg[: -null_count] 
    
        return msg





            




class leerjason:
    def procesar_archivos_txt(self, ruta, dpi, arbol):
        contenido = os.listdir(ruta)

        for nombre in contenido:
            if isfile(join(ruta, nombre)) and nombre.endswith(".txt"):
                with open(join(ruta, nombre), 'r') as archivo:
                    mensaje = archivo.read()

                # Dividir el nombre del archivo en partes usando "-" como separador
                partes = nombre.split("-")

                # Verificar si el nombre del archivo tiene el formato adecuado
                if len(partes) == 3 and partes[0] == "CONV":
                    dpi = partes[1]  # El DPI se encuentra en la segunda parte

                    # Buscar el cliente en el árbol AVL
                    cliente_encontrado = arbol.buscar(dpi)

                    if cliente_encontrado:
                        # Agregar el mensaje a la lista de mensajes del cliente
                        if not hasattr(cliente_encontrado.cliente, 'mensajes'):
                            cliente_encontrado.cliente.mensajes = []
                        cliente_encontrado.cliente.mensajes.append(mensaje)

                        recomendacion = mensaje
                        cifrar = cifrado()

                        rcifrado = cifrar.encryptMessage(recomendacion)
                        cliente_encontrado.cliente.rcifrado = rcifrado

                        mdecodificado = rcifrado

                        dcifrado = cifrar.decryptMessage(mdecodificado)

                        cliente_encontrado.cliente.dcifrado = dcifrado
                    else:
                        print(f"No se encontró ningún cliente con DPI {dpi} para el mensaje.")
    def procesar_json_y_agregar_al_arbol(self, file_path, arbol):

         with open(file_path, "r") as f:
            for line in f:
                if line.startswith("INSERT;"):
                    json_data = line[len("INSERT;"):]

                    try:
                        data = json.loads(json_data)

                        Nombre = data["name"]
                        Dpi = data["dpi"]
                        Fecha_nacimiento = data.get("datebirth", None)
                        Direccion = data["address"]
                        companies = data.get("companies", [])

                        
                        # Llamar a la función para procesar archivos TXT y asignar mensajes
                        ruta_txt = r"C:\Users\Usuario\Desktop\inputs"  # Reemplaza con la ruta correcta
                        self.procesar_archivos_txt(ruta_txt, Dpi, arbol)

                        # Crear un nuevo cliente con los datos del JSON
                        nuevo_cliente = cliente(Nombre, Dpi, Fecha_nacimiento, Direccion, companies, mensaje=None, rcifrado= None, dcifrado = None)
                        
                        # Agregar el cliente al árbol AVL
                        arbol.agregar(nuevo_cliente)
                        
                        

                    except json.JSONDecodeError:
                        print("Error al decodificar JSON en la línea:", line)


            if line.startswith("DELETE;"):
                    json_data = line[len("DELETE;"):]

                    try:
                        data = json.loads(json_data)
                        Dpi = data["dpi"]
                        eliminado = arbol.eliminar(Dpi)
                        if eliminado:
                            print(f"Cliente con valor único {Dpi} eliminado exitosamente.")
                        else:
                            print(f"Cliente con valor único {Dpi} no encontrado para eliminar.")

                    except json.JSONDecodeError:
                        print("Error al decodificar JSON en la línea:", line)
                
            elif line.startswith("PATCH;"):
                
                    json_data = line[len("PATCH;"):]
                    fecha_nacimiento = None
                    direccion = None

                    try:
                        data = json.loads(json_data)
                        dpi = data.get("dpi")
                        fecha_nacimiento = data.get("datebirth")
                        Nombre = data.get("name")
                        direccion = data.get("address")
                        companies = data.get("companies", [])
                        

                        if fecha_nacimiento is not None or direccion is not None:
                            nuevas_companies = []
                            nuevas_companies.append(companies)
                            nueva_fecha_nacimiento=fecha_nacimiento
                            nueva_direccion=direccion
                            arbol.actualizar_datos_por_dpi(dpi, nueva_fecha_nacimiento, nueva_direccion, nuevas_companies)
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
            
    def mostrar_menu(self):
        while True:
            print("---------------------------")
            print("1. Mostar clientes")
            print("---------------------------")
            print("2. Buscar cliente por DPI")
            print("---------------------------")
            print("3. Salir")
            op = input("Ingrese la opción a la que desea ingresar: ")
            

            if op == "1":
                print("Estos son los clientes existentes:")
                self.mostrar_clientes()
                op1 = input("Ingrese 'Si' si desea volver a realizar esta acción: ")
                if op1 != "Si":
                    limpiar_consola()

            elif op == "2":
                # Buscar cliente por DPI
                self.buscar_cliente_por_dpi()
                limpiar_consola()
            elif op == "3":
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
            print("---------------------------")
            print("Número de Dpi: ", cliente.Dpi)
            print("---------------------------")
            print("Fecha de nacimiento:", cliente.fecha_nacimiento)
            print("---------------------------")
            print("Dirección:", cliente.direccion)
            print("---------------------------")
            print("Empresas del cliente:", cliente.companies)
            print("---------------------------")
            # Verificar si el cliente tiene un mensaje y mostrarlo si está presente
            if hasattr(cliente, 'mensaje'):
                print("Mensaje del archivo:", cliente.rcifrado)
            print("---------------------------")
            self.__mostrar_clientes_recursivo(nodo.derecha)


    
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
                    print("---------------------------")
                    print("Nombre:", cliente_encontrado.cliente.Nombre)
                    print("---------------------------")
                    print("Nùmero de Dpi: ", cliente_encontrado.cliente.Dpi)
                    print("---------------------------")
                    print("Fecha de nacimiento:", cliente_encontrado.cliente.fecha_nacimiento)
                    print("---------------------------")
                    print("Dirección:", cliente_encontrado.cliente.direccion)
                    print("---------------------------")
                    print("Empresas del cliente: ", cliente_encontrado.cliente.companies)
                    print("---------------------------")
                    print("Mensaje decifrado: ", cliente_encontrado.cliente.dcifrado)
                    print("---------------------------")
                else:
                    print(f"No se encontró ningún cliente con DPI {dpi}.")
            except ValueError:
                print("Por favor, ingrese un número de DPI válido.")

    
    



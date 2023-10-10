import sys
from ArbolAvl import ArbolAvl, menu_principal, leerjason

def main():
    # Crear una instancia de ArbolAvl
    arbol = ArbolAvl()
    
    # Crear una instancia de leerjason
    lector = leerjason()
    
    # Redirigir la salida estándar a un archivo temporal
    sys.stdout = open("temp_output.txt", "w")
    
    # Llamar al método para procesar el archivo JSON y agregar datos al árbol
    lector.procesar_json_y_agregar_al_arbol("C:/Users/Usuario/Desktop/inputs.txt", arbol)
    
    ##Restaurar la salida estándar original
    sys.stdout = sys.__stdout__
    
    # Crear una instancia de menu_principal y pasar el árbol como argumento
    menu = menu_principal(arbol)
    
    # Mostrar el menú principal
    menu.mostrar_menu()

if __name__ == "__main__":
    main()

    
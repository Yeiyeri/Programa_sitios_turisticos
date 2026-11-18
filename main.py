# Primera version: consulta de sitios turisticos desde consola.
import os
from PIL import Image
from sitios_turisticos import sitios_turisticos

#def verificar_imagenes():
    #print("Carpeta actual:", os.getcwd())

    #for sitio in sitios_turisticos:
        #ruta = sitio["imagen"]
        #print("Buscando:", os.path.abspath(ruta))
        #if os.path.exists(ruta):
            #print(f"Imagen encontrada: {sitio["nombre"]}")
        #else:
            #print(f"Imagen no encontrada: {sitio['nombre']}")

def mostrar_sitios():
    print("\n========== SITIOS TURISTICOS ==========")

    for indice, sitio in enumerate(sitios_turisticos, start=1):
        print(f"{indice}. {sitio['nombre']} - {sitio['tipo']}")

    print("=======================================")


def mostrar_detalles():
    mostrar_sitios()

    try:
        opcion = int(input("\nEscribe el numero del sitio que deseas consultar: "))

        if 1 <= opcion <= len(sitios_turisticos):
            sitio = sitios_turisticos[opcion - 1]
            print("\n========== DETALLES DEL SITIO ==========")
            print(f"Nombre: {sitio['nombre']}")
            print(f"Tipo: {sitio['tipo']}")
            print(f"Ubicacion: {sitio['ubicacion']}")
            print(f"Descripcion: {sitio['descripcion']}")
            imagen = Image.open(sitio["imagen"])
            imagen.show()
            enlace = f"https://www.google.com/maps?q={sitio['latitud']},{sitio['longitud']}"
            print(f"Google Maps: {enlace}")
            print("========================================")
        else:
            print("Opcion no valida. Selecciona un numero de la lista.")
    except ValueError:
        print("Entrada incorrecta. Debes escribir un numero.")


def mostrar_por_tipo():
    print("\nTipos de sitios disponibles:")
    print("1. Natural")
    print("2. Historico")
    print("3. Popular")

    tipos = {"1": "Natural", "2": "Historico", "3": "Popular"}
    opcion = input("Selecciona un tipo: ").strip()

    if opcion not in tipos:
        print("Tipo no valido.")
        return

    tipo_elegido = tipos[opcion]
    print(f"\n========== SITIOS: {tipo_elegido.upper()} ==========")

    encontrados = [
        sitio for sitio in sitios_turisticos
        if sitio["tipo"] == tipo_elegido
    ]

    if encontrados:
        for sitio in encontrados:
            print(f"- {sitio['nombre']}: {sitio['ubicacion']}")
    else:
        print("No hay sitios registrados en esta categoria.")


def menu():
    while True:
        print("\n========== EXPLORAGUAJIRA ==========")
        print("1. Mostrar todos los sitios turisticos")
        print("2. Consultar detalles de un sitio")
        print("3. Buscar sitios por tipo")
        print("4. Salir")
        print("====================================")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            mostrar_sitios()
        elif opcion == "2":
            mostrar_detalles()
        elif opcion == "3":
            mostrar_por_tipo()
        elif opcion == "4":
            print("Gracias por utilizar ExploraGuajira.")
            break
        else:
            print("Opcion no valida. Intenta nuevamente.")


if __name__ == "__main__":
    #verificar_imagenes()
    menu()

#python servidor.py
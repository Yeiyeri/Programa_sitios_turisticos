sitios_turisticos = [
    {
        "nombre": "Cabo de la Vela",
        "tipo": "Natural",
        "ubicacion": "Uribia, La Guajira",
        "descripcion": (
            "Destino turístico conocido por sus paisajes desérticos, "
            "sus playas y su cultura Wayuu."
        )
    },
    {
        "nombre": "Punta Gallinas",
        "tipo": "Natural",
        "ubicacion": "Alta Guajira, La Guajira",
        "descripcion": (
            "Lugar reconocido por sus dunas, playas y paisajes "
            "naturales del extremo norte de Sudamérica."
        )
    },
    {
        "nombre": "Santuario de Fauna y Flora Los Flamencos",
        "tipo": "Natural",
        "ubicacion": "Camarones, Riohacha",
        "descripcion": (
            "Área natural donde se pueden observar flamencos "
            "y otras especies de aves."
        )
    },
    {
        "nombre": "Salinas de Manaure",
        "tipo": "Popular",
        "ubicacion": "Manaure, La Guajira",
        "descripcion": (
            "Sitio conocido por la producción de sal y sus "
            "paisajes de estanques salineros."
        )
    },
    {
        "nombre": "Centro Histórico de Cartagena",
        "tipo": "Histórico",
        "ubicacion": "Cartagena de Indias, Bolívar",
        "descripcion": (
            "Zona histórica reconocida por su arquitectura colonial, "
            "sus murallas y sus calles tradicionales."
        )
    }
]


def mostrar_sitios():
    print("\n========== SITIOS TURÍSTICOS ==========")

    for indice, sitio in enumerate(sitios_turisticos, start=1):
        print(f"{indice}. {sitio['nombre']} - {sitio['tipo']}")

    print("=======================================")


def mostrar_detalles():
    mostrar_sitios()

    try:
        opcion = int(input("\nEscribe el número del sitio que deseas consultar: "))

        if 1 <= opcion <= len(sitios_turisticos):
            sitio = sitios_turisticos[opcion - 1]

            print("\n========== DETALLES DEL SITIO ==========")
            print(f"Nombre: {sitio['nombre']}")
            print(f"Tipo: {sitio['tipo']}")
            print(f"Ubicación: {sitio['ubicacion']}")
            print(f"Descripción: {sitio['descripcion']}")
            print("========================================")
        else:
            print("Opción no válida. Selecciona un número de la lista.")
    except ValueError:
        print("Entrada incorrecta. Debes escribir un número.")


def mostrar_por_tipo():
    print("\nTipos de sitios disponibles:")
    print("1. Natural")
    print("2. Histórico")
    print("3. Popular")

    tipos = {
        "1": "Natural",
        "2": "Histórico",
        "3": "Popular"
    }

    opcion = input("Selecciona un tipo: ").strip()

    if opcion not in tipos:
        print("Tipo no válido.")
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
        print("No hay sitios registrados en esta categoría.")


def menu():
    while True:
        print("\n========== EXPLORAGUAJIRA ==========")
        print("1. Mostrar todos los sitios turísticos")
        print("2. Consultar detalles de un sitio")
        print("3. Buscar sitios por tipo")
        print("4. Salir")
        print("====================================")

        opcion = input("Selecciona una opción: ").strip()

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
            print("Opción no válida. Intenta nuevamente.")


if __name__ == "__main__":
    menu()

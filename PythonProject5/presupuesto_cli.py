import json
import os

DATABASE_FILE = 'presupuesto.json'

def cargar_presupuesto():
    """Carga los datos del presupuesto desde el archivo JSON."""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

def guardar_presupuesto(presupuesto):
    """Guarda los datos del presupuesto en el archivo JSON."""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(presupuesto, f, indent=4)

def registrar_articulo(presupuesto):
    """Registra un nuevo artículo en el presupuesto."""
    print("\n--- Registrar Artículo ---")
    nombre = input("Nombre del artículo: ")
    try:
        monto = float(input("Monto del artículo: "))
        if monto <= 0:
            print("El monto debe ser mayor que cero.")
            return
    except ValueError:
        print("Monto inválido. Debe ingresar un número.")
        return

    articulo = {"nombre": nombre, "monto": monto}
    presupuesto.append(articulo)
    guardar_presupuesto(presupuesto)
    print(f"Artículo '{nombre}' registrado exitosamente.")

def buscar_articulo(presupuesto):
    """Busca artículos en el presupuesto por nombre."""
    print("\n--- Buscar Artículo ---")
    termino_busqueda = input("Ingrese el nombre del artículo a buscar: ").lower()
    resultados = [articulo for articulo in presupuesto if termino_busqueda in articulo['nombre'].lower()]
    if resultados:
        print("\n--- Resultados de la búsqueda ---")
        for i, articulo in enumerate(resultados):
            print(f"{i+1}. Nombre: {articulo['nombre']}, Monto: {articulo['monto']}")
    else:
        print(f"No se encontraron artículos con el nombre '{termino_busqueda}'.")

def editar_articulo(presupuesto):
    """Edita un artículo existente en el presupuesto."""
    print("\n--- Editar Artículo ---")
    if not presupuesto:
        print("No hay artículos registrados para editar.")
        return

    buscar_articulo(presupuesto)
    try:
        indice_editar = int(input("Ingrese el número del artículo que desea editar: ")) - 1
        if 0 <= indice_editar < len(presupuesto):
            articulo_editar = presupuesto[indice_editar]
            print(f"\nEditando: Nombre: {articulo_editar['nombre']}, Monto: {articulo_editar['monto']}")
            nuevo_nombre = input(f"Nuevo nombre (dejar en blanco para mantener '{articulo_editar['nombre']}'): ")
            nuevo_monto_str = input(f"Nuevo monto (dejar en blanco para mantener '{articulo_editar['monto']}'): ")

            if nuevo_nombre:
                articulo_editar['nombre'] = nuevo_nombre
            if nuevo_monto_str:
                try:
                    nuevo_monto = float(nuevo_monto_str)
                    if nuevo_monto <= 0:
                        print("El monto debe ser mayor que cero.")
                        return
                    articulo_editar['monto'] = nuevo_monto
                except ValueError:
                    print("Monto inválido. No se modificó el monto.")

            guardar_presupuesto(presupuesto)
            print(f"Artículo '{articulo_editar['nombre']}' editado exitosamente.")
        else:
            print("Número de artículo inválido.")
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")

def eliminar_articulo(presupuesto):
    """Elimina un artículo existente del presupuesto."""
    print("\n--- Eliminar Artículo ---")
    if not presupuesto:
        print("No hay artículos registrados para eliminar.")
        return

    buscar_articulo(presupuesto)
    try:
        indice_eliminar = int(input("Ingrese el número del artículo que desea eliminar: ")) - 1
        if 0 <= indice_eliminar < len(presupuesto):
            articulo_eliminado = presupuesto.pop(indice_eliminar)
            guardar_presupuesto(presupuesto)
            print(f"Artículo '{articulo_eliminado['nombre']}' eliminado exitosamente.")
        else:
            print("Número de artículo inválido.")
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")

def mostrar_presupuesto(presupuesto):
    """Muestra todos los artículos registrados en el presupuesto."""
    print("\n--- Presupuesto Actual ---")
    if presupuesto:
        for i, articulo in enumerate(presupuesto):
            print(f"{i+1}. Nombre: {articulo['nombre']}, Monto: {articulo['monto']}")
        total = sum(articulo['monto'] for articulo in presupuesto)
        print(f"\nTotal del presupuesto: {total:.2f}")
    else:
        print("El presupuesto está vacío.")

def main():
    """Función principal de la aplicación."""
    presupuesto = cargar_presupuesto()

    while True:
        print("\n--- Sistema de Registro de Presupuesto ---")
        print("1. Registrar Artículo")
        print("2. Buscar Artículo")
        print("3. Editar Artículo")
        print("4. Eliminar Artículo")
        print("5. Mostrar Presupuesto")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_articulo(presupuesto)
        elif opcion == '2':
            buscar_articulo(presupuesto)
        elif opcion == '3':
            editar_articulo(presupuesto)
        elif opcion == '4':
            eliminar_articulo(presupuesto)
        elif opcion == '5':
            mostrar_presupuesto(presupuesto)
        elif opcion == '6':
            print("Saliendo del sistema de presupuesto.")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
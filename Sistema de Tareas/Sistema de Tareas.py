from dbUtils import create_tables, insert_task, update_task, delete_task, get_conn, get_all_tasks
conn = get_conn()

def mostrar_menu():
    print("\n--- Menú de Tareas ---")
    print("1. Ver tareas")
    print("2. Agregar tarea")
    print("3. Eliminar tarea")
    print("4. Crear base de datos")
    print("5. Modificar Titulo")
    print("6. Salir")
    

def ver_tareas():
    tareas = get_all_tasks(conn)
    if not tareas:
        print("No hay tareas.")
    else:
        print("\nTareas:")
        for i, row in enumerate(tareas, start=1):   # OJO: start=1, no start-1
            # row es una tupla: (id, title, is_done)
            print(f"{i}. ID: {row[0]} | Descripción: {row[1]} | Estado: {row[2]}")


def agregar_tarea(nueva_tarea):
    if nueva_tarea:
        t1 = insert_task(conn, nueva_tarea)
        print("Tarea creada con id:", t1)
    else:
        print("La tarea no puede estar vacía.")

def eliminar_tarea(indice):
    filas = delete_task(conn, indice)
    if filas > 0:
        print(f"Tarea '{indice}' eliminada.")
    else:
        print("Índice inválido.")

def modificar_tarea(indice, title):
    filas = update_task(conn, indice, title)
    if filas > 0:
        print(f"Tarea '{indice}' modificada.")
    else:
        print("Índice inválido.")
        
def main():
    tareas = []
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            ver_tareas()
        elif opcion == "2":
            nueva = input("Escribe la nueva tarea: ")
            agregar_tarea(nueva)
        elif opcion == "3":
            ver_tareas()
            try:
                indice = int(input("Número de tarea a eliminar: "))
                eliminar_tarea(indice)
            except ValueError:
                print("Por favor, ingresa un número válido.")
        elif opcion == "4":
             create_tables()
        elif opcion == "5":
            ver_tareas()
            try:
                indice = int(input("Número de tarea a modificar: "))
                title = str(input("Ingrese el nuevo titulo de la tarea: "))
                if title != "":
                    modificar_tarea(indice, title)
                else:
                    print("ingrese el titulo. Intenta de nuevo.")
            except ValueError:
                print("Por favor, ingresa un número válido.")
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()

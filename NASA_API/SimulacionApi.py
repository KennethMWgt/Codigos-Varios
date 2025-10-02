from datetime import datetime
import requests
import dbUtils_mars

def mostrar_menu():
    print("\n--- Menú de Tareas ---")
    print("1. Generar Informacion")
    print("2. Extraer Json")
    print("3. Salir")
    
def Llamada_Api(fecha):
    url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    params = {
    "api_key": "SHMDr37hwS4DXp2FA5Zb9Nt4aaau52Tkxel0RUXL",   # cambia a tu key si tienes
    "earth_date": fecha     # opcional, formato YYYY-MM-DD
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        photos = data.get("photos",[])
        rovers = [] # datos desde la bd
        dbUtils_mars.create_tables()
        for photo in photos:
            nuevo_rover = {"id":  photo["rover"]["id"], "nombre": photo["rover"]["name"]}
            if not any(rover["id"] == nuevo_rover["id"] for rover in rovers):
                rovers.append(nuevo_rover)
                dbUtils_mars.insert_rover(nuevo_rover["id"], nuevo_rover["nombre"])
            print("---------Photos--------")
            print("ID:", photo["id"])
            print("Camera_ID:", photo["camera"]["id"]) 
            print("Image:", photo["img_src"])
            print("Earth Date:", photo["earth_date"])
            print("---------Camara--------")
            print("ID:", photo["camera"]["id"])
            print("Camera:", photo["camera"]["full_name"])
            print("Rover_ID:",photo["rover"]["id"])
            print("---------Rover--------")
            print("ID:",photo["rover"]["id"])
            print("Rover:", photo["rover"]["name"])
            print("-" * 120)
        print(rovers)
    else:
        print("Error:", response.status_code, response.text)
    
def main():
 
     while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            fecha = input("Ingrese la fecha para extraer la información (Formato: Año-Mes-Día): ")
            try:
                fecha_valida = datetime.strptime(fecha, "%Y-%m-%d")
                print("Fecha válida:", fecha_valida.date())
                Llamada_Api(fecha_valida)
            except ValueError:
                print("Fecha inválida. Asegúrese de usar el formato correcto (Año-Mes-Día) y que sea una fecha real.")
            
        #elif opcion == "2":
            #nueva_tarea = input("Escribe la nueva tarea: ")
            #agregar_tarea(nueva_tarea)
        
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
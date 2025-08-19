# empleados.py
def leer_empleados(archivo):
    empleados = []
    with open(archivo, 'r') as f:
        for line in f:
            # Dividimos los datos por coma y quitamos posibles espacios
            nombre, departamento, salario = line.strip().split(',')
            empleados.append({
                'nombre': nombre,
                'departamento': departamento,
                'salario': float(salario)  # Convertimos el salario a número flotante
            })
    return empleados


def salario_promedio(empleados):
    total_salario = sum(emp['salario'] for emp in empleados)
    return total_salario / len(empleados) if empleados else 0


def empleado_mas_ganador(empleados):
    if empleados:
        return max(empleados, key=lambda emp: emp['salario'])
    return None


def mostrar_resultados(empleados):
    promedio = salario_promedio(empleados)
    ganador = empleado_mas_ganador(empleados)
    print(f"Salario promedio: {promedio:.2f}")
    if ganador:
        print(f"El empleado que gana más es {ganador['nombre']} con un salario de {ganador['salario']}")

# Si este script se ejecuta directamente
if __name__ == "__main__":
    archivo = 'Leer_Archivo_Empleado\empleados.txt'  # Nombre del archivo
    empleados = leer_empleados(archivo)
    mostrar_resultados(empleados)

# test_empleados.py
import unittest
from empleados import leer_empleados, salario_promedio, empleado_mas_ganador

class TestEmpleados(unittest.TestCase):

    def setUp(self):
        # Preparamos un archivo de prueba en memoria (puedes ajustar según lo necesario)
        self.empleados_data = [
            {'nombre': 'Juan', 'departamento': 'ventas', 'salario': 2000},
            {'nombre': 'Maria', 'departamento': 'marketing', 'salario': 2500},
            {'nombre': 'Pedro', 'departamento': 'ventas', 'salario': 2800},
            {'nombre': 'Laura', 'departamento': 'finanzas', 'salario': 3000}
        ]

    def test_salario_promedio(self):
        promedio = salario_promedio(self.empleados_data)
        self.assertEqual(promedio, 2575)

    def test_empleado_mas_ganador(self):
        ganador = empleado_mas_ganador(self.empleados_data)
        self.assertEqual(ganador['nombre'], 'Laura')
        self.assertEqual(ganador['salario'], 3000)

    def test_leer_empleados(self):
        # Creamos un archivo de prueba
        with open('test_empleados.txt', 'w') as f:
            for emp in self.empleados_data:
                f.write(f"{emp['nombre']},{emp['departamento']},{emp['salario']}\n")
        
        empleados = leer_empleados('test_empleados.txt')
        self.assertEqual(len(empleados), 4)
        self.assertEqual(empleados[0]['nombre'], 'Juan')
        self.assertEqual(empleados[0]['salario'], 2000)

if __name__ == "__main__":
    unittest.main()

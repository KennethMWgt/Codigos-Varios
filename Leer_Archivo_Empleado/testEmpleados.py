# test_empleados.py
import unittest
from Leer_Archivo_Empleado.empleados import leer_empleados, salario_promedio, empleado_mas_ganador

class TestEmpleados(unittest.TestCase):

    def setUp(self):
        # Preparamos un archivo de prueba en memoria (puedes ajustar según lo necesario)
        self.empleados_data = leer_empleados('empleados.txt')

    def test_salario_promedio(self):
        promedio = salario_promedio(self.empleados_data)
        self.assertEqual(promedio, 2575)

    def test_empleado_mas_ganador(self):
        ganador = empleado_mas_ganador(self.empleados_data)
        self.assertEqual(ganador['nombre'], 'Laura')
        self.assertEqual(ganador['salario'], 3000)

    def test_leer_empleados(self):
               
        empleados = self.empleados_data
        self.assertEqual(len(empleados), 4)
        self.assertEqual(empleados[0]['nombre'], 'Juan')
        self.assertEqual(empleados[0]['salario'], 2000)

if __name__ == "__main__":
    unittest.main()

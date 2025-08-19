# test_stock.py
import unittest
import stock

class TestStock(unittest.TestCase):

    def setUp(self):
        # Reiniciamos el stock antes de cada test
        stock.stock = {"manzanas": 10, "naranjas": 8, "bananas": 15}

    def test_producto_inexistente(self):
        self.assertEqual(
            stock.verificar_stock("peras", 3),
            "❌ El producto 'peras' no existe en el inventario."
        )

    def test_cantidad_invalida(self):
        self.assertEqual(
            stock.verificar_stock("manzanas", 0),
            "⚠️ La cantidad debe ser mayor a 0."
        )

    def test_stock_suficiente(self):
        resultado = stock.verificar_stock("manzanas", 5)
        self.assertIn("✅ Se vendieron 5 manzanas", resultado)
        self.assertEqual(stock.stock["manzanas"], 5)

    def test_stock_insuficiente(self):
        resultado = stock.verificar_stock("naranjas", 20)
        self.assertIn("❌ Stock insuficiente", resultado)
        self.assertEqual(stock.stock["naranjas"], 8)

if __name__ == "__main__":
    unittest.main()
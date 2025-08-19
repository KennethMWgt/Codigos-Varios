import unittest
from Numeros_Primos.tarea_primos import es_primo 

class TestEsPrimo(unittest.TestCase):
    
    def test_primos(self):
        self.assertTrue(es_primo(2))
        self.assertTrue(es_primo(3))
        self.assertTrue(es_primo(7))
        self.assertTrue(es_primo(97))

    def test_no_primos(self):
        self.assertFalse(es_primo(0))
        self.assertFalse(es_primo(1))
        self.assertFalse(es_primo(4))
        self.assertFalse(es_primo(100))

if __name__ == '__main__':
    unittest.main()
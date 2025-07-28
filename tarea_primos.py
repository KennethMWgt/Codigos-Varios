def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

print("Números primos del 1 al 100:")
for num in range(1, 101):
    if es_primo(num):
        print(num, end=" ")

import unittest

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
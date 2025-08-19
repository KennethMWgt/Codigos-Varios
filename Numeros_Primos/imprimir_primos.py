from Numeros_Primos.es_primo import es_primo

print("Números primos del 1 al 100:")
for num in range(1, 101):
    if es_primo(num):
        print(num, end=" ")
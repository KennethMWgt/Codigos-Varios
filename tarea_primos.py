def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


if __name__ == '__main__':
    print("Números primos del 1 al 100:")
    for num in range(1, 101):
        if es_primo(num):
            print(num, end=" ")
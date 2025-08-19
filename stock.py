# stock.py

# Diccionario inicial con inventario
stock = {
    "manzanas": 10,
    "naranjas": 8,
    "bananas": 15
}

def verificar_stock(producto: str, cantidad: int) -> str:
    """
    Valida si hay suficiente inventario y actualiza el stock.
    Retorna un mensaje con el resultado.
    """
    producto = producto.lower()

    if producto not in stock:
        return f"❌ El producto '{producto}' no existe en el inventario."

    if cantidad <= 0:
        return "⚠️ La cantidad debe ser mayor a 0."

    if stock[producto] >= cantidad:
        stock[producto] -= cantidad
        return f"✅ Se vendieron {cantidad} {producto}. Stock restante: {stock[producto]}"
    else:
        return f"❌ Stock insuficiente de {producto}. Disponible: {stock[producto]}"

def ejecutar():
    """
    Interacción con el usuario para simular ventas.
    """
    print("=== SISTEMA DE CONTROL DE STOCK ===")
    print("Inventario inicial:", stock)

    while True:
        producto = input("Ingrese el producto (o 'salir' para terminar): ").lower()
        if producto == "salir":
            break

        try:
            cantidad = int(input("Ingrese la cantidad: "))
        except ValueError:
            print("⚠️ Debe ingresar un número válido.")
            continue

        print(verificar_stock(producto, cantidad))

    print("Inventario final:", stock)

if __name__ == "__main__":
    ejecutar()
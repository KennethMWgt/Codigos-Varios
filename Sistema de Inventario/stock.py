# stock.py

# Diccionario inicial con inventario
stock = {
    "manzanas": 10,
    "naranjas": 8,
    "bananas": 15
}

def agregar_producto(producto: str, cantidad: int):
    """
    Agrega un nuevo producto al inventario con la cantidad indicada.
    """
    producto = producto.lower()
    if cantidad <= 0:
        print("La cantidad debe ser mayor a 0 para agregar el producto.")
        return
    stock[producto] = cantidad
    print(f"Producto '{producto}' agregado con {cantidad} unidades.")

def actualizar_stock(producto: str, cantidad: int) -> str:
    """
    Valida si hay suficiente inventario y actualiza el stock.
    Retorna un mensaje con el resultado.
    """
    producto = producto.lower()

    if producto not in stock:
        return f"El producto '{producto}' no existe en el inventario."

    if cantidad <= 0:
        return "La cantidad debe ser mayor a 0."

    if stock[producto] >= cantidad:
        stock[producto] -= cantidad
        return f"Se vendieron {cantidad} {producto}. Stock restante: {stock[producto]}"
    else:
        return f"Stock insuficiente de {producto}. Disponible: {stock[producto]}"

def ejecutar():
    """
    Interacción con el usuario para simular ventas.
    """
    print("=== SISTEMA DE CONTROL DE STOCK ===")
    print("Inventario inicial:", stock)

    while True:
        producto = input("\nIngrese el producto (o 'salir' para terminar)(+ actualizar stock): ").lower()
        if producto == "salir":
            break
        if producto == "+":
            producto = input("\nIngrese el producto:").lower()
            nueva_cantidad2 = int(input(f"Ingrese la cantidad para '{producto}': "))
            agregar_producto(producto, nueva_cantidad2)
            continue

        if producto not in stock:
            respuesta = input(f"El producto '{producto}' no existe. ¿Desea agregarlo? (s/n): ").lower()
            if respuesta == 's':
                try:
                    nueva_cantidad = int(input(f"Ingrese la cantidad para '{producto}': "))
                    agregar_producto(producto, nueva_cantidad)
                    print("\nNuevo Inventario:", stock)
                except ValueError:
                    print("Cantidad inválida. Debe ser un número entero.")
                continue
            else:
                print("No se realizó ninguna acción.")
                continue

        try:
            cantidad = int(input("Ingrese la cantidad: "))
        except ValueError:
            print("Debe ingresar un número válido.")
            continue
        print(actualizar_stock(producto, cantidad))
    
    print("\nInventario final:", stock)

if __name__ == "__main__":
    ejecutar()
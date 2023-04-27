"""Product model."""

class Product:
    """A product in the store."""
    
    # seller: Seller

    def __init__(self, name: str, price: int, quantity: int) -> None:
        self.name: str = name
        self.price: int = price
        self.quantity: int = quantity

    def __str__(self) -> str:
        return f"Product: {self.name} - {self.price} ({self.quantity}x)"
    
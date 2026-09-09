from dataclasses import dataclass, field
from datetime import datetime


def main():
    print("Hello from cosmicpython!")


@dataclass
class Product:
    name: str
    sku: str


@dataclass
class Customer:
    name: str
    cust_id: int


@dataclass
class OrderLine:
    """Amount of a given SKU within a batch."""

    ref: int
    sku: str
    qty: int


@dataclass(frozen=True)
class Order:
    """Represents an order that a customer has requested."""

    ref: int
    order_lines: dict[int, OrderLine]


@dataclass
class Batch:
    """A batch of stock."""

    ref: int
    sku: str
    name: str
    qty: int
    eta: datetime | None = None
    allocated: set[int] = field(default_factory=set)

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self.qty -= order_line.qty
            self.allocated.add(order_line.ref)

    def deallocate(self, order_line: OrderLine):
        if order_line.ref in self.allocated:
            self.qty += order_line.qty
            self.allocated.remove(order_line.ref)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return (
            order_line.ref not in self.allocated
            and order_line.sku == self.sku
            and self.qty >= order_line.qty
        )


if __name__ == "__main__":
    main()

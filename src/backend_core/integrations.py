from decimal import Decimal


class CatalogClient:
    prices = {"coffee": Decimal("12.99"), "mug": Decimal("9.50"), "hoodie": Decimal("39.00")}

    def price_for(self, sku: str) -> Decimal:
        return self.prices.get(sku, Decimal("0.00"))


class InventoryClient:
    inventory = {"coffee": 30, "mug": 4, "hoodie": 0}

    def available(self, sku: str) -> int:
        return self.inventory.get(sku, 0)


class PaymentClient:
    def authorize(self, payment_token: str, amount: Decimal) -> str:
        return f"auth_{payment_token[-4:]}_{str(amount).replace('.', '')}"


class FulfillmentClient:
    def reserve(self, destination_zip: str) -> str:
        return f"fulfillment_{destination_zip[:5]}"


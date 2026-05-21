from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException

from backend_core.auth import Principal
from backend_core.integrations import CatalogClient, FulfillmentClient, InventoryClient, PaymentClient
from backend_core.models import CheckoutRequest, CheckoutResponse, QuoteRequest, QuoteResponse


class CommerceOrchestrator:
    def __init__(self) -> None:
        self.catalog = CatalogClient()
        self.inventory = InventoryClient()
        self.payment = PaymentClient()
        self.fulfillment = FulfillmentClient()

    def quote(self, request: QuoteRequest, principal: Principal) -> QuoteResponse:
        if principal.tenant_id != "tenant_cincinnati":
            raise HTTPException(status_code=403, detail="Tenant denied")
        subtotal = Decimal("0.00")
        warnings: list[str] = []
        for item in request.items:
            price = self.catalog.price_for(item.sku)
            if price == 0:
                warnings.append(f"{item.sku} unknown")
            if self.inventory.available(item.sku) < item.quantity:
                warnings.append(f"{item.sku} inventory unavailable")
            subtotal += price * item.quantity
        tax = (subtotal * Decimal("0.075")).quantize(Decimal("0.01"))
        shipping = Decimal("4.99")
        return QuoteResponse(
            quote_id=f"quote_{uuid4().hex[:8]}",
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            total=subtotal + tax + shipping,
            warnings=warnings,
        )

    def checkout(self, request: CheckoutRequest, principal: Principal) -> CheckoutResponse:
        quote = self.quote(request, principal)
        if quote.warnings:
            raise HTTPException(status_code=409, detail={"message": "Cannot checkout unresolved quote", "warnings": quote.warnings})
        auth_id = self.payment.authorize(request.payment_token, quote.total)
        fulfill_id = self.fulfillment.reserve(request.destination_zip)
        return CheckoutResponse(
            order_id=f"order_{uuid4().hex[:8]}",
            status="accepted",
            quote=quote,
            partner_calls=[auth_id, fulfill_id],
        )


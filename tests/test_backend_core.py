from fastapi.testclient import TestClient

from backend_core.main import app

client = TestClient(app)


def auth(token: str = "partner-app") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_quote_requires_authentication() -> None:
    response = client.post("/v1/orders/quote", json={"customer_id": "cust_1", "items": [{"sku": "coffee", "quantity": 1}], "destination_zip": "45202"})
    assert response.status_code == 401


def test_quote_orchestrates_catalog_inventory_tax_and_shipping() -> None:
    response = client.post(
        "/v1/orders/quote",
        headers=auth(),
        json={"customer_id": "cust_1", "items": [{"sku": "coffee", "quantity": 2}], "destination_zip": "45202"},
    )
    assert response.status_code == 200
    assert response.json()["total"] == "32.92"


def test_checkout_requires_write_scope() -> None:
    response = client.post(
        "/v1/orders/checkout",
        headers={**auth("analyst"), "Idempotency-Key": "k1"},
        json={"customer_id": "cust_1", "items": [{"sku": "coffee", "quantity": 1}], "destination_zip": "45202", "payment_token": "tok_123456"},
    )
    assert response.status_code == 403


def test_checkout_is_idempotent() -> None:
    payload = {"customer_id": "cust_1", "items": [{"sku": "coffee", "quantity": 1}], "destination_zip": "45202", "payment_token": "tok_123456"}
    headers = {**auth(), "Idempotency-Key": "same-key"}
    first = client.post("/v1/orders/checkout", headers=headers, json=payload)
    second = client.post("/v1/orders/checkout", headers=headers, json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["order_id"] == second.json()["order_id"]


def test_mcp_tool_invocation_uses_same_contract_boundary() -> None:
    response = client.post(
        "/mcp/invoke",
        headers=auth(),
        json={"name": "commerce.quote", "arguments": {"customer_id": "cust_1", "items": [{"sku": "mug", "quantity": 1}], "destination_zip": "45202"}},
    )
    assert response.status_code == 200
    assert response.json()["result"]["total"] == "15.20"


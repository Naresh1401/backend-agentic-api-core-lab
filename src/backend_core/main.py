from typing import Annotated, Any

from fastapi import Depends, FastAPI, Header

from backend_core.auth import Principal, require_scope
from backend_core.models import CheckoutRequest, CheckoutResponse, QuoteRequest, QuoteResponse, ToolInvocation
from backend_core.orchestrator import CommerceOrchestrator

app = FastAPI(title="Backend Agentic API Core Lab", version="0.1.0")
idempotency: dict[str, CheckoutResponse] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/orders/quote", response_model=QuoteResponse)
def quote(
    request: QuoteRequest,
    principal: Principal = Depends(require_scope("orders:read")),
) -> QuoteResponse:
    return CommerceOrchestrator().quote(request, principal)


@app.post("/v1/orders/checkout", response_model=CheckoutResponse)
def checkout(
    request: CheckoutRequest,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    principal: Principal = Depends(require_scope("orders:write")),
) -> CheckoutResponse:
    if idempotency_key in idempotency:
        return idempotency[idempotency_key]
    response = CommerceOrchestrator().checkout(request, principal)
    idempotency[idempotency_key] = response
    return response


@app.get("/mcp/tools")
def tools(_: Principal = Depends(require_scope("tools:invoke"))) -> dict[str, list[dict[str, Any]]]:
    return {
        "tools": [
            {
                "name": "commerce.quote",
                "description": "Quote commerce items. Read-only from a side-effect perspective.",
                "input_schema": QuoteRequest.model_json_schema(),
                "side_effects": "none",
            }
        ]
    }


@app.post("/mcp/invoke")
def invoke_tool(
    invocation: ToolInvocation,
    principal: Principal = Depends(require_scope("tools:invoke")),
) -> dict[str, Any]:
    quote = CommerceOrchestrator().quote(QuoteRequest.model_validate(invocation.arguments), principal)
    return {"tool": invocation.name, "result": quote.model_dump(mode="json")}


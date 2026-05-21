# Backend Agentic API Core Lab

Portfolio repo for the JD must-have skills:

- Strong backend engineering with REST APIs and integration services
- Authentication and authorization for API access
- API orchestration/composition across services
- Production-ready engineering practices
- MCP server/tool interface experience
- Agentic workflow basics and tool consumption

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn backend_core.main:app --reload --app-dir src
```

## Demo Tokens

- `Bearer platform-admin`: all scopes
- `Bearer partner-app`: `orders:read orders:write tools:invoke`
- `Bearer analyst`: `orders:read`

## Core Endpoints

- `GET /health`
- `POST /v1/orders/quote`
- `POST /v1/orders/checkout`
- `GET /mcp/tools`
- `POST /mcp/invoke`


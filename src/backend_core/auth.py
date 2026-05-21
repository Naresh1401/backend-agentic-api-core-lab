from dataclasses import dataclass
from typing import Annotated, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant_id: str
    scopes: frozenset[str]


TOKENS = {
    "platform-admin": Principal("admin", "tenant_cincinnati", frozenset({"orders:read", "orders:write", "tools:invoke"})),
    "partner-app": Principal("partner-app", "tenant_cincinnati", frozenset({"orders:read", "orders:write", "tools:invoke"})),
    "analyst": Principal("analyst", "tenant_cincinnati", frozenset({"orders:read"})),
}


def authenticate(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> Principal:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    principal = TOKENS.get(credentials.credentials)
    if principal is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token")
    return principal


def require_scope(scope: str) -> Callable[[Principal], Principal]:
    def dependency(principal: Annotated[Principal, Depends(authenticate)]) -> Principal:
        if scope not in principal.scopes:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing scope: {scope}")
        return principal

    return dependency


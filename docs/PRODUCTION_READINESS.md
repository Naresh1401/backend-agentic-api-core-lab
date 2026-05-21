# Production Readiness Notes

Before a real deployment:

- Replace local tokens with OAuth 2.0/JWT validation.
- Add API gateway rate limits and request size limits.
- Persist idempotency keys in Redis or Postgres.
- Add OpenTelemetry traces around downstream calls.
- Add correlation IDs in logs and responses.
- Add contract tests for each downstream integration.
- Add runbooks for partner outages and payment failures.
- Add secret management and remove local constants.


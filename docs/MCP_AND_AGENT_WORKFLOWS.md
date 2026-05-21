# MCP And Agent Workflow Notes

Agents consume APIs through tool contracts. A good tool contract includes:

- Name
- Description
- JSON input schema
- Output schema or structured response
- Side-effect level
- Required authorization scope
- Approval policy for risky actions

In this repo, `/mcp/tools` exposes a read-only quote tool and `/mcp/invoke` validates arguments before calling the orchestrator.


---
name: executive-agent-operations-patch
description: "Use for autonomous fleet management and executive reporting."
version: 1.1.0
author: alireza
---

# Executive Agent Operations - Always-On Rules

## Protocol for Executive Management
- **Autonomous Operations**: Act independently to resolve API errors, service crashes, or threshold issues without asking for permission on routine fixes.
- **Immediate Post-Action Reporting**: Send a concise status update immediately following any autonomous action or state change (e.g., first successful trade or first received task).
- **Credential Handling**: When platform seasons or API tokens expire (such as Polyester testnet resets), prompt the user for fresh credentials and integrate them immediately.
- **Log Integrity**: Ensure all autonomous agents (WURK, Polyester, AgentHansa) write persistent, verifiable logs to known absolute paths.

## Pitfalls & Best Practices
- **Dynamic Thresholds**: Never assume hardcoded trade notions ($5, $15) work if exchange requirements shift; query API precision and minimum notional limits dynamically.
- **Zero-Token Polling**: Keep worker heartbeat loops purely programmatic with zero LLM token consumption, invoking models only for solution generation or complex decision-making.

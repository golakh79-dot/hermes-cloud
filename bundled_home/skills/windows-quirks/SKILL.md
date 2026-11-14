---
name: windows-quirks
description: "Use to fix Windows agent crashes. Prevents encoding errors."
---

# Windows Quirks

When running autonomous agents on Windows, always follow these rules to avoid crashes and encoding errors:

### Console Output & Unicode
*   **Avoid Emojis in Print:** Windows default terminal (cp1251) crashes on non-ASCII characters like emojis.
*   **The 'Safe-Print' Rule:** Always use `.encode('ascii', 'ignore').decode('ascii')` on any string containing dynamic content (status messages, logs, quest titles) before printing to stdout.
*   **Logging:** Save the full content (with emojis) to the log file using `encoding='utf-8'`, but keep the printed console output as ASCII-only.

```python
# Safe print template
clean_msg = msg.encode('ascii', 'ignore').decode('ascii')
print(f"[{ts}] {clean_msg}")
# Full log template
with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(f"[{ts}] {msg}\n")
```

### File Handling
*   **Forward Slashes:** Always use forward slashes (`/`) for paths even on Windows. Python and shell tools on Windows handle them natively and it avoids shell-escaping errors.
*   **Encoding:** Explicitly define `encoding='utf-8'` in all `open()` calls to avoid BOM issues or local codepage misinterpretations.

### Background Processes
*   Use `master_watchdog.py` to monitor and restart agents, but ensure log file locks are released. Do not keep log files open in an interactive terminal while the agent is running in the background.

### API Credentials & Validation
*   **Token Replacement:** When updating API keys or tokens in scripts, ensure any placeholder symbols (e.g., `***`) are completely removed. Verify token connectivity using `curl` or a dedicated test script before updating code.
*   **Verification:** If a script fails with `401 Unauthorized`, verify the token endpoint explicitly (`/getMe` for Telegram) to distinguish between a dead token and an implementation bug.

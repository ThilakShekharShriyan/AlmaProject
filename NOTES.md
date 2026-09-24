# Attribution

Agent-generated, then reviewed against pytest before each push:

- `.cursor/rules/` and `.cursorrules` (installed from PatrickJS rule packs; the TypeScript pack overwrote `.cursorrules`, so the FastAPI best-practices text was copied to `.cursor/rules/cursor-python-fastapi-best-practices.mdc`)
- `apps/identity`, `apps/documents`, `apps/leads`, `apps/notifications`
- `apps/web` pages and route handlers
- `docs/DESIGN.md`, `README.md`, this file

Hand adjustment: `apps/identity/tests/test_login.py` after the first run failed. The agent opened `TestClient` without a context manager, so startup never created `users`. The fix is the `with TestClient(app)` block in that file.

`*.egg-info` was committed once by the agent and removed in the identity commit.

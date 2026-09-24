# Attribution

Agent-generated, then reviewed against pytest before each push:

- `.cursor/rules/` and `.cursorrules` (installed from PatrickJS rule packs; the TypeScript pack overwrote `.cursorrules`, so the FastAPI best-practices text was copied to `.cursor/rules/cursor-python-fastapi-best-practices.mdc`)
- `apps/identity`, `apps/documents`, `apps/leads`, `apps/notifications`
- `apps/web` pages and route handlers
- `docs/DESIGN.md`, `README.md`, this file

Hand adjustment: `apps/identity/tests/test_login.py` after the first run failed. The agent opened `TestClient` without a context manager, so startup never created `users`. The fix is the `with TestClient(app)` block in that file.

`*.egg-info` was committed once by the agent and removed in the identity commit.

Hand adjustment: `apps/web/app/apply/page.tsx`. After a successful submit, `event.currentTarget` is null, so `reset()` threw. The handler now keeps the form element from before the request.

The FastAPI services and Redis queue were removed. The running app is `apps/web` only: Supabase for auth, leads, and resumes, Resend for mail.
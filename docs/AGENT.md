# Coding agent usage

The running app is `apps/web` only. Supabase and Resend are the data and mail services. The FastAPI processes were an earlier layout and have been removed.

Tools: Cursor agent (Grok) with the shell, file edits, and the IDE browser. Project rules came from `npx mdskills install` for PatrickJS FastAPI and Next.js rules. Supabase and Vercel MCP were added later for the hosted database and the deployment.

Delegated: service layout, FastAPI routes, SQLAlchemy models, Alembic revisions, pytest, and the Next.js pages. I reviewed each slice by running pytest before the push. The browser walkthrough of the form, login, list, download, and status change has not been done yet.

One bad result: the login tests constructed `TestClient(app)` and immediately posted. The users table was missing (`relation "users" does not exist`) because that client does not run the FastAPI lifespan, so `create_all` and the attorney seed never ran. Health tests still passed because they mock the database check. I changed the login tests to `with TestClient(app) as client`, which enters the lifespan, and both login cases passed.

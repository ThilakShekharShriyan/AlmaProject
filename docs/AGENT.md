# Coding agent usage

Cursor was the harness for this project: file edits, the shell, and the browser. Supabase’s MCP server was in the loop for the schema and attorney auth. Vercel’s MCP server and CLI created the project, set env, attached the domain, and connected GitHub. GitHub Actions typechecks and builds `apps/web` on every push and pull request. A push to `main` deploys. Agents drafted the code. I decided what was allowed to ship.

I delegated the first draft of each slice, from the lead row and resume upload through the React screen that uses it. That is the fast path. I kept the product calls. There are two customers. The prospect gets a public form and a confirmation. The attorney gets a private list, the resume, and Reach out. I had an early FastAPI split removed once Supabase owned auth, Postgres, and files, and Resend owned the two emails. The state rule stayed in the database: `PENDING` → `REACHED_OUT` once, anything else 409. I also rejected UI that treated the attorney like a public nav item. Log out shows only on the lead pages, `/admin` is typed in, and a signed-in attorney cannot submit an application.

One bad result survived a green save. After a successful submit, the page threw `Cannot read properties of null (reading 'reset')`. The agent called `event.currentTarget.reset()` after `await fetch`. React clears `currentTarget` on the first await, so the lead was stored and the success path still crashed. I caught it by submitting the form the way a prospect would and reading the stack. `apps/web/app/apply/apply-form.tsx` now keeps the form element before the request and resets that reference. Agent speed still needs a pass over the path the user actually finishes.

Excerpts: [docs/PROMPTS.md](PROMPTS.md). Attribution: [NOTES.md](../NOTES.md).

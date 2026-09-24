# Prompt excerpts

Instructions from the session. The agent implemented them. I kept the ones that show the architecture call, the auth boundary, and the bug.

**Schema through the screen**

> Build the lead intake end to end. Public `POST` accepts `first_name`, `last_name`, `email`, and a resume. Persist the row and the file, then send one email to the prospect and one to the attorney. The attorney UI is authenticated and lists every field the prospect submitted. Status is `PENDING` on insert and may move only to `REACHED_OUT`. Document the design and how to run it.

**Collapse the process boundary**

> Remove the FastAPI services, local Postgres, Redis, and Mailpit. Supabase is the system of record for Auth, the lead and document rows, and the private `resumes` bucket. Resend sends both messages. Keep the status transition in Postgres, not in the client.

**Failure after a successful write**

> `POST /api/apply` returns 200 and the lead is stored, then the client throws `Cannot read properties of null (reading 'reset')` at `event.currentTarget.reset()` in `onSubmit`. `currentTarget` is null after the `await`. Capture the form element before the request and reset that reference.

**Session boundary**

> Do not render Admin or Log out in the public header. `/admin` is a typed URL. Show Log out only on `/leads` when the `access_token` cookie is present. If that cookie is set, `/` and `/apply` must not accept another application: offer log out, or cancel back to the lead list. `POST /api/apply` returns 403 in that case.

**Production loop**

> The Vercel MCP server is authenticated. Attach the custom domain, set the production env, and connect the GitHub repo so `main` deploys. Add a free GitHub Actions workflow that runs `npm ci`, `tsc --noEmit`, and `next build` in `apps/web` on every push and pull request.

**Managed services versus our own platform**

> Document the current design: Supabase Auth, Postgres, and Storage, with Resend for product email. Explain the request path, the RLS boundary, and where it scales. Then contrast AWS EKS with in-house OIDC: the app on the cluster, RDS, S3, and a queue in front of SES. Same product rules, different ownership.

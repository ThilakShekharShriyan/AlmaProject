# Design

## Callers

- Prospect: public form. No account.
- Attorney: one seeded user. Internal list and status change require a JWT.

## State

- A lead is created as `PENDING`.
- An attorney may set it to `REACHED_OUT`.
- Any other transition, including a repeat of `REACHED_OUT`, is rejected with 409.
- Prospect fields are not edited after create.

## Services

- `apps/web` — Next.js. The browser talks only to this app.
- `apps/identity` — attorney password hash and JWT issue. Database `identity_db`.
- `apps/documents` — resume bytes on disk, path in `documents_db`. PDF, DOC, DOCX, 10 MB.
- `apps/leads` — lead rows in `leads_db`. Publishes `LeadSubmitted` on Redis.
- `apps/notifications` — stateless worker. Sends two emails. Does not change lead state.

Services do not share tables. Sync calls are HTTP. Email is the only async hop.

## Routes

- Public: document upload, lead create.
- Auth: login, lead list, lead get, resume download, status patch.
- Leads checks the JWT locally with a shared HMAC secret.

## Ports

- File port: write and read bytes under `uploads/`. The database stores the path.
- Email port: `EmailSender` over SMTP. Local target is Mailpit.

## If email fails

The lead stays saved. The worker logs the error.

## Layout

```
apps/web
apps/identity
apps/documents
apps/leads
apps/notifications
docker-compose.yml
docs/DESIGN.md
docs/AGENT.md
NOTES.md
.env.example
README.md
```

## Why

- Five processes keep file bytes, passwords, lead state, and SMTP out of one process. A mail failure cannot roll back a saved lead.
- Postgres is one local server with three databases so the services do not share tables. Redis carries only `LeadSubmitted`.
- The resume stays on disk. The documents database stores the path.
- `EmailSender` is the mail port. Local SMTP is Mailpit, so the inbox is visible without an API key.
- The browser talks only to Next.js. Service URLs stay on the server. The attorney JWT is an httpOnly cookie.
- Leads checks the JWT itself with the shared secret, so listing leads does not call identity.
- Status moves only from `PENDING` to `REACHED_OUT`. A repeat is 409.

## Boundaries

Compose runs Postgres, Redis, and Mailpit. The API and web processes stay on the host. No Kubernetes, AWS, OAuth, or resume bytes in Postgres.

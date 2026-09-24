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
docs/DESIGN.md
docs/AGENT.md
NOTES.md
.env.example
README.md
```

## Out of this pass

No Docker, Compose, Kubernetes, AWS, OAuth, or resume bytes in Postgres. Docker Compose is a later follow-up.

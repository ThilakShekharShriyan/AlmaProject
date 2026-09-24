# Design

## Callers

- Prospect: public form. No account.
- Attorney: a Supabase Auth user. The lead list and status change require that user's access token.

## State

- A lead is created as `PENDING`.
- An attorney may set it to `REACHED_OUT`.
- Any other transition, including a repeat of `REACHED_OUT`, is rejected with 409.
- Prospect fields are not edited after create.

## App

`apps/web` is the only process. The browser talks only to Next.js. Server code calls Supabase for auth, lead rows, document metadata, and the private `resumes` bucket, and calls Resend for the two emails.

## Routes

- Public: apply form, which uploads the resume, inserts the lead, and sends mail.
- Auth: login, lead list, lead get, resume download, status patch.
- Row access is enforced by Supabase RLS. The access token is an httpOnly cookie.

## If email fails

The lead stays saved. The server logs the send error.

## Why

- One Next.js app is enough because Supabase already separates auth, rows, and file bytes.
- Resend sends both messages. A mail failure does not roll back the lead.
- Status moves only from `PENDING` to `REACHED_OUT`. A repeat is 409.

# Lead intake

Public application form for prospects, and a private lead list for an attorney.

A prospect submits a name, email, and resume. The app stores the lead, uploads the resume, and emails the prospect and the attorney. The attorney signs in, downloads the resume, and marks the lead as reached out. A lead starts as `PENDING` and can move to `REACHED_OUT` once. A second change is rejected.

Live site: [https://leads.thilakshekharshriyan.com](https://leads.thilakshekharshriyan.com)

## Stack

| Piece | Role |
| --- | --- |
| Next.js (`apps/web`) | Pages and API routes |
| Supabase Auth | Attorney sign-in |
| Supabase Postgres | Leads and resume metadata |
| Supabase Storage | Resume files in the `resumes` bucket |
| Resend | Email to the prospect and the attorney |
| Vercel | Hosts the site. Pushes to `main` deploy. |

GitHub Actions typechecks and builds `apps/web` on every push to `main` and on every pull request.

## Pages

| Path | Who |
| --- | --- |
| `/` | Public landing page |
| `/apply` | Public form: first name, last name, email, resume |
| `/admin` | Attorney sign-in. This is not in the header. `/login` redirects here. |
| `/leads` | Attorney lead list. Requires sign-in. |
| `/leads/[id]` | One lead, resume download, and Reach out |

The header shows **Log out** only on the lead pages. A signed-in attorney who opens `/` or `/apply` is asked to log out or go back. The public form also refuses a submission while that session cookie is set.

Resume files must be PDF, DOC, or DOCX, and 10 MB or smaller.

If email fails, the lead stays saved and the server logs the send error.

## What you need

- Node.js 20+
- A Supabase project
- A Resend API key and a verified sending domain

## Configure

```bash
cp .env.example .env
```

`.env` stays on your machine. It is gitignored.

| Variable | Value |
| --- | --- |
| `SUPABASE_URL` | Project URL, such as `https://your-project.supabase.co` |
| `SUPABASE_ANON_KEY` | The anon or publishable key |
| `RESEND_API_KEY` | Resend API key |
| `EMAIL_FROM` | From address on a domain verified in Resend. Quote it if the name contains a space: `"Alma <leads@your-verified-domain.com>"` |
| `ATTORNEY_NOTIFICATION_EMAIL` | Address that receives the attorney copy |

The app reads this file from the repo root when the variables are not already in the environment. Vercel injects the same names in production.

### Supabase

Create these before the form will save:

- A private Storage bucket named `resumes`.
- Table `documents` with `id`, `filename`, `content_type`, and `storage_path`.
- Table `leads` with `id`, `first_name`, `last_name`, `email`, `document_id`, `status`, `created_at`, and `updated_at`.
- Status values `PENDING` and `REACHED_OUT`. A database check allows only `PENDING` → `REACHED_OUT`.
- Row level security: anonymous insert of a `PENDING` lead and its document; authenticated select and update.
- An Authentication user for the attorney, with the email confirmed. The sign-in form sends that email and password to Supabase. There is no local users table.

## Run

```bash
cd apps/web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

Check the types with `npx tsc --noEmit` from `apps/web`.

## Demo

1. Open `/apply` and submit a name, email, and PDF resume.
2. Confirm the prospect email and the attorney email.
3. Open `/admin` and sign in with the Supabase attorney user.
4. Open the lead, download the resume, and click **Reach out**. The status becomes `REACHED_OUT`.
5. Click **Reach out** again. The app rejects it.

Design notes are in [docs/DESIGN.md](docs/DESIGN.md). Agent usage is in [docs/AGENT.md](docs/AGENT.md), with excerpts in [docs/PROMPTS.md](docs/PROMPTS.md) and attribution in [NOTES.md](NOTES.md).

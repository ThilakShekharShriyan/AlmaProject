# Lead intake

Public prospect form and attorney review. Next.js on the host. Supabase holds auth, leads, and resumes. Resend sends the emails.

## What you need

- Node.js 20+
- A Supabase project and a Resend API key

## Configure

```bash
cp .env.example .env
```

Fill in `.env`:

- `SUPABASE_URL` and `SUPABASE_ANON_KEY`
- `RESEND_API_KEY`, and `EMAIL_FROM` as an address on a domain verified in Resend
- `ATTORNEY_NOTIFICATION_EMAIL` for the attorney copy

Create the attorney in Supabase Authentication and confirm the email. The login form sends that email and password to Supabase.

## Run

```bash
cd apps/web
npm install
npm run dev
```

Open http://localhost:3000/apply

The same app is deployed at https://leads.thilakshekharshriyan.com

## Demo path

1. Submit the public form with a PDF resume.
2. Confirm mail to the prospect and the attorney.
3. Sign in at `/login` with the Supabase attorney user.
4. Open the lead, download the resume, and click Reach out. Status becomes `REACHED_OUT`.

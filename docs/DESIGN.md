# Design

## What this is

A prospect submits a name, email, and resume. An attorney later signs in, reads that lead, downloads the resume, and marks it reached out. The lead is created as `PENDING`. The only allowed change is `PENDING` → `REACHED_OUT`. A repeat is rejected with 409. Prospect fields are not edited after create.

The browser talks only to one Next.js app, `apps/web`. That app calls Supabase for auth, rows, and files, and Resend for the two emails. Vercel hosts the app. GitHub Actions typechecks and builds on every push and pull request. A push to `main` deploys.

## How a submission works

1. `POST /api/apply` refuses the request when the attorney session cookie is present, so a signed-in attorney cannot file an application.
2. The resume must be a PDF, DOC, or DOCX under 10 MB. The app uploads the bytes to the private Storage bucket `resumes` and inserts a `documents` row (id, filename, content type, storage path).
3. It inserts a `leads` row as `PENDING`, with the prospect fields and the document id. The app generates the ids. Inserts use `return=minimal` because the anonymous role cannot read the row back.
4. The same request sends two Resend emails: one to the prospect, one to `ATTORNEY_NOTIFICATION_EMAIL`. If either send fails, the lead stays saved and the error is logged. Mail does not roll back the row.

## How attorney access works

Sign-in is `POST /api/login`. Next.js sends the email and password to Supabase Auth (`grant_type=password`) and stores the access token in an httpOnly cookie. There is no local users table.

`/leads` is behind middleware. A missing cookie redirects to `/admin`. List, detail, resume download, and status change send that token to Supabase, so Postgres row level security is what allows the read and the update. Anonymous callers may insert a `PENDING` lead and its document. Authenticated callers may select and update.

A database check allows only `PENDING` → `REACHED_OUT`. Any other update, including a second Reach out, comes back as SQLSTATE `23514`, and the API returns 409.

Log out clears the cookie. The header shows that action only on the lead pages. The public pages ask a signed-in attorney to log out or go back.

## Why this shape

Supabase already separates the three things this product stores: who the attorney is, the lead rows, and the resume bytes. One Next.js process is enough to orchestrate them. Splitting auth, documents, and leads into separate services would add network hops and deploy units without a second team to own them.

Resend is the mail path, not Supabase. Supabase Auth confirms the attorney account. It does not send the prospect confirmation or the attorney notification. Those are product emails, so they go through a verified sending domain on Resend.

The status rule lives in the database, not only in the button. A client that calls the API twice still cannot move a lead twice.

Email is synchronous and best-effort. The assignment’s important record is the lead. A mail outage must not lose it.

## How this scales

The app process is stateless. Vercel can run more copies as traffic grows. Lead rows and resume metadata sit in Postgres. File bytes sit in Storage, so the Next.js process does not keep uploads on disk.

This workload scales well for a public form and a small number of attorneys. Writes are one lead per submission. Reads are an attorney opening a short list. The CDN serves the pages. The database is the source of truth and is not on the request path for static assets.

The limits show up before the cluster would:

- Both emails run inside the submit request. A slow mail API makes that request slow. A large spike of submissions shares Resend’s rate limit. A queue and a worker would take mail off the request.
- Each serverless invocation opens its own call to Supabase. Very high concurrency is bounded by Supabase’s pool and plan, not by adding pods.
- The anonymous key is public. Safety depends on row level security staying correct. A bug in a policy is a data bug.
- There is one region and one project. This is not an active-active multi-region setup.
- Resume size is capped at 10 MB in the app. Larger files would need a direct-to-storage upload.

For the traffic this product actually has, those limits are acceptable. The design spends capacity on the database and the mail provider, which are the parts that hold state.

## Advantages

- No servers to patch. Auth, Postgres, file storage, and the web app are managed.
- One deploy updates the whole product. Vercel builds `main`. The database and files stay where they are.
- Authorization is in Postgres. The lead list cannot be read with the anonymous key, even if someone calls the REST API directly.
- The status rule is enforced under the API, so the UI is not the only guard.
- A mail failure does not delete the lead.
- The attorney session is an httpOnly cookie. Page JavaScript does not read the token.

## Disadvantages

- The product depends on Supabase and Resend. Moving the rows, files, or auth users later is a migration, not a config change.
- Identity is a Supabase email and password. It is not the company’s employee directory. An attorney who leaves is removed in the Supabase dashboard, not by turning off their SSO account.
- The anonymous key ships to the browser’s network calls from the server, and the policies are the security boundary. They have to be reviewed with the schema.
- Mail is inline. There is no retry queue. A failed send is a log line.
- Observability is vendor logs plus `console.error`. There is no separate error tracker.
- Local development needs a real Supabase project and a real Resend key. There is no local database in this repo.

## If this ran on our own infrastructure

With AWS EKS and in-house OAuth, the product behavior would stay the same and the ownership would change.

The Next.js app would run as a deployment on the cluster, behind the company ingress and load balancer. We would own the image, the replicas, the rollout, and the secrets. GitHub would build the image and the cluster would roll it out, instead of Vercel deploying the Git push.

Sign-in would be the company identity provider. The attorney would authenticate with OIDC (or the company’s SSO) and the app would validate that token. Supabase’s password grant and the Auth user list would go away. Authorization might still be a row check, but it would key off the company subject or group, not the Supabase `authenticated` role. Turning off the employee in the directory would turn off access here.

Leads would live in a database we operate, such as RDS. Resumes would live in S3. The bucket policy and the app’s IAM role would replace the Supabase storage policies. Email would go through SES or another company mail gateway, with the same rule: save the lead first, then send, and do not roll back on a send failure. At that point a queue on SQS and a worker on the cluster would be the natural way to retry mail, because we would already be running the worker.

We would also own backups, network policy, TLS at the edge, database migrations, and on-call for the cluster. That is the right trade when the company already runs EKS and every internal tool must use the same SSO. It is extra machinery for a single public form. This repo uses the managed services so the lead path, the status rule, and the two emails can ship without that platform.

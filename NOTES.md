# Attribution

Agent-generated, then checked in the browser and with `tsc` before the later pushes.

The public form, attorney sign-in, lead list, and reach-out action live in `apps/web`. Supabase stores the rows and resumes. Resend sends mail.

Hand adjustment: `apps/web/app/apply/apply-form.tsx`. After a successful submit, `event.currentTarget` is null, so `reset()` threw. The handler keeps the form element from before the request.

The FastAPI services and Redis queue were removed. The running app is `apps/web` only.

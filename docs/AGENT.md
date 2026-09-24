# Coding agent usage

I used Cursor for this repo. The agent edited files, ran the shell, and checked pages in the browser. Supabase and Vercel were connected as well, so the agent could apply the database, create the project, attach the domain, and connect GitHub. GitHub Actions typechecks and builds `apps/web` on each push and pull request. A push to `main` deploys on Vercel.

I delegated the implementation: the Next.js pages and API routes, the Supabase calls, the Resend emails, the workflow, the README, and the design document. I kept the decisions. After an earlier FastAPI layout, I had the agent remove those services and use Supabase for auth, rows, and resumes, and Resend for the two emails. I created the attorney user, verified the sending domain, and reviewed the live site. I rejected a header that always showed Admin and Log out, a footer sentence, and the Alma name in the brand.

One bad result: a successful apply crashed with `Cannot read properties of null (reading 'reset')` in the apply handler. The agent called `event.currentTarget.reset()` after `await fetch`. React clears `currentTarget` after the first await, so the lead was saved and the page then threw. I caught it by submitting the form and reading that stack. `apps/web/app/apply/apply-form.tsx` now keeps the form element in `formElement` before the request and calls `formElement.reset()` after success.

Prompt excerpts are in [docs/PROMPTS.md](PROMPTS.md). File attribution is in [NOTES.md](../NOTES.md).

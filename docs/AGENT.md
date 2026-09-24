# Coding agent usage

Cursor was the harness: file edits, search, the shell, and the in-IDE browser. Three MCP servers were in that loop. Supabase applied the schema and confirmed the attorney user. Vercel created the project, set production env, attached `leads.thilakshekharshriyan.com`, and connected the GitHub repo. The browser MCP checked the public form, the signed-in gate, and the lead list. Skills and rules in the repo were the Karpathy guidelines, the Next.js and TypeScript rules, and daisyUI for the cream theme. The Vercel CLI and GitHub Actions finished the loop: `npm ci`, `tsc --noEmit`, and `next build` on every push, then a production deploy of `main`.

I delegated the first draft of each slice, from the lead row and resume upload through the React screen. That pass is what the agent is for. I kept the decisions. Supabase owns auth, Postgres, and the `resumes` bucket. Resend owns the two emails. The earlier FastAPI split came out because this state machine did not need four processes. The prospect form stays public. The attorney list stays behind the `access_token` cookie. Log out renders only on `/leads`. A signed-in attorney cannot submit.

One bad result got past a stored lead. `onSubmit` called `event.currentTarget.reset()` after `await fetch`. React clears `currentTarget` on the first await, so the page threw `Cannot read properties of null (reading 'reset')` after a 200. I caught it by submitting the form and reading the stack. `apps/web/app/apply/apply-form.tsx` now keeps the form element before the request and resets that reference.

Excerpts: [docs/PROMPTS.md](PROMPTS.md). Attribution: [NOTES.md](../NOTES.md).

# Attribution

Agent-generated, then reviewed before push: `apps/web`, `.github/workflows/ci.yml`, `README.md`, `docs/DESIGN.md`, and `docs/diagrams/`. Commits landed when I asked the agent to commit or push. `.env` never did.

I did not hand-type those modules. I set the constraints and sent back output that failed them.

| What | Who |
| --- | --- |
| Pages, API routes, Supabase client, Resend mail, CI, design diagrams | Agent draft, accepted after `tsc` and a browser pass |
| Drop the FastAPI services and ship one Next.js app on Supabase and Resend | My call. The state machine did not need four processes |
| Public form vs attorney tools: no Admin link, Log out only when signed in, no apply while the attorney cookie is set | My review. The agent had mixed the two customers in the header |
| `apps/web/app/apply/apply-form.tsx` reset | I reproduced `currentTarget` null after a successful submit. The agent kept the form element from before `await` |

No application file is hand-written. The review is the part I did not delegate.

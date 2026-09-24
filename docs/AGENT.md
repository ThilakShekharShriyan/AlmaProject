# Coding agent usage

The running app is `apps/web`. Supabase holds auth, leads, and resumes. Resend sends the two emails. Vercel deploys `main`.

Tools: Cursor agent with the shell, file edits, and the IDE browser. Supabase and Vercel were used for the hosted database and the deployment.

The earlier FastAPI services, local Postgres, Redis, and Mailpit were removed after the app moved to Supabase and Resend.

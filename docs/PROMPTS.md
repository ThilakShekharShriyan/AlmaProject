# Prompt excerpts

The agent implemented these. I kept the ones that show the decision, the review, and the bug.

**End to end, both customers**

> A lead is a form PUBLICLY available for prospects… first name, last name, email, resume / CV. Once submitted, send emails to both the prospect and an attorney. An internal UI guarded by auth lists the leads. State starts PENDING and transitions to REACHED_OUT when an attorney marks it. Design the system, build the web app and APIs, persistent storage, and document how to run it.

**Cut scope instead of keeping a diagram**

> lets get rid of all the unnecessary stuff

The FastAPI services, local Postgres, Redis, and Mailpit came out. Supabase holds auth, rows, and resumes. Resend sends mail.

**Caught on the success path**

> Cannot read properties of null (reading 'reset')
>
> app/apply/page.tsx (24:25) @ onSubmit
>
> event.currentTarget.reset();

The lead had already saved. The crash was the form clear after `await`.

**Attorney workflow is not public chrome**

> the logout on top header should only be if we are signed in and admin also option shouldn't be, if you want to go to admin you should manually type in url

> if you are logged in and you are trying to go outside it, you will need to log out, like going to apply, so u cant apply as admin

**Ship with the tools in the loop**

> I have authenticated vercel and there is mcp server as well can you try now with custom domain name

> Can we enable CI CD for free github and create a loop… with vercel

**Say what would change on our own platform**

> I currently used supabase for auth, storage and email… if we had our own infrastructure, AWS EKS and in house Oauth SSO, authentication it would be different. Explain how my current design is and how it works, and will scale, advantage and disadvantage of this method.

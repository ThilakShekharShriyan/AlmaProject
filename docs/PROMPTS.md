# Prompt excerpts

Short excerpts from the Cursor session. The agent implemented each one.

**Scope**

> Develop an application to support creating, getting and updating leads. A lead is a form PUBLICLY available for prospects… first name, last name, email, resume / CV… emails to both the prospect and an attorney… PENDING… REACHED_OUT… FastAPI APIs and a simple front-end in Next.js… persistent storage… how to run the project… design document… coding-agent usage.

**After the first services were too heavy**

> lets get rid of all the unnecessary stuff

The running app became one Next.js app on Supabase and Resend.

**A bug I hit in the browser**

> Cannot read properties of null (reading 'reset')
>
> app/apply/page.tsx (24:25) @ onSubmit
>
> event.currentTarget.reset();

**Header review**

> the logout on top header should only be if we are signed in and admin also option shouldn't be, if you want to go to admin you should manually type in url

**Deploy**

> using next js and vercel we can deploy it
>
> I have authenticated vercel and there is mcp server as well can you try now with custom domain name

**Agent usage, this writeup**

> Submit a Document your coding-agent usage… which tools you used, what you delegated vs. wrote yourself and why, and one place the agent produced wrong or subtly bad code… Representative prompt logs… Attribution in your commits or a NOTES file.

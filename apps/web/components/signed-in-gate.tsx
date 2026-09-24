import Link from "next/link";
import { CancelButton } from "./cancel-button";

export function SignedInGate() {
  return (
    <section className="mx-auto w-full min-w-0 max-w-lg rounded-box bg-base-100 p-6 sm:p-8">
      <h1 className="text-balance text-3xl font-semibold">Log out to continue</h1>
      <p className="mt-3 text-base-content/70">
        You are signed in as an attorney. Log out before opening the public site or submitting an application.
      </p>
      <div className="mt-6 flex w-full flex-col gap-3 sm:flex-row">
        <Link href="/logout" className="btn btn-primary w-full sm:w-auto">
          Log out
        </Link>
        <CancelButton />
      </div>
    </section>
  );
}

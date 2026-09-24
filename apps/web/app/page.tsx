import Link from "next/link";
import { cookies } from "next/headers";
import { SignedInGate } from "../components/signed-in-gate";

export default async function Home() {
  if ((await cookies()).get("access_token")?.value) {
    return <SignedInGate />;
  }

  return (
    <section className="hero w-full min-w-0 rounded-box bg-base-100">
      <div className="hero-content w-full max-w-full flex-col items-start gap-6 px-4 py-10 sm:px-8 sm:py-16">
        <div className="w-full min-w-0 max-w-xl">
          <h1 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">Tell us about your case</h1>
          <p className="mt-3 text-base-content/70">
            Share your name, email, and resume. An attorney receives your application and follows up.
          </p>
        </div>
        <Link href="/apply" className="btn btn-primary w-full sm:w-auto">
          Start application
        </Link>
      </div>
    </section>
  );
}

import Link from "next/link";

export default function Home() {
  return (
    <section className="hero rounded-box bg-base-100">
      <div className="hero-content flex-col items-start gap-6 py-12 sm:py-16">
        <div className="max-w-xl">
          <h1 className="text-4xl font-semibold tracking-tight">Tell us about your case</h1>
          <p className="mt-3 text-base-content/70">
            Share your name, email, and resume. An attorney receives your application and follows up.
          </p>
        </div>
        <Link href="/apply" className="btn btn-primary">
          Start application
        </Link>
      </div>
    </section>
  );
}

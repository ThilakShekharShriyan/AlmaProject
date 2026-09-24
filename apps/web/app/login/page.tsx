"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setPending(true);
    setError(null);
    const form = new FormData(event.currentTarget);
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        email: form.get("email"),
        password: form.get("password"),
      }),
    });
    setPending(false);
    if (!response.ok) {
      setError("Invalid email or password.");
      return;
    }
    router.push("/leads");
    router.refresh();
  }

  return (
    <div className="mx-auto max-w-md">
      <h1 className="text-3xl font-semibold">Attorney sign in</h1>
      <p className="mt-2 text-base-content/70">Sign in to see applications and mark the ones you have contacted.</p>
      <form onSubmit={onSubmit} className="card mt-6 bg-base-100 shadow-sm">
        <div className="card-body gap-4">
          <fieldset className="fieldset">
            <label className="label" htmlFor="email">
              Email
            </label>
            <input id="email" name="email" type="email" className="input w-full" autoComplete="username" required />
          </fieldset>
          <fieldset className="fieldset">
            <label className="label" htmlFor="password">
              Password
            </label>
            <input id="password" name="password" type="password" className="input w-full" autoComplete="current-password" required />
          </fieldset>
          {error ? (
            <div role="alert" className="alert alert-error">
              {error}
            </div>
          ) : null}
          <button type="submit" className="btn btn-primary" disabled={pending}>
            {pending ? <span className="loading loading-spinner" /> : null}
            {pending ? "Signing in" : "Sign in"}
          </button>
        </div>
      </form>
    </div>
  );
}

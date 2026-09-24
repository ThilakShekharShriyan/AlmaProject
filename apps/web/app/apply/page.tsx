"use client";

import { FormEvent, useState } from "react";

export default function ApplyPage() {
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formElement = event.currentTarget;
    setPending(true);
    setError(null);
    setMessage(null);
    const form = new FormData(formElement);
    const response = await fetch("/api/apply", { method: "POST", body: form });
    const body = await response.json().catch(() => ({}));
    setPending(false);
    if (!response.ok) {
      setError(typeof body.detail === "string" ? body.detail : "Could not submit the application.");
      return;
    }
    setMessage("Application received. Check your email for a confirmation.");
    formElement.reset();
  }

  return (
    <main>
      <h1>Apply</h1>
      <form onSubmit={onSubmit}>
        <label>
          First name
          <input name="first_name" required />
        </label>
        <label>
          Last name
          <input name="last_name" required />
        </label>
        <label>
          Email
          <input name="email" type="email" required />
        </label>
        <label>
          Resume
          <input name="resume" type="file" accept=".pdf,.doc,.docx" required />
        </label>
        <button type="submit" disabled={pending}>
          {pending ? "Submitting..." : "Submit"}
        </button>
      </form>
      {message ? <p>{message}</p> : null}
      {error ? <p>{error}</p> : null}
    </main>
  );
}

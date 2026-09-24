"use client";

import { SubmitEvent, useState } from "react";

export function ApplyForm() {
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function onSubmit(event: SubmitEvent<HTMLFormElement>) {
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
    const email = String(form.get("email") ?? "");
    setMessage(`Application received. A confirmation was sent to ${email}.`);
    formElement.reset();
  }

  return (
    <div className="mx-auto w-full min-w-0 max-w-lg">
      <h1 className="text-3xl font-semibold">Apply</h1>
      <p className="mt-2 text-base-content/70">
        All four fields are required. The resume must be a PDF, DOC, or DOCX under 10 MB.
      </p>
      <form onSubmit={onSubmit} className="card mt-6 w-full min-w-0 bg-base-100 shadow-sm">
        <div className="card-body min-w-0 gap-4">
          <fieldset className="fieldset">
            <label className="label" htmlFor="first_name">
              First name
            </label>
            <input id="first_name" name="first_name" className="input w-full" autoComplete="given-name" required />
          </fieldset>
          <fieldset className="fieldset">
            <label className="label" htmlFor="last_name">
              Last name
            </label>
            <input id="last_name" name="last_name" className="input w-full" autoComplete="family-name" required />
          </fieldset>
          <fieldset className="fieldset">
            <label className="label" htmlFor="email">
              Email
            </label>
            <input id="email" name="email" type="email" className="input w-full" autoComplete="email" required />
            <p className="label">We send the confirmation to this address.</p>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label" htmlFor="resume">
              Resume
            </label>
            <input id="resume" name="resume" type="file" accept=".pdf,.doc,.docx,application/pdf" className="file-input w-full max-w-full" required />
          </fieldset>
          {message ? (
            <div role="alert" className="alert alert-success break-words">
              {message}
            </div>
          ) : null}
          {error ? (
            <div role="alert" className="alert alert-error">
              {error}
            </div>
          ) : null}
          <button type="submit" className="btn btn-primary w-full" disabled={pending}>
            {pending ? <span className="loading loading-spinner" /> : null}
            {pending ? "Submitting" : "Submit application"}
          </button>
        </div>
      </form>
    </div>
  );
}

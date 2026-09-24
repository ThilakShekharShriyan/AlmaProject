"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function ReachOutButton({ leadId, status }: { leadId: string; status: string }) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);
  if (status !== "PENDING") {
    return null;
  }

  async function markReachedOut() {
    setError(null);
    setPending(true);
    const response = await fetch(`/api/leads/${leadId}`, {
      method: "PATCH",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ status: "REACHED_OUT" }),
    });
    setPending(false);
    if (!response.ok) {
      setError("Could not update the lead.");
      return;
    }
    router.refresh();
  }

  return (
    <div className="flex w-full min-w-0 flex-col gap-2">
      <button type="button" className="btn btn-primary w-full sm:w-auto" onClick={markReachedOut} disabled={pending}>
        {pending ? <span className="loading loading-spinner" /> : null}
        {pending ? "Saving" : "Mark as reached out"}
      </button>
      {error ? (
        <div role="alert" className="alert alert-error break-words">
          {error}
        </div>
      ) : null}
    </div>
  );
}

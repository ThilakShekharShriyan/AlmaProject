"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function ReachOutButton({ leadId, status }: { leadId: string; status: string }) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  if (status !== "PENDING") {
    return null;
  }

  async function markReachedOut() {
    setError(null);
    const response = await fetch(`/api/leads/${leadId}`, {
      method: "PATCH",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ status: "REACHED_OUT" }),
    });
    if (!response.ok) {
      setError("Could not update the lead.");
      return;
    }
    router.refresh();
  }

  return (
    <div>
      <button type="button" onClick={markReachedOut}>
        Reach out
      </button>
      {error ? <p>{error}</p> : null}
    </div>
  );
}

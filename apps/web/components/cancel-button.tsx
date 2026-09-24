"use client";

import { useRouter } from "next/navigation";

export function CancelButton() {
  const router = useRouter();

  function goBack() {
    if (window.history.length > 1) {
      router.back();
      return;
    }
    router.push("/leads");
  }

  return (
    <button type="button" className="btn w-full sm:w-auto" onClick={goBack}>
      Cancel
    </button>
  );
}

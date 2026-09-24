"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function AttorneyLogout() {
  const path = usePathname();
  if (!path.startsWith("/leads")) return null;

  return (
    <nav className="navbar-end min-w-0">
      <Link href="/logout" className="btn btn-ghost">
        Log out
      </Link>
    </nav>
  );
}

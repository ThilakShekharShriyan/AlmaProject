import Link from "next/link";
import { cookies } from "next/headers";

export async function SiteFrame({ children }: { children: React.ReactNode }) {
  const signedIn = Boolean((await cookies()).get("access_token")?.value);

  return (
    <div className="flex min-h-screen min-w-0 flex-col bg-base-200">
      <header className="navbar min-h-16 w-full min-w-0 flex-wrap bg-base-100 px-2 shadow-sm sm:px-4">
        <div className="navbar-start min-w-0">
          <Link href="/" className="btn btn-ghost text-lg">
            Lead intake
          </Link>
        </div>
        {signedIn ? (
          <nav className="navbar-end min-w-0">
            <Link href="/logout" className="btn btn-ghost">
              Log out
            </Link>
          </nav>
        ) : null}
      </header>
      <main className="mx-auto w-full min-w-0 max-w-5xl flex-1 px-4 py-8 sm:px-6">{children}</main>
    </div>
  );
}

export function StatusBadge({ status }: { status: string }) {
  const reached = status === "REACHED_OUT";
  return (
    <span className={reached ? "badge badge-success" : "badge badge-warning"}>
      {reached ? "Reached out" : "Pending"}
    </span>
  );
}

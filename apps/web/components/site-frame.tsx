import Link from "next/link";
import { cookies } from "next/headers";

export async function SiteFrame({ children }: { children: React.ReactNode }) {
  const signedIn = Boolean((await cookies()).get("access_token")?.value);

  return (
    <div className="flex min-h-screen flex-col bg-base-200">
      <header className="navbar bg-base-100 shadow-sm">
        <div className="navbar-start">
          <Link href="/" className="btn btn-ghost text-lg">
            Alma
          </Link>
        </div>
        <nav className="navbar-end gap-2">
          <Link href="/apply" className="btn btn-ghost">
            Apply
          </Link>
          {signedIn ? (
            <Link href="/leads" className="btn btn-ghost">
              Leads
            </Link>
          ) : (
            <Link href="/login" className="btn btn-ghost">
              Attorney sign in
            </Link>
          )}
        </nav>
      </header>
      <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-8 sm:px-6">{children}</main>
      <footer className="footer footer-center bg-base-100 p-4 text-base-content/70 sm:footer-horizontal">
        <p>Prospects apply here. Attorneys review leads after signing in.</p>
      </footer>
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

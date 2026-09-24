import Link from "next/link";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { StatusBadge } from "../../components/site-frame";

type Lead = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  status: string;
  created_at: string;
};

const leadsUrl = process.env.LEADS_URL ?? "http://127.0.0.1:8003";

export default async function LeadsPage() {
  const token = (await cookies()).get("access_token")?.value;
  if (!token) {
    redirect("/login");
  }
  const response = await fetch(`${leadsUrl}/leads`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  if (response.status === 401) {
    redirect("/login");
  }
  const leads = (await response.json()) as Lead[];
  const pendingCount = leads.filter((lead) => lead.status === "PENDING").length;

  return (
    <div>
      <h1 className="text-3xl font-semibold">Leads</h1>
      <p className="mt-2 text-base-content/70">
        {leads.length === 0
          ? "No applications yet."
          : `${pendingCount} waiting for contact, ${leads.length} total.`}
      </p>
      {leads.length === 0 ? (
        <div className="mt-6 rounded-box bg-base-100 p-8 text-base-content/70">
          New applications will show up here after a prospect submits the form.
        </div>
      ) : (
        <div className="mt-6 overflow-x-auto rounded-box bg-base-100">
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Status</th>
                <th>Submitted</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((lead) => (
                <tr key={lead.id} className="hover">
                  <td>
                    <Link href={`/leads/${lead.id}`} className="link">
                      {lead.first_name} {lead.last_name}
                    </Link>
                  </td>
                  <td>{lead.email}</td>
                  <td>
                    <StatusBadge status={lead.status} />
                  </td>
                  <td>{new Date(lead.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

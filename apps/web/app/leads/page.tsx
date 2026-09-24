import Link from "next/link";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

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

  return (
    <main>
      <h1>Leads</h1>
      <table>
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
            <tr key={lead.id}>
              <td>
                <Link href={`/leads/${lead.id}`}>
                  {lead.first_name} {lead.last_name}
                </Link>
              </td>
              <td>{lead.email}</td>
              <td>{lead.status}</td>
              <td>{new Date(lead.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

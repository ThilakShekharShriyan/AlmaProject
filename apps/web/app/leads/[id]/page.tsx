import Link from "next/link";
import { cookies } from "next/headers";
import { notFound, redirect } from "next/navigation";
import { ReachOutButton } from "./reach-out-button";

type Lead = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  document_id: string;
  status: string;
  created_at: string;
};

const leadsUrl = process.env.LEADS_URL ?? "http://127.0.0.1:8003";

export default async function LeadDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const token = (await cookies()).get("access_token")?.value;
  if (!token) {
    redirect("/login");
  }
  const response = await fetch(`${leadsUrl}/leads/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  if (response.status === 401) {
    redirect("/login");
  }
  if (response.status === 404) {
    notFound();
  }
  const lead = (await response.json()) as Lead;

  return (
    <main>
      <p>
        <Link href="/leads">Back to leads</Link>
      </p>
      <h1>
        {lead.first_name} {lead.last_name}
      </h1>
      <p>{lead.email}</p>
      <p>Status: {lead.status}</p>
      <p>Submitted: {new Date(lead.created_at).toLocaleString()}</p>
      <p>
        <a href={`/api/leads/${lead.id}/resume`}>Download resume</a>
      </p>
      <ReachOutButton leadId={lead.id} status={lead.status} />
    </main>
  );
}

import Link from "next/link";
import { cookies } from "next/headers";
import { notFound, redirect } from "next/navigation";
import { StatusBadge } from "../../../components/site-frame";
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
    <div className="mx-auto max-w-lg">
      <Link href="/leads" className="link">
        Back to leads
      </Link>
      <article className="card mt-4 bg-base-100 shadow-sm">
        <div className="card-body gap-3">
          <h1 className="card-title text-2xl">
            {lead.first_name} {lead.last_name}
          </h1>
          <p>{lead.email}</p>
          <p>
            <StatusBadge status={lead.status} />
          </p>
          <p className="text-base-content/70">Submitted {new Date(lead.created_at).toLocaleString()}</p>
          <div className="card-actions mt-2 flex-col items-stretch sm:flex-row">
            <a href={`/api/leads/${lead.id}/resume`} className="btn">
              Download resume
            </a>
            <ReachOutButton leadId={lead.id} status={lead.status} />
          </div>
        </div>
      </article>
    </div>
  );
}

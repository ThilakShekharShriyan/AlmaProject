import Link from "next/link";
import { cookies } from "next/headers";
import { notFound, redirect } from "next/navigation";
import { StatusBadge } from "../../../components/site-frame";
import { getLead } from "../../../lib/supabase";
import { ReachOutButton } from "./reach-out-button";

export default async function LeadDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const token = (await cookies()).get("access_token")?.value;
  if (!token) {
    redirect("/login");
  }
  const lead = await getLead(id, token);
  if (lead === 401) {
    redirect("/login");
  }
  if (lead === 404) {
    notFound();
  }

  return (
    <div className="mx-auto w-full min-w-0 max-w-lg">
      <Link href="/leads" className="link">
        Back to leads
      </Link>
      <article className="card mt-4 w-full min-w-0 bg-base-100 shadow-sm">
        <div className="card-body min-w-0 gap-3">
          <h1 className="card-title text-2xl break-words">
            {lead.first_name} {lead.last_name}
          </h1>
          <p className="break-all">{lead.email}</p>
          <p>
            <StatusBadge status={lead.status} />
          </p>
          <p className="text-base-content/70">Submitted {new Date(lead.created_at).toLocaleString()}</p>
          <div className="card-actions mt-2 flex-col items-stretch sm:flex-row">
            <a href={`/api/leads/${lead.id}/resume`} className="btn w-full sm:w-auto">
              Download resume
            </a>
            <ReachOutButton leadId={lead.id} status={lead.status} />
          </div>
        </div>
      </article>
    </div>
  );
}

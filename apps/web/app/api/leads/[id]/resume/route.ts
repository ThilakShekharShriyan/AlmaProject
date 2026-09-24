import { cookies } from "next/headers";

const leadsUrl = process.env.LEADS_URL ?? "http://127.0.0.1:8003";
const documentsUrl = process.env.DOCUMENTS_URL ?? "http://127.0.0.1:8002";

export async function GET(_request: Request, context: { params: Promise<{ id: string }> }) {
  const { id } = await context.params;
  const token = (await cookies()).get("access_token")?.value;
  if (!token) {
    return Response.json({ detail: "not authenticated" }, { status: 401 });
  }
  const leadResponse = await fetch(`${leadsUrl}/leads/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  if (!leadResponse.ok) {
    return Response.json(await leadResponse.json(), { status: leadResponse.status });
  }
  const lead = await leadResponse.json();
  const fileResponse = await fetch(`${documentsUrl}/documents/${lead.document_id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!fileResponse.ok) {
    return Response.json({ detail: "resume unavailable" }, { status: fileResponse.status });
  }
  return new Response(fileResponse.body, {
    headers: {
      "content-type": fileResponse.headers.get("content-type") ?? "application/octet-stream",
      "content-disposition": fileResponse.headers.get("content-disposition") ?? "attachment",
    },
  });
}

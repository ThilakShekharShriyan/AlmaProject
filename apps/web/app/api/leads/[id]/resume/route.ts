import { cookies } from "next/headers";
import { downloadResume, getLead } from "../../../../../lib/supabase";

export async function GET(_request: Request, context: { params: Promise<{ id: string }> }) {
  const { id } = await context.params;
  const token = (await cookies()).get("access_token")?.value;
  if (!token) {
    return Response.json({ detail: "not authenticated" }, { status: 401 });
  }
  const lead = await getLead(id, token);
  if (lead === 401) {
    return Response.json({ detail: "not authenticated" }, { status: 401 });
  }
  if (lead === 404) {
    return Response.json({ detail: "lead not found" }, { status: 404 });
  }
  const file = await downloadResume(lead.document_id, token);
  if (file === 401) {
    return Response.json({ detail: "not authenticated" }, { status: 401 });
  }
  if (file === 404) {
    return Response.json({ detail: "resume unavailable" }, { status: 404 });
  }
  return new Response(file.bytes, {
    headers: {
      "content-type": file.contentType,
      "content-disposition": `attachment; filename="${file.filename}"`,
    },
  });
}

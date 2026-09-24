import { cookies } from "next/headers";
import { markReachedOut } from "../../../../lib/supabase";

export async function PATCH(_request: Request, context: { params: Promise<{ id: string }> }) {
  const { id } = await context.params;
  const token = (await cookies()).get("access_token")?.value;
  if (!token) {
    return Response.json({ detail: "not authenticated" }, { status: 401 });
  }
  const result = await markReachedOut(id, token);
  if (result.lead) {
    return Response.json(result.lead, { status: result.status });
  }
  return Response.json({ detail: result.detail }, { status: result.status });
}

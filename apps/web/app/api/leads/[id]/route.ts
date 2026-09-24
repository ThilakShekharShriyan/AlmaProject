import { cookies } from "next/headers";

const leadsUrl = process.env.LEADS_URL ?? "http://127.0.0.1:8003";

export async function PATCH(request: Request, context: { params: Promise<{ id: string }> }) {
  const { id } = await context.params;
  const token = (await cookies()).get("access_token")?.value;
  if (!token) {
    return Response.json({ detail: "not authenticated" }, { status: 401 });
  }
  const body = await request.json();
  const response = await fetch(`${leadsUrl}/leads/${id}`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify(body),
  });
  const payload = await response.json();
  return Response.json(payload, { status: response.status });
}

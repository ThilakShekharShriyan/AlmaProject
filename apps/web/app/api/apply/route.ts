const documentsUrl = process.env.DOCUMENTS_URL ?? "http://127.0.0.1:8002";
const leadsUrl = process.env.LEADS_URL ?? "http://127.0.0.1:8003";

export async function POST(request: Request) {
  const form = await request.formData();
  const resume = form.get("resume");
  if (!(resume instanceof File)) {
    return Response.json({ detail: "resume is required" }, { status: 422 });
  }

  const upload = new FormData();
  upload.set("file", resume, resume.name);
  const documentResponse = await fetch(`${documentsUrl}/documents`, {
    method: "POST",
    body: upload,
  });
  if (!documentResponse.ok) {
    const detail = await documentResponse.json().catch(() => ({ detail: "upload failed" }));
    return Response.json(detail, { status: documentResponse.status });
  }
  const document = await documentResponse.json();

  const leadResponse = await fetch(`${leadsUrl}/leads`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      first_name: form.get("first_name"),
      last_name: form.get("last_name"),
      email: form.get("email"),
      document_id: document.document_id,
    }),
  });
  const lead = await leadResponse.json().catch(() => ({ detail: "lead create failed" }));
  return Response.json(lead, { status: leadResponse.status });
}

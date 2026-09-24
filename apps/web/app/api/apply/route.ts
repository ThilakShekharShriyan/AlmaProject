import { insertLead, saveResume } from "../../../lib/supabase";
import { sendLeadEmails } from "../../../lib/mail";

export async function POST(request: Request) {
  const form = await request.formData();
  const resume = form.get("resume");
  if (!(resume instanceof File)) {
    return Response.json({ detail: "resume is required" }, { status: 422 });
  }
  const saved = await saveResume(resume);
  if (!saved.ok) {
    return Response.json({ detail: saved.detail }, { status: saved.status });
  }
  const firstName = String(form.get("first_name") ?? "");
  const lastName = String(form.get("last_name") ?? "");
  const email = String(form.get("email") ?? "");
  const lead = await insertLead({ firstName, lastName, email, documentId: saved.documentId });
  if (!lead) {
    return Response.json({ detail: "lead save failed" }, { status: 502 });
  }
  await sendLeadEmails(lead);
  return Response.json(lead);
}

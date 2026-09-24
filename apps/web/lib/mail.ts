import type { Lead } from "./supabase";

export async function sendLeadEmails(lead: Lead): Promise<void> {
  const apiKey = process.env.RESEND_API_KEY;
  const from = process.env.EMAIL_FROM;
  const attorney = process.env.ATTORNEY_NOTIFICATION_EMAIL;
  if (!apiKey || !from || !attorney) {
    console.error("lead %s saved; email config missing", lead.id);
    return;
  }
  const name = `${lead.first_name} ${lead.last_name}`;
  const messages = [
    {
      to: lead.email,
      subject: "We received your application",
      text: `Hello ${name}, we received your resume and an attorney will be in touch.`,
    },
    {
      to: attorney,
      subject: `New lead: ${name}`,
      text: `${name} <${lead.email}> submitted a resume. Lead id ${lead.id}.`,
    },
  ];
  await Promise.all(
    messages.map(async (message) => {
      const response = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { authorization: `Bearer ${apiKey}`, "content-type": "application/json" },
        body: JSON.stringify({ from, to: [message.to], subject: message.subject, text: message.text }),
      });
      if (!response.ok) {
        console.error("lead %s saved; email to %s failed", lead.id, message.to, await response.text());
      }
    }),
  );
}

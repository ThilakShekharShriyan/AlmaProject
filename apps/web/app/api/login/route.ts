import { NextResponse } from "next/server";

const identityUrl = process.env.IDENTITY_URL ?? "http://127.0.0.1:8001";

export async function POST(request: Request) {
  const body = await request.json();
  const response = await fetch(`${identityUrl}/auth/login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  const payload = await response.json().catch(() => ({ detail: "login failed" }));
  if (!response.ok) {
    return NextResponse.json(payload, { status: response.status });
  }
  const next = NextResponse.json({ ok: true });
  next.cookies.set("access_token", payload.access_token, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
  });
  return next;
}

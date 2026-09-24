import { NextResponse } from "next/server";
import { signIn } from "../../../lib/supabase";

export async function POST(request: Request) {
  const body = (await request.json()) as { email?: string; password?: string };
  const token = await signIn(body.email ?? "", body.password ?? "");
  if (!token) {
    return NextResponse.json({ detail: "invalid credentials" }, { status: 401 });
  }
  const next = NextResponse.json({ ok: true });
  next.cookies.set("access_token", token, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    secure: process.env.NODE_ENV === "production",
  });
  return next;
}

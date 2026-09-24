function required(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`${name} is not set`);
  }
  return value;
}

export function supabaseUrl(): string {
  return required("SUPABASE_URL");
}

export function anonKey(): string {
  return required("SUPABASE_ANON_KEY");
}

export function authHeaders(token?: string): HeadersInit {
  const key = anonKey();
  return {
    apikey: key,
    authorization: `Bearer ${token || key}`,
  };
}

export interface Lead {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  document_id: string;
  status: string;
  created_at: string;
}

export async function signIn(email: string, password: string): Promise<string | null> {
  const response = await fetch(`${supabaseUrl()}/auth/v1/token?grant_type=password`, {
    method: "POST",
    headers: { ...authHeaders(), "content-type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    return null;
  }
  const payload = (await response.json()) as { access_token?: string };
  return payload.access_token ?? null;
}

export async function saveResume(file: File): Promise<{ ok: true; documentId: string } | { ok: false; status: number; detail: string }> {
  const suffix = file.name.includes(".") ? file.name.slice(file.name.lastIndexOf(".")).toLowerCase() : "";
  const types: Record<string, string> = {
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  };
  const contentType = types[suffix];
  if (!contentType) {
    return { ok: false, status: 422, detail: "resume must be pdf, doc, or docx" };
  }
  const bytes = await file.arrayBuffer();
  if (bytes.byteLength === 0) {
    return { ok: false, status: 422, detail: "resume is empty" };
  }
  if (bytes.byteLength > 10 * 1024 * 1024) {
    return { ok: false, status: 422, detail: "resume exceeds 10 MB" };
  }
  const documentId = crypto.randomUUID();
  const storagePath = `${documentId}${suffix}`;
  const uploaded = await fetch(`${supabaseUrl()}/storage/v1/object/resumes/${storagePath}`, {
    method: "POST",
    headers: { ...authHeaders(), "content-type": contentType },
    body: bytes,
  });
  if (!uploaded.ok) {
    return { ok: false, status: 502, detail: "resume upload failed" };
  }
  const created = await fetch(`${supabaseUrl()}/rest/v1/documents`, {
    method: "POST",
    headers: { ...authHeaders(), "content-type": "application/json", prefer: "return=minimal" },
    body: JSON.stringify({
      id: documentId,
      filename: file.name || storagePath,
      content_type: contentType,
      storage_path: storagePath,
    }),
  });
  if (!created.ok) {
    return { ok: false, status: 502, detail: "resume record failed" };
  }
  return { ok: true, documentId };
}

export async function insertLead(input: {
  firstName: string;
  lastName: string;
  email: string;
  documentId: string;
}): Promise<Lead | null> {
  const now = new Date().toISOString();
  const row = {
    id: crypto.randomUUID(),
    first_name: input.firstName,
    last_name: input.lastName,
    email: input.email,
    document_id: input.documentId,
    status: "PENDING",
    created_at: now,
    updated_at: now,
  };
  const response = await fetch(`${supabaseUrl()}/rest/v1/leads`, {
    method: "POST",
    headers: { ...authHeaders(), "content-type": "application/json", prefer: "return=minimal" },
    body: JSON.stringify(row),
  });
  if (!response.ok) {
    return null;
  }
  return row;
}

export async function listLeads(token: string): Promise<Lead[] | 401> {
  const response = await fetch(`${supabaseUrl()}/rest/v1/leads?select=*&order=created_at.desc`, {
    headers: { ...authHeaders(token), accept: "application/json" },
    cache: "no-store",
  });
  if (response.status === 401) {
    return 401;
  }
  if (!response.ok) {
    return [];
  }
  return (await response.json()) as Lead[];
}

export async function getLead(id: string, token: string): Promise<Lead | 401 | 404> {
  const response = await fetch(`${supabaseUrl()}/rest/v1/leads?id=eq.${id}&select=*`, {
    headers: { ...authHeaders(token), accept: "application/json" },
    cache: "no-store",
  });
  if (response.status === 401) {
    return 401;
  }
  const rows = response.ok ? ((await response.json()) as Lead[]) : [];
  return rows[0] ?? 404;
}

export async function markReachedOut(id: string, token: string): Promise<{ status: number; lead?: Lead; detail?: string }> {
  const response = await fetch(`${supabaseUrl()}/rest/v1/leads?id=eq.${id}`, {
    method: "PATCH",
    headers: {
      ...authHeaders(token),
      "content-type": "application/json",
      accept: "application/json",
      prefer: "return=representation",
    },
    body: JSON.stringify({ status: "REACHED_OUT" }),
  });
  if (response.status === 401) {
    return { status: 401, detail: "not authenticated" };
  }
  if (!response.ok) {
    const payload = (await response.json().catch(() => ({}))) as { code?: string };
    if (payload.code === "23514") {
      return { status: 409, detail: "lead is already REACHED_OUT" };
    }
    return { status: 502, detail: "lead update failed" };
  }
  const rows = (await response.json()) as Lead[];
  if (!rows[0]) {
    return { status: 404, detail: "lead not found" };
  }
  return { status: 200, lead: rows[0] };
}

export async function downloadResume(
  documentId: string,
  token: string,
): Promise<{ bytes: ArrayBuffer; filename: string; contentType: string } | 401 | 404> {
  const found = await fetch(
    `${supabaseUrl()}/rest/v1/documents?id=eq.${documentId}&select=filename,content_type,storage_path`,
    { headers: { ...authHeaders(token), accept: "application/json" }, cache: "no-store" },
  );
  if (found.status === 401) {
    return 401;
  }
  const rows = found.ok
    ? ((await found.json()) as { filename: string; content_type: string; storage_path: string }[])
    : [];
  const row = rows[0];
  if (!row) {
    return 404;
  }
  const file = await fetch(`${supabaseUrl()}/storage/v1/object/resumes/${row.storage_path}`, {
    headers: authHeaders(token),
  });
  if (file.status === 401) {
    return 401;
  }
  if (!file.ok) {
    return 404;
  }
  return { bytes: await file.arrayBuffer(), filename: row.filename, contentType: row.content_type };
}

import { cookies } from "next/headers";
import { SignedInGate } from "../../components/signed-in-gate";
import { ApplyForm } from "./apply-form";

export default async function ApplyPage() {
  if ((await cookies()).get("access_token")?.value) {
    return <SignedInGate />;
  }
  return <ApplyForm />;
}

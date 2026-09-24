import Link from "next/link";

export default function Home() {
  return (
    <main>
      <h1>Lead intake</h1>
      <p>
        <Link href="/apply">Apply</Link>
        {" · "}
        <Link href="/login">Attorney login</Link>
      </p>
    </main>
  );
}

import Link from "next/link";

export default function HomePage() {
  return (
    <main>
      <h1>Wash World</h1>
      <p>This is the Next.js home page.</p>
      <p>
        <Link href="/page">Open the name demo</Link>
      </p>
    </main>
  );
}

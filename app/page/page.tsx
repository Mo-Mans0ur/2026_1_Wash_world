"use client";

import { useState } from "react";
import getName from "./GetName";

export default function NamePage() {
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleGetName() {
    try {
      setIsLoading(true);
      setError("");
      const fetchedName = await getName();
      setName(fetchedName);
    } catch {
      setError("Could not load the name");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main>
      <h1>Welcome to the Page Route</h1>
      <button type="button" onClick={handleGetName} disabled={isLoading}>
        {isLoading ? "Loading..." : "Get Name"}
      </button>
      {name ? <p>{name}</p> : null}
      {error ? <p>{error}</p> : null}
    </main>
  );
}

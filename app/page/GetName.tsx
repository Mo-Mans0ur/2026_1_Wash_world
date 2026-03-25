export default async function getName() {
  const response = await fetch("/api/get-name", {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch name");
  }

  const data = await response.json();
  return data.name as string;
}

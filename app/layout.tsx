import type { ReactNode } from "react";

export const metadata = {
  title: "Wash World",
  description: "Next.js demo page",
};

type RootLayoutProps = {
  children: ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

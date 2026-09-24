import type { Metadata } from "next";
import { SiteFrame } from "../components/site-frame";
import "./globals.css";

export const metadata: Metadata = {
  title: "Alma lead intake",
  description: "Submit a resume or review prospect leads.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" data-theme="cream">
      <body>
        <SiteFrame>{children}</SiteFrame>
      </body>
    </html>
  );
}

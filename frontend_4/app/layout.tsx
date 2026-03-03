import type { Metadata } from "next";
import "./globals.css";
import Navbar from "../components/Navbar";
import FeedbackToggle from "@/components/FeedbackToggle";
import ScrollToTop from "@/components/ScrollToTop";

export const metadata: Metadata = {
  title: "CivicResolve Secure",
  description: "Modern infrastructure management portal",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossOrigin=""
        />
      </head>
      <body className="antialiased pt-20">
        <Navbar />
        <ScrollToTop />
        {children}
        <FeedbackToggle />
      </body>
    </html>
  );
}

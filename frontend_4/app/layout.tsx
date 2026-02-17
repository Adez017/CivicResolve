import type { Metadata } from "next";
import "./globals.css";
import FeedbackToggle from "@/components/FeedbackToggle";

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
    <script
      dangerouslySetInnerHTML={{
        __html: `
          (function () {
            const theme = localStorage.getItem('theme');
            if (theme === 'light') {
              document.documentElement.classList.remove('dark');
            } else {
              document.documentElement.classList.add('dark');
            }
          })();
        `,
      }}
    />
    <link
      rel="stylesheet"
      href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
      integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
      crossOrigin=""
    />
  </head>
  <body className="antialiased transition-colors duration-500">
    {children}
  </body>
</html>

  );
}

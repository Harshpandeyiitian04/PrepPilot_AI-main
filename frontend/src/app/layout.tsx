// This file is the outer frame of every page: the fonts, the page title, and the place where each page sits.

import type { Metadata } from "next";
import { IBM_Plex_Mono, Inter } from "next/font/google";
import "./globals.css";

// The typewriter-style font used for headings and small labels.
const plexMono = IBM_Plex_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

// The plain reading font used for normal text.
const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

// The name and short description shown in the browser tab.
export const metadata: Metadata = {
  title: "InterviewOS",
  description: "Multi-agent AI interview platform by Harsh Pandey",
};

// Wraps every page in the same html and body, and applies both fonts.
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body className={`${plexMono.variable} ${inter.variable} antialiased font-sans-body`}>
        {children}
      </body>
    </html>
  );
}

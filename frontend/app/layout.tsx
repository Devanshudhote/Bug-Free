import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'TruthShield AI — Dual Detection System',
  description: 'AI-powered dual detection system that verifies news credibility and validates physics claims in real time.',
  keywords: ['fake news detection', 'physics verification', 'AI', 'truth detection', 'BERT', 'FastAPI'],
  openGraph: {
    title: 'TruthShield AI',
    description: 'Verify news and physics claims with AI',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

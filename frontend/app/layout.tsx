
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body style={{ margin: 0, fontFamily: "system-ui, Arial" }}>
        <header style={{ padding: 16, borderBottom: "1px solid #eee", display: "flex", gap: 16 }}>
          <strong>IMEC Intelligence Hub</strong>
          <nav style={{ display: "flex", gap: 12 }}>
            <a href="/">Accueil</a>
            <a href="/?lang=fr">FR</a>
            <a href="/?lang=en">EN</a>
            <a href="/?lang=ar">AR</a>
          </nav>
        </header>
        <main style={{ padding: 16 }}>{children}</main>
      </body>
    </html>
  );
}

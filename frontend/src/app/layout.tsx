import type { Metadata } from "next"
import "./globals.css"
import Header from "./Header"

export const metadata: Metadata = {
  title: "レッツ不労所得",
  description: "株の保有情報と配当金情報を組み合わせて可視化するアプリ",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body className="container mx-auto bg-slate-700 text-slate-50">
        <div className="flex flex-col min-h-screen">
          <Header />
          <main className="flex-grow">{children}</main>
        </div>
      </body>
    </html>
  )
}

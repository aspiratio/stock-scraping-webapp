import Link from "next/link"
import React from "react"

const Header = () => {
  return (
    <header className="py-5 px-10 border-b flex justify-between items-center">
      <h1 className="text-2xl font-extrabold">
        <Link href="/">レッツ不労所得</Link>
      </h1>
    </header>
  )
}

export default Header

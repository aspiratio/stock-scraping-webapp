"use client"
import {
  getCurrentAuthUser,
  logout,
  monitorAuthState,
} from "@/utils/firebaseAuth"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"

const Header = () => {
  const [isLogin, setIsLogin] = useState<boolean>(false)
  const router = useRouter()

  useEffect(() => {
    // ユーザーがログインしているかどうかを監視する
    const unsubscribe = monitorAuthState((user) => {
      setIsLogin(!!user)
      !user && router.push("/login")
    })
    // コンポーネントがアンマウントされるときにリスナーをクリーンアップ
    return () => unsubscribe()
  }, [router])

  const onClickLogout = async () => {
    await logout()
    router.push("/login")
  }
  return (
    <header className="py-5 px-10 border-b flex justify-between items-center">
      <h1 className="text-2xl font-extrabold">
        <Link href="/">レッツ不労所得</Link>
      </h1>
      {isLogin && <button onClick={onClickLogout}>ログアウト</button>}
    </header>
  )
}

export default Header

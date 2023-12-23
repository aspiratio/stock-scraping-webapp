"use client"
import { loginWithEmailAndPassword } from "@/utils/firebaseAuth"
import { useState } from "react"
import { useRouter } from "next/navigation"

const LoginPage = () => {
  const router = useRouter()
  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    try {
      const isEmailVerfied = await loginWithEmailAndPassword(email, password)
      if (isEmailVerfied) {
        router.push("/")
      }
    } catch (error: any) {
      alert(error.message)
    }
  }
  return (
    <div>
      <h1>ログインページ</h1>

      <form onSubmit={(e) => handleSubmit(e)}>
        <input
          type="email"
          placeholder="メールアドレス"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="text-black"
        />
        <input
          type="password"
          placeholder="パスワード"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="text-black"
        />
        <button type="submit">ログイン</button>
      </form>
    </div>
  )
}

export default LoginPage

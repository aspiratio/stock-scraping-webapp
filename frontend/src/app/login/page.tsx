"use client"
import { loginWithEmailAndPassword } from "@/utils/firebaseAuth"
import { useState } from "react"
import { useRouter } from "next/navigation"
import Button from "@/components/button"

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
    <form
      onSubmit={(e) => handleSubmit(e)}
      className="text-lg flex flex-col items-center justify-center h-screen"
    >
      <div className="m-4">
        <label htmlFor="email">メールアドレス</label>
        <input
          type="email"
          id="email"
          placeholder="メールアドレス"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="text-black w-80 block"
        />
      </div>
      <div className="m-4">
        <label htmlFor="password">パスワード</label>
        <input
          type="password"
          id="password"
          placeholder="パスワード"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="text-black w-80 block"
        />
      </div>
      <Button type="submit" className="mt-8">
        ログイン
      </Button>
    </form>
  )
}

export default LoginPage

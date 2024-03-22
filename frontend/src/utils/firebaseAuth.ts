import { onAuthStateChanged, signOut } from "firebase/auth"
import { signInWithEmailAndPassword } from "firebase/auth"
import { auth } from "@/utils/config"

export const loginWithEmailAndPassword = async (
  email: string,
  password: string
) => {
  try {
    await signInWithEmailAndPassword(auth, email, password)
    return true
  } catch {
    throw Error("メールアドレスかパスワードが間違っています")
  }
}

export const logout = async () => {
  await signOut(auth)
}

export const getCurrentAuthUser = () => {
  return auth.currentUser
}

export const monitorAuthState = (callback: (user: any) => void) => {
  return onAuthStateChanged(auth, callback)
}

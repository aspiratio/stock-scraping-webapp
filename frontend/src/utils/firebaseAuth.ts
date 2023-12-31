import { initializeApp } from "firebase/app"
import { getAuth, onAuthStateChanged, signOut } from "firebase/auth"
import { signInWithEmailAndPassword } from "firebase/auth"

const firebaseApp = initializeApp({
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
})

const auth = getAuth()

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

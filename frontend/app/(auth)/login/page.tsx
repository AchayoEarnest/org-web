import { Metadata } from "next"
import Link from "next/link"
import { LoginForm } from "@/components/forms/LoginForm"

export const metadata: Metadata = { title: "Sign In" }

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold">Welcome back</h1>
          <p className="mt-2 text-sm text-gray-500">Sign in to your account</p>
        </div>
        <div className="card p-8">
          <LoginForm />
          <p className="mt-6 text-center text-sm text-gray-500">
            Do not have an account?{" "}
            <Link href="/register" className="text-brand-600 hover:underline font-medium">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

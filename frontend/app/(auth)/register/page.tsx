import { Metadata } from "next"
import Link from "next/link"
import { RegisterForm } from "@/components/forms/RegisterForm"

export const metadata: Metadata = { title: "Create Account" }

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold">Create an account</h1>
          <p className="mt-2 text-sm text-gray-500">Join our community today</p>
        </div>
        <div className="card p-8">
          <RegisterForm />
          <p className="mt-6 text-center text-sm text-gray-500">
            Already have an account?{" "}
            <Link href="/login" className="text-brand-600 hover:underline font-medium">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}

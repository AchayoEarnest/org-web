"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Loader2 } from "lucide-react"
import { apiClient } from "@/lib/api"
import { signIn } from "next-auth/react"

const schema = z.object({
  full_name:  z.string().min(2, "Name must be at least 2 characters"),
  email:      z.string().email("Invalid email"),
  password:   z.string().min(8, "Password must be at least 8 characters"),
  password2:  z.string(),
}).refine((d) => d.password === d.password2, { message: "Passwords do not match", path: ["password2"] })

type FormData = z.infer<typeof schema>

export function RegisterForm() {
  const router = useRouter()
  const [error, setError] = useState("")

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormData) => {
    setError("")
    try {
      await apiClient.post("/auth/register/", data)
      await signIn("credentials", { email: data.email, password: data.password, redirect: false })
      router.push("/dashboard/member")
    } catch (err: any) {
      setError(err.response?.data?.email?.[0] ?? "Registration failed. Please try again.")
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 p-3 text-sm text-red-600">{error}</div>
      )}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Full Name</label>
        <input {...register("full_name")} placeholder="Jane Doe" className="input" />
        {errors.full_name && <p className="mt-1 text-xs text-red-500">{errors.full_name.message}</p>}
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Email</label>
        <input {...register("email")} type="email" placeholder="you@example.com" className="input" />
        {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email.message}</p>}
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Password</label>
        <input {...register("password")} type="password" placeholder="••••••••" className="input" />
        {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password.message}</p>}
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Confirm Password</label>
        <input {...register("password2")} type="password" placeholder="••••••••" className="input" />
        {errors.password2 && <p className="mt-1 text-xs text-red-500">{errors.password2.message}</p>}
      </div>
      <button type="submit" disabled={isSubmitting} className="btn-primary w-full">
        {isSubmitting ? <><Loader2 size={16} className="animate-spin" /> Creating account…</> : "Create Account"}
      </button>
    </form>
  )
}

"use client"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Loader2, CheckCircle } from "lucide-react"
import { apiClient } from "@/lib/api"

const schema = z.object({
  name:    z.string().min(2),
  email:   z.string().email(),
  subject: z.string().min(5),
  message: z.string().min(20, "Message must be at least 20 characters"),
})
type FormData = z.infer<typeof schema>

export function ContactForm() {
  const [success, setSuccess] = useState(false)
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormData) => {
    await apiClient.post("/contact/", data)
    setSuccess(true)
    reset()
  }

  if (success) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center gap-3">
        <CheckCircle size={48} className="text-green-500" />
        <h3 className="text-lg font-semibold">Message Sent!</h3>
        <p className="text-gray-500 text-sm">We will get back to you within 1-2 business days.</p>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Name</label>
          <input {...register("name")} placeholder="Your name" className="input" />
          {errors.name && <p className="mt-1 text-xs text-red-500">{errors.name.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Email</label>
          <input {...register("email")} type="email" placeholder="you@example.com" className="input" />
          {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email.message}</p>}
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Subject</label>
        <input {...register("subject")} placeholder="How can we help?" className="input" />
        {errors.subject && <p className="mt-1 text-xs text-red-500">{errors.subject.message}</p>}
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Message</label>
        <textarea {...register("message")} rows={5} placeholder="Your message…" className="input resize-none" />
        {errors.message && <p className="mt-1 text-xs text-red-500">{errors.message.message}</p>}
      </div>
      <button type="submit" disabled={isSubmitting} className="btn-primary w-full">
        {isSubmitting ? <><Loader2 size={16} className="animate-spin" /> Sending…</> : "Send Message"}
      </button>
    </form>
  )
}

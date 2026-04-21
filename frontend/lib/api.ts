import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from "axios"
import { getSession, signOut } from "next-auth/react"

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

function createApiClient(): AxiosInstance {
  const client = axios.create({
    baseURL: `${API_BASE}/api/v1`,
    headers: { "Content-Type": "application/json" },
    timeout: 15_000,
  })

  client.interceptors.request.use(async (config: InternalAxiosRequestConfig) => {
    const session = await getSession()
    if (session?.accessToken) {
      config.headers.Authorization = `Bearer ${session.accessToken}`
    }
    return config
  })

  client.interceptors.response.use(
    (res) => res,
    async (error: AxiosError) => {
      if (error.response?.status === 401) {
        await signOut({ callbackUrl: "/login" })
      }
      return Promise.reject(error)
    }
  )

  return client
}

export const apiClient = createApiClient()

// Server-side fetch helper (RSC / Server Actions)
export async function apiFetch<T>(
  path: string,
  options?: RequestInit & { token?: string }
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options?.headers as Record<string, string>),
  }
  if (options?.token) {
    headers.Authorization = `Bearer ${options.token}`
  }
  const res = await fetch(`${API_BASE}/api/v1${path}`, {
    ...options,
    headers,
    next: { revalidate: 60 },
  })
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${res.statusText}`)
  }
  return res.json() as Promise<T>
}

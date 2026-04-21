"use client"
import { useSession } from "next-auth/react"
import type { Role } from "@/types"

export function useAuth() {
  const { data: session, status } = useSession()

  return {
    user:          session?.user,
    role:          (session?.user?.role ?? "member") as Role,
    accessToken:   session?.accessToken,
    isLoading:     status === "loading",
    isAuth:        status === "authenticated",
    isAdmin:       session?.user?.role === "admin",
    isStaff:       session?.user?.role === "staff",
    isStaffOrAdmin: ["admin", "staff"].includes(session?.user?.role ?? ""),
  }
}

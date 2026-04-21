import { getServerSession } from "next-auth"
import { redirect } from "next/navigation"
import { authOptions } from "@/lib/auth"
import { AdminDashboard } from "@/components/dashboard/AdminDashboard"

export const metadata = { title: "Admin Dashboard" }

export default async function AdminPage() {
  const session = await getServerSession(authOptions)
  if (!session || session.user.role !== "admin") redirect("/dashboard/member")
  return <AdminDashboard accessToken={session.accessToken} />
}

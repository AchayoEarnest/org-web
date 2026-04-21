import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"

export const metadata = { title: "My Dashboard" }

export default async function MemberPage() {
  const session = await getServerSession(authOptions)
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-6">My Dashboard</h1>
      <div className="card p-6">
        <p className="text-gray-500">Welcome, {session?.user?.name}!</p>
      </div>
    </div>
  )
}

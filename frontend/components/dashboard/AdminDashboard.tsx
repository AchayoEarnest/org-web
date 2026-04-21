"use client"
import { useQuery } from "@tanstack/react-query"
import { Users, Eye, Calendar, TrendingUp } from "lucide-react"
import { apiClient } from "@/lib/api"
import {
  AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts"

interface KPICardProps {
  title: string
  value?: number | string
  icon: React.ElementType
  trend?: number
  color: string
}

function KPICard({ title, value, icon: Icon, trend, color }: KPICardProps) {
  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4">
        <span className="text-sm font-medium text-gray-500">{title}</span>
        <div className={`w-9 h-9 rounded-lg ${color} flex items-center justify-center`}>
          <Icon size={16} className="text-white" />
        </div>
      </div>
      <div className="text-3xl font-bold">{value ?? "—"}</div>
      {trend !== undefined && (
        <div className={`mt-1 text-xs font-medium ${trend >= 0 ? "text-green-600" : "text-red-500"}`}>
          {trend >= 0 ? "+" : ""}{trend}% this week
        </div>
      )}
    </div>
  )
}

export function AdminDashboard({ accessToken }: { accessToken: string }) {
  const { data } = useQuery({
    queryKey: ["dashboard"],
    queryFn:  () => apiClient.get("/analytics/dashboard/").then((r) => r.data),
    refetchInterval: 30_000,
  })

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
        <KPICard title="Total Users"   value={data?.users}      icon={Users}    trend={12}  color="bg-brand-500" />
        <KPICard title="Page Views"    value={data?.page_views} icon={Eye}      trend={8}   color="bg-emerald-500" />
        <KPICard title="Active Events" value={data?.events}     icon={Calendar} trend={-2}  color="bg-violet-500" />
        <KPICard title="New Signups"   value={data?.signups}    icon={TrendingUp} trend={24} color="bg-amber-500" />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h2 className="text-base font-semibold mb-6">Page Views (30 days)</h2>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={data?.views_chart ?? []}>
              <defs>
                <linearGradient id="gv" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#2563eb" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="day" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Area type="monotone" dataKey="count" stroke="#2563eb" fill="url(#gv)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <div className="card p-6">
          <h2 className="text-base font-semibold mb-6">Users by Role</h2>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data?.users_by_role ?? []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="role" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="count" fill="#2563eb" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

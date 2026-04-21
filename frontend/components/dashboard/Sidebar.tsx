"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { signOut } from "next-auth/react"
import {
  LayoutDashboard, Users, FileText, Calendar, Briefcase,
  BarChart, Bell, Settings, LogOut, FolderOpen, MessageSquare,
} from "lucide-react"
import { cn } from "@/lib/utils"
import type { Role } from "@/types"

interface NavItem { href: string; label: string; icon: React.ElementType; roles: Role[] }

const NAV: NavItem[] = [
  { href: "/dashboard/admin",  label: "Dashboard",  icon: LayoutDashboard, roles: ["admin"] },
  { href: "/dashboard/staff",  label: "Dashboard",  icon: LayoutDashboard, roles: ["staff"] },
  { href: "/dashboard/member", label: "My Account",  icon: LayoutDashboard, roles: ["member"] },
  { href: "/dashboard/admin/users",   label: "Users",     icon: Users,        roles: ["admin"] },
  { href: "/dashboard/admin/content", label: "Content",   icon: FileText,     roles: ["admin", "staff"] },
  { href: "/dashboard/admin/media",   label: "Media",     icon: FolderOpen,   roles: ["admin", "staff"] },
  { href: "/dashboard/admin/events",  label: "Events",    icon: Calendar,     roles: ["admin", "staff"] },
  { href: "/dashboard/admin/careers", label: "Careers",   icon: Briefcase,    roles: ["admin", "staff"] },
  { href: "/dashboard/admin/messages", label: "Messages", icon: MessageSquare, roles: ["admin", "staff"] },
  { href: "/dashboard/admin/analytics", label: "Analytics", icon: BarChart,  roles: ["admin"] },
  { href: "/dashboard/notifications",   label: "Notifications", icon: Bell,  roles: ["admin", "staff", "member"] },
  { href: "/dashboard/settings",        label: "Settings",      icon: Settings, roles: ["admin", "staff", "member"] },
]

export function Sidebar({ role }: { role: Role }) {
  const pathname = usePathname()
  const items    = NAV.filter((item) => item.roles.includes(role))

  return (
    <aside className="w-56 flex-shrink-0 hidden md:flex flex-col bg-white dark:bg-gray-900 border-r border-gray-100 dark:border-gray-800 h-full">
      <div className="h-16 flex items-center px-5 border-b border-gray-100 dark:border-gray-800">
        <Link href="/" className="font-bold text-lg text-brand-600">OrgSite</Link>
      </div>
      <nav className="flex-1 overflow-y-auto py-4 px-3">
        <ul className="space-y-0.5">
          {items.map(({ href, label, icon: Icon }) => (
            <li key={href}>
              <Link
                href={href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                  pathname === href
                    ? "bg-brand-50 dark:bg-brand-900/30 text-brand-600"
                    : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-100"
                )}
              >
                <Icon size={16} />
                {label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <div className="p-3 border-t border-gray-100 dark:border-gray-800">
        <button
          onClick={() => signOut({ callbackUrl: "/" })}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 w-full transition-colors"
        >
          <LogOut size={16} /> Sign out
        </button>
      </div>
    </aside>
  )
}

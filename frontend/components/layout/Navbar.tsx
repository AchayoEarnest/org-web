"use client"
import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { useSession, signOut } from "next-auth/react"
import { Menu, X, ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"

const NAV_LINKS = [
  { href: "/about",    label: "About" },
  { href: "/services", label: "Services" },
  { href: "/projects", label: "Projects" },
  { href: "/blog",     label: "Blog" },
  { href: "/events",   label: "Events" },
  { href: "/careers",  label: "Careers" },
  { href: "/contact",  label: "Contact" },
]

export function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const pathname = usePathname()
  const { data: session } = useSession()

  return (
    <header className="fixed top-0 inset-x-0 z-50 bg-white/90 dark:bg-gray-900/90 backdrop-blur border-b border-gray-100 dark:border-gray-800">
      <nav className="container-wide flex items-center justify-between h-16">
        <Link href="/" className="font-bold text-xl text-brand-600">OrgSite</Link>

        {/* Desktop nav */}
        <ul className="hidden md:flex items-center gap-1">
          {NAV_LINKS.map(({ href, label }) => (
            <li key={href}>
              <Link
                href={href}
                className={cn(
                  "px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                  pathname === href
                    ? "bg-brand-50 dark:bg-brand-900/30 text-brand-600"
                    : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                )}
              >
                {label}
              </Link>
            </li>
          ))}
        </ul>

        <div className="hidden md:flex items-center gap-3">
          {session ? (
            <div className="relative group">
              <button className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-brand-600">
                {session.user.name?.split(" ")[0]}
                <ChevronDown size={14} />
              </button>
              <div className="absolute right-0 top-full mt-1 w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                <Link href="/dashboard/admin" className="block px-4 py-2.5 text-sm hover:bg-gray-50 dark:hover:bg-gray-700 rounded-t-xl">
                  Dashboard
                </Link>
                <button onClick={() => signOut({ callbackUrl: "/" })} className="w-full text-left px-4 py-2.5 text-sm hover:bg-gray-50 dark:hover:bg-gray-700 text-red-600 rounded-b-xl">
                  Sign out
                </button>
              </div>
            </div>
          ) : (
            <>
              <Link href="/login"    className="btn-secondary text-sm">Sign in</Link>
              <Link href="/register" className="btn-primary  text-sm">Get Started</Link>
            </>
          )}
        </div>

        <button className="md:hidden p-2" onClick={() => setMobileOpen(!mobileOpen)}>
          {mobileOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </nav>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 px-4 pb-4">
          {NAV_LINKS.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              onClick={() => setMobileOpen(false)}
              className="block py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:text-brand-600"
            >
              {label}
            </Link>
          ))}
          <div className="mt-4 flex flex-col gap-2">
            {session ? (
              <button onClick={() => signOut()} className="btn-secondary text-sm">Sign out</button>
            ) : (
              <>
                <Link href="/login"    onClick={() => setMobileOpen(false)} className="btn-secondary text-sm text-center">Sign in</Link>
                <Link href="/register" onClick={() => setMobileOpen(false)} className="btn-primary  text-sm text-center">Get Started</Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  )
}

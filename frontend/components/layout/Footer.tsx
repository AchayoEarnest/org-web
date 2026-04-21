import Link from "next/link"

const LINKS = {
  Organization: [
    { href: "/about",    label: "About Us" },
    { href: "/services", label: "Services" },
    { href: "/projects", label: "Projects" },
    { href: "/careers",  label: "Careers" },
  ],
  Resources: [
    { href: "/blog",      label: "Blog" },
    { href: "/events",    label: "Events" },
    { href: "/documents", label: "Resources" },
    { href: "/contact",   label: "Contact" },
  ],
}

export function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="container-wide py-16 grid grid-cols-1 md:grid-cols-4 gap-10">
        <div className="col-span-1 md:col-span-2">
          <span className="text-white font-bold text-xl">OrgSite</span>
          <p className="mt-3 text-sm text-gray-400 max-w-sm leading-relaxed">
            Empowering communities through education, innovation, and collaboration. Join us in making a difference.
          </p>
        </div>
        {Object.entries(LINKS).map(([title, links]) => (
          <div key={title}>
            <h4 className="text-white font-semibold text-sm mb-4">{title}</h4>
            <ul className="space-y-2">
              {links.map(({ href, label }) => (
                <li key={href}>
                  <Link href={href} className="text-sm text-gray-400 hover:text-white transition-colors">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="border-t border-gray-800 container-wide py-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-gray-500">
        <span>© {new Date().getFullYear()} Org Website. All rights reserved.</span>
        <div className="flex gap-4">
          <Link href="/privacy" className="hover:text-gray-300 transition-colors">Privacy Policy</Link>
          <Link href="/terms"   className="hover:text-gray-300 transition-colors">Terms of Service</Link>
        </div>
      </div>
    </footer>
  )
}

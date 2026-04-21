import { Globe, BookOpen, Users, Heart, BarChart, Shield } from "lucide-react"

const SERVICES = [
  { icon: Globe,     title: "Community Programs",   desc: "Outreach and support programs for underserved communities." },
  { icon: BookOpen,  title: "Education & Training",  desc: "Skill-building workshops, courses, and certifications." },
  { icon: Users,     title: "Leadership Development", desc: "Empowering the next generation of community leaders." },
  { icon: Heart,     title: "Health & Wellness",     desc: "Access to essential health resources and awareness campaigns." },
  { icon: BarChart,  title: "Research & Advocacy",   desc: "Data-driven insights to inform policy and practice." },
  { icon: Shield,    title: "Capacity Building",     desc: "Strengthening organizations through mentorship and grants." },
]

export function ServicesGrid() {
  return (
    <section className="section">
      <div className="container-wide">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">What We Do</h2>
          <p className="mt-3 text-gray-500 dark:text-gray-400">Comprehensive programs designed for lasting impact</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {SERVICES.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="card p-6 hover:shadow-md transition-shadow group">
              <div className="w-12 h-12 rounded-xl bg-brand-50 dark:bg-brand-900/30 flex items-center justify-center mb-4 group-hover:bg-brand-100 transition-colors">
                <Icon size={22} className="text-brand-600 dark:text-brand-400" />
              </div>
              <h3 className="font-semibold text-lg mb-2">{title}</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

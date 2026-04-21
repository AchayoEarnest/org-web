import Link from "next/link"
import { ArrowRight, Calendar, MapPin } from "lucide-react"
import { formatDate } from "@/lib/utils"
import type { Event } from "@/types"

export function UpcomingEvents({ events }: { events: Event[] }) {
  if (!events.length) return null
  return (
    <section className="section">
      <div className="container-wide">
        <div className="flex items-end justify-between mb-10">
          <div>
            <h2 className="text-3xl font-bold">Upcoming Events</h2>
            <p className="mt-2 text-gray-500 dark:text-gray-400">Join us in person or online</p>
          </div>
          <Link href="/events" className="hidden sm:flex items-center gap-1 text-sm font-medium text-brand-600 hover:underline">
            All events <ArrowRight size={14} />
          </Link>
        </div>
        <div className="space-y-4">
          {events.map((event) => (
            <div key={event.id} className="card p-5 flex items-start gap-5 hover:shadow-md transition-shadow">
              <div className="flex-shrink-0 w-14 h-14 rounded-xl bg-brand-50 dark:bg-brand-900/30 flex flex-col items-center justify-center text-brand-600 dark:text-brand-400">
                <span className="text-xs font-medium uppercase">{formatDate(event.start_datetime, "MMM")}</span>
                <span className="text-xl font-bold leading-none">{formatDate(event.start_datetime, "d")}</span>
              </div>
              <div className="flex-1">
                <h3 className="font-semibold">{event.title}</h3>
                <div className="flex flex-wrap gap-3 mt-1 text-sm text-gray-500">
                  <span className="flex items-center gap-1"><Calendar size={12} />{formatDate(event.start_datetime, "h:mm a")}</span>
                  {event.location && <span className="flex items-center gap-1"><MapPin size={12} />{event.location}</span>}
                </div>
              </div>
              <Link href={`/events/${event.slug}`} className="btn-secondary text-sm whitespace-nowrap flex-shrink-0">
                Register
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

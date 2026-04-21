import { Metadata } from "next"
import Link from "next/link"
import Image from "next/image"
import { apiFetch } from "@/lib/api"
import { formatDate } from "@/lib/utils"
import type { PaginatedResponse, Event } from "@/types"

export const metadata: Metadata = { title: "Events" }
export const revalidate = 60

export default async function EventsPage() {
  const data = await apiFetch<PaginatedResponse<Event>>("/events/?page_size=20").catch(() => ({ results: [] as Event[] }))

  return (
    <main className="section">
      <div className="container-wide">
        <h1 className="text-4xl font-bold mb-2">Upcoming Events</h1>
        <p className="text-gray-500 dark:text-gray-400 mb-12">Join us at one of our upcoming events</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {data.results.map((event) => (
            <article key={event.id} className="card overflow-hidden hover:shadow-md transition-shadow">
              {event.featured_image && (
                <div className="relative h-44">
                  <Image src={event.featured_image} alt={event.title} fill className="object-cover" />
                </div>
              )}
              <div className="p-6">
                <div className="flex items-center gap-2 text-xs mb-3">
                  <span className={`px-2 py-0.5 rounded-full font-medium ${event.is_free ? "bg-green-100 text-green-700" : "bg-blue-100 text-blue-700"}`}>
                    {event.is_free ? "Free" : `$${event.price}`}
                  </span>
                  {event.is_virtual && (
                    <span className="px-2 py-0.5 rounded-full font-medium bg-purple-100 text-purple-700">Virtual</span>
                  )}
                </div>
                <h2 className="text-lg font-semibold leading-snug line-clamp-2 mb-2">{event.title}</h2>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {formatDate(event.start_datetime, "EEE, MMM d · h:mm a")}
                </p>
                {event.location && <p className="text-sm text-gray-500 mt-1">{event.location}</p>}
                <div className="mt-4 flex items-center justify-between">
                  {event.spots_left !== null && (
                    <span className="text-xs text-gray-400">{event.spots_left} spots left</span>
                  )}
                  <Link href={`/events/${event.slug}`} className="btn-primary text-xs px-4 py-2 ml-auto">
                    Register
                  </Link>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </main>
  )
}

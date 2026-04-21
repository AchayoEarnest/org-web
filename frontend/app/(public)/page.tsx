import { Metadata } from "next"
import { HeroSection }     from "@/components/sections/HeroSection"
import { ImpactStats }     from "@/components/sections/ImpactStats"
import { ServicesGrid }    from "@/components/sections/ServicesGrid"
import { FeaturedPosts }   from "@/components/sections/FeaturedPosts"
import { UpcomingEvents }  from "@/components/sections/UpcomingEvents"
import { Partners }        from "@/components/sections/Partners"
import { CTASection }      from "@/components/sections/CTASection"
import { apiFetch }        from "@/lib/api"
import type { PaginatedResponse, Post, Event } from "@/types"

export const metadata: Metadata = {
  title: "Home — Org Website",
  description: "We work to empower communities through education, innovation, and collaboration.",
}
export const revalidate = 60

async function getHomeData() {
  try {
    const [postsRes, eventsRes] = await Promise.all([
      apiFetch<PaginatedResponse<Post>>("/content/posts/?is_featured=true&page_size=3"),
      apiFetch<PaginatedResponse<Event>>("/events/?page_size=3"),
    ])
    return { posts: postsRes.results, events: eventsRes.results }
  } catch {
    return { posts: [], events: [] }
  }
}

export default async function HomePage() {
  const { posts, events } = await getHomeData()

  return (
    <main>
      <HeroSection />
      <ImpactStats />
      <ServicesGrid />
      <FeaturedPosts posts={posts} />
      <UpcomingEvents events={events} />
      <Partners />
      <CTASection />
    </main>
  )
}

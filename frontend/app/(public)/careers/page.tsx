import { Metadata } from "next"
import Link from "next/link"
import { apiFetch } from "@/lib/api"
import type { PaginatedResponse, Job } from "@/types"

export const metadata: Metadata = { title: "Careers" }
export const revalidate = 60

const typeLabel: Record<string, string> = {
  full_time: "Full Time", part_time: "Part Time",
  contract: "Contract", internship: "Internship", volunteer: "Volunteer",
}

export default async function CareersPage() {
  const data = await apiFetch<PaginatedResponse<Job>>("/careers/jobs/?is_active=true").catch(() => ({ results: [] as Job[] }))

  return (
    <main className="section">
      <div className="container-narrow">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Join Our Team</h1>
          <p className="text-gray-500 dark:text-gray-400">
            We are looking for passionate people to help us make an impact.
          </p>
        </div>
        <div className="space-y-4">
          {data.results.map((job) => (
            <div key={job.id} className="card p-6 flex items-start justify-between gap-6 hover:shadow-md transition-shadow">
              <div>
                <h2 className="text-lg font-semibold">{job.title}</h2>
                <div className="flex flex-wrap gap-2 mt-2">
                  <span className="text-sm text-gray-500">{job.department}</span>
                  <span className="text-gray-300 dark:text-gray-600">·</span>
                  <span className="text-sm text-gray-500">{job.location}</span>
                  <span className="text-gray-300 dark:text-gray-600">·</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-brand-50 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400 font-medium">
                    {typeLabel[job.type]}
                  </span>
                </div>
              </div>
              <Link href={`/careers/${job.slug}`} className="btn-primary whitespace-nowrap flex-shrink-0">
                Apply Now
              </Link>
            </div>
          ))}
          {data.results.length === 0 && (
            <p className="text-center text-gray-500 py-12">No open positions at this time. Check back soon!</p>
          )}
        </div>
      </div>
    </main>
  )
}

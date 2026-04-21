import { Metadata } from "next"
import Link from "next/link"
import Image from "next/image"
import { apiFetch } from "@/lib/api"
import { formatDate } from "@/lib/utils"
import type { PaginatedResponse, Post } from "@/types"

export const metadata: Metadata = { title: "Blog" }
export const revalidate = 60

export default async function BlogPage() {
  const data = await apiFetch<PaginatedResponse<Post>>("/content/posts/?page_size=12").catch(() => ({ results: [] as Post[] }))

  return (
    <main className="section">
      <div className="container-wide">
        <h1 className="text-4xl font-bold mb-2">News & Insights</h1>
        <p className="text-gray-500 dark:text-gray-400 mb-12">Latest updates from our team</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {data.results.map((post) => (
            <article key={post.id} className="card overflow-hidden group hover:shadow-md transition-shadow">
              {post.featured_image && (
                <div className="relative h-48 overflow-hidden">
                  <Image
                    src={post.featured_image}
                    alt={post.title}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
              )}
              <div className="p-6">
                {post.category && (
                  <span className="text-xs font-medium text-brand-600 dark:text-brand-400 uppercase tracking-wide">
                    {post.category.name}
                  </span>
                )}
                <h2 className="mt-2 text-lg font-semibold leading-snug line-clamp-2">
                  <Link href={`/blog/${post.slug}`} className="hover:text-brand-600 transition-colors">
                    {post.title}
                  </Link>
                </h2>
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 line-clamp-3">{post.excerpt}</p>
                <div className="mt-4 flex items-center gap-3 text-xs text-gray-400">
                  <span>{post.author_name}</span>
                  <span>·</span>
                  <span>{formatDate(post.published_at)}</span>
                  <span>·</span>
                  <span>{post.read_time} min read</span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </main>
  )
}

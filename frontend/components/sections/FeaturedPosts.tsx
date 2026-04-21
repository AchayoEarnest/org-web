import Link from "next/link"
import Image from "next/image"
import { ArrowRight } from "lucide-react"
import { formatDate } from "@/lib/utils"
import type { Post } from "@/types"

export function FeaturedPosts({ posts }: { posts: Post[] }) {
  if (!posts.length) return null
  return (
    <section className="section bg-gray-50 dark:bg-gray-900/50">
      <div className="container-wide">
        <div className="flex items-end justify-between mb-10">
          <div>
            <h2 className="text-3xl font-bold">Latest News</h2>
            <p className="mt-2 text-gray-500 dark:text-gray-400">Updates from our team</p>
          </div>
          <Link href="/blog" className="hidden sm:flex items-center gap-1 text-sm font-medium text-brand-600 hover:underline">
            View all <ArrowRight size={14} />
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {posts.map((post) => (
            <article key={post.id} className="card overflow-hidden group hover:shadow-md transition-shadow">
              {post.featured_image && (
                <div className="relative h-44 overflow-hidden">
                  <Image src={post.featured_image} alt={post.title} fill
                    className="object-cover group-hover:scale-105 transition-transform duration-300" />
                </div>
              )}
              <div className="p-5">
                <p className="text-xs text-gray-400 mb-2">{formatDate(post.published_at)}</p>
                <h3 className="font-semibold leading-snug line-clamp-2 mb-2">
                  <Link href={`/blog/${post.slug}`} className="hover:text-brand-600 transition-colors">
                    {post.title}
                  </Link>
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">{post.excerpt}</p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}

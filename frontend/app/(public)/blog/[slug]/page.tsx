import { Metadata } from "next"
import { notFound } from "next/navigation"
import Image from "next/image"
import { apiFetch }  from "@/lib/api"
import { formatDate } from "@/lib/utils"
import type { Post } from "@/types"

interface Props { params: { slug: string } }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  try {
    const post = await apiFetch<Post>(`/content/posts/${params.slug}/`)
    return {
      title:       post.meta_title || post.title,
      description: post.excerpt,
      openGraph:   { images: post.featured_image ? [post.featured_image] : [] },
    }
  } catch {
    return { title: "Post Not Found" }
  }
}

export default async function BlogPostPage({ params }: Props) {
  let post: Post
  try {
    post = await apiFetch<Post>(`/content/posts/${params.slug}/`)
  } catch {
    notFound()
  }

  return (
    <main className="section">
      <div className="container-narrow">
        <div className="mb-8">
          {post.category && (
            <span className="text-sm font-medium text-brand-600 dark:text-brand-400">
              {post.category.name}
            </span>
          )}
          <h1 className="mt-2 text-4xl font-bold leading-tight">{post.title}</h1>
          <div className="mt-4 flex items-center gap-4 text-sm text-gray-500">
            <span>By {post.author_name}</span>
            <span>·</span>
            <time>{formatDate(post.published_at)}</time>
            <span>·</span>
            <span>{post.read_time} min read</span>
          </div>
        </div>
        {post.featured_image && (
          <div className="relative h-72 sm:h-96 rounded-xl overflow-hidden mb-10">
            <Image src={post.featured_image} alt={post.title} fill className="object-cover" priority />
          </div>
        )}
        <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed mb-8">{post.excerpt}</p>
        {/* Body rendering — integrate TipTap or a JSON-to-HTML renderer here */}
        <div className="prose prose-lg dark:prose-invert max-w-none">
          <pre className="text-xs bg-gray-100 dark:bg-gray-800 p-4 rounded overflow-auto">
            {JSON.stringify(post.body, null, 2)}
          </pre>
        </div>
      </div>
    </main>
  )
}

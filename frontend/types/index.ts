export type Role = "admin" | "staff" | "member"

export interface User {
  id: string
  email: string
  full_name: string
  role: Role
  avatar?: string
  bio?: string
  phone?: string
  email_verified: boolean
  newsletter_sub: boolean
  created_at: string
}

export interface Post {
  id: string
  title: string
  slug: string
  excerpt: string
  featured_image?: string
  author_name: string
  category: Category
  tags: Tag[]
  status: "draft" | "review" | "published" | "archived"
  is_featured: boolean
  view_count: number
  read_time: number
  published_at: string
  created_at: string
  body?: Record<string, unknown>
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
}

export interface Tag {
  id: number
  name: string
  slug: string
}

export interface Event {
  id: string
  title: string
  slug: string
  description: string
  location?: string
  is_virtual: boolean
  virtual_url?: string
  start_datetime: string
  end_datetime: string
  capacity?: number
  featured_image?: string
  is_published: boolean
  is_free: boolean
  price: string
  spots_left?: number
  registration_count: number
}

export interface Job {
  id: string
  title: string
  slug: string
  department: string
  location: string
  type: "full_time" | "part_time" | "contract" | "internship" | "volunteer"
  description: string
  requirements: string
  benefits?: string
  salary_min?: number
  salary_max?: number
  is_active: boolean
  deadline?: string
  application_count: number
}

export interface Document {
  id: string
  title: string
  description?: string
  file: string
  file_size: number
  file_type: string
  access_level: "public" | "members" | "staff" | "admin"
  category_name?: string
  download_count: number
  created_at: string
}

export interface Notification {
  id: string
  title: string
  body: string
  type: "info" | "success" | "warning" | "error"
  link?: string
  is_read: boolean
  created_at: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

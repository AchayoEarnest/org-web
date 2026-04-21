import { NextAuthOptions } from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"
import GoogleProvider from "next-auth/providers/google"

const API_BASE = process.env.API_URL ?? "http://localhost:8000"

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId:     process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    CredentialsProvider({
      name: "Email & Password",
      credentials: {
        email:    { label: "Email",    type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null
        try {
          const res = await fetch(`${API_BASE}/api/v1/auth/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email:    credentials.email,
              password: credentials.password,
            }),
          })
          if (!res.ok) return null
          const data = await res.json()
          return {
            id:           data.user.id,
            email:        data.user.email,
            name:         data.user.full_name,
            image:        data.user.avatar ?? null,
            role:         data.user.role,
            accessToken:  data.tokens.access,
            refreshToken: data.tokens.refresh,
          }
        } catch {
          return null
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken  = (user as any).accessToken
        token.refreshToken = (user as any).refreshToken
        token.role         = (user as any).role
        token.userId       = user.id
      }
      return token
    },
    async session({ session, token }) {
      session.accessToken  = token.accessToken  as string
      session.user.role    = token.role         as string
      session.user.id      = token.userId       as string
      return session
    },
  },
  pages: {
    signIn: "/login",
    error:  "/login",
  },
  session:  { strategy: "jwt" },
  secret:   process.env.NEXTAUTH_SECRET,
}

// Extend next-auth types
declare module "next-auth" {
  interface Session {
    accessToken: string
    user: { id: string; role: string; email: string; name?: string; image?: string }
  }
}
declare module "next-auth/jwt" {
  interface JWT {
    accessToken:  string
    refreshToken: string
    role:         string
    userId:       string
  }
}

"use client"
import Link from "next/link"
import { motion } from "framer-motion"
import { ArrowRight, PlayCircle } from "lucide-react"

export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center bg-gradient-to-br from-brand-950 via-brand-900 to-brand-800 text-white overflow-hidden">
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{ backgroundImage: "radial-gradient(circle at 2px 2px, white 1px, transparent 0)", backgroundSize: "40px 40px" }} />
      </div>
      {/* Blobs */}
      <div className="absolute -top-24 -right-24 w-96 h-96 bg-brand-500 rounded-full blur-3xl opacity-20" />
      <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-blue-400 rounded-full blur-3xl opacity-15" />

      <div className="relative container-wide py-24 sm:py-32">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: "easeOut" }}
          className="max-w-3xl"
        >
          <motion.span
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="inline-flex items-center gap-2 text-sm font-medium bg-white/10 text-white/90 px-4 py-2 rounded-full mb-6 border border-white/20"
          >
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            Making a difference since 2010
          </motion.span>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold leading-tight mb-6">
            Empowering
            <span className="block text-brand-300">Communities</span>
            Together
          </h1>

          <p className="text-lg sm:text-xl text-white/75 leading-relaxed mb-10 max-w-2xl">
            We work at the intersection of education, technology, and community to create lasting impact for the people who need it most.
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <Link href="/about" className="btn-primary bg-white text-brand-700 hover:bg-gray-100 gap-2">
              Learn More <ArrowRight size={16} />
            </Link>
            <button className="btn-secondary border-white/30 text-white hover:bg-white/10 gap-2">
              <PlayCircle size={18} /> Watch Our Story
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

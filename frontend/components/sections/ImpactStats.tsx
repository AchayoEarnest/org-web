"use client"
import { useRef } from "react"
import { motion, useInView } from "framer-motion"

const STATS = [
  { value: "50,000+", label: "People Served",   color: "text-brand-600" },
  { value: "120+",    label: "Programs Run",     color: "text-emerald-600" },
  { value: "35",      label: "Countries Reached", color: "text-violet-600" },
  { value: "$4.2M",   label: "Funds Raised",     color: "text-amber-600" },
]

export function ImpactStats() {
  const ref    = useRef(null)
  const inView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <section className="section bg-gray-50 dark:bg-gray-900/50" ref={ref}>
      <div className="container-wide">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">Our Impact</h2>
          <p className="mt-3 text-gray-500 dark:text-gray-400">Numbers that reflect our commitment</p>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {STATS.map(({ value, label, color }, i) => (
            <motion.div
              key={label}
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className="text-center"
            >
              <div className={`text-4xl sm:text-5xl font-bold ${color}`}>{value}</div>
              <div className="mt-2 text-sm text-gray-500 dark:text-gray-400 font-medium">{label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

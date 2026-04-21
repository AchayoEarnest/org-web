import Link from "next/link"

export function CTASection() {
  return (
    <section className="section bg-brand-600">
      <div className="container-narrow text-center text-white">
        <h2 className="text-3xl sm:text-4xl font-bold mb-4">Ready to Make a Difference?</h2>
        <p className="text-brand-100 mb-8 max-w-xl mx-auto text-lg">
          Join thousands of people who are already making an impact in their communities.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/register" className="btn-primary bg-white text-brand-700 hover:bg-gray-100">
            Get Started Free
          </Link>
          <Link href="/contact" className="btn-secondary border-white/40 text-white hover:bg-white/10">
            Contact Us
          </Link>
        </div>
      </div>
    </section>
  )
}

export function Partners() {
  const partners = [
    "Partner One", "Partner Two", "Partner Three",
    "Partner Four", "Partner Five", "Partner Six",
  ]
  return (
    <section className="section border-y border-gray-100 dark:border-gray-800">
      <div className="container-wide text-center">
        <p className="text-sm font-medium text-gray-400 uppercase tracking-widest mb-8">Trusted Partners</p>
        <div className="flex flex-wrap items-center justify-center gap-10">
          {partners.map((p) => (
            <div key={p} className="text-lg font-semibold text-gray-300 dark:text-gray-600 hover:text-gray-500 dark:hover:text-gray-400 transition-colors cursor-default">
              {p}
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

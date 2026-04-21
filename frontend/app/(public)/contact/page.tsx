import { Metadata } from "next"
import { ContactForm } from "@/components/forms/ContactForm"

export const metadata: Metadata = { title: "Contact Us" }

export default function ContactPage() {
  return (
    <main className="section">
      <div className="container-narrow">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Get in Touch</h1>
          <p className="text-gray-500 dark:text-gray-400 max-w-xl mx-auto">
            Have a question or want to collaborate? We would love to hear from you.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          <ContactForm />
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">Our Office</h3>
              <p className="text-gray-500 dark:text-gray-400 text-sm leading-relaxed">
                123 Main Street, Suite 100<br />
                City, State 00000<br />
                Country
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">Email</h3>
              <a href="mailto:hello@example.com" className="text-brand-600 hover:underline text-sm">
                hello@example.com
              </a>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">Office Hours</h3>
              <p className="text-gray-500 dark:text-gray-400 text-sm">
                Monday – Friday, 9am – 5pm
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}

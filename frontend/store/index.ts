import { create } from "zustand"
import { persist } from "zustand/middleware"

interface UIStore {
  sidebarOpen:     boolean
  theme:           "light" | "dark" | "system"
  setSidebarOpen:  (v: boolean) => void
  toggleSidebar:   () => void
  setTheme:        (t: "light" | "dark" | "system") => void
}

export const useUIStore = create<UIStore>()(
  persist(
    (set) => ({
      sidebarOpen:    true,
      theme:          "system",
      setSidebarOpen: (v) => set({ sidebarOpen: v }),
      toggleSidebar:  ()  => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
      setTheme:       (t) => set({ theme: t }),
    }),
    { name: "ui-store" }
  )
)

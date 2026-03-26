"use client"

import { useState } from "react"
import { Beaker, Bot, FlaskConical, LayoutDashboard, Menu, Plus, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { navItems } from "@/features/lab-notebook/navigation"
import type { AppView } from "@/features/lab-notebook/types"
import { cn } from "@/lib/utils"

interface MobileSidebarProps {
  activeView: AppView
  onViewChange: (view: AppView | "new-experiment") => void
}

const navIcons = {
  dashboard: LayoutDashboard,
  projects: FlaskConical,
  new: Plus,
  ai: Bot,
  settings: Settings,
} as const

export function MobileSidebar({ activeView, onViewChange }: MobileSidebarProps) {
  const [open, setOpen] = useState(false)

  const handleNavClick = (id: AppView | "new-experiment") => {
    onViewChange(id)
    setOpen(false)
  }

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden" aria-label="Open navigation">
          <Menu className="h-5 w-5" />
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-64 p-0">
        <SheetHeader className="flex h-16 items-center border-b border-border px-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <Beaker className="h-4 w-4 text-primary-foreground" />
            </div>
            <SheetTitle className="font-semibold">Lab Notebook AI</SheetTitle>
          </div>
        </SheetHeader>
        <nav className="p-3">
          <ul className="space-y-1">
            {navItems.map((item) => {
              const Icon = navIcons[item.icon]

              return (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => handleNavClick(item.id)}
                    aria-current={activeView === item.id ? "page" : undefined}
                    className={cn(
                      "flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                      activeView === item.id
                        ? "bg-accent text-accent-foreground"
                        : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                    )}
                  >
                    <Icon className="h-5 w-5 shrink-0" />
                    <span>{item.label}</span>
                  </button>
                </li>
              )
            })}
          </ul>
        </nav>
      </SheetContent>
    </Sheet>
  )
}

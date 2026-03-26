"use client"

import { useState } from "react"
import Link from "next/link"
import {
  Beaker,
  Bot,
  ChevronLeft,
  ChevronRight,
  FlaskConical,
  LayoutDashboard,
  Plus,
  Settings,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { navItems } from "@/features/lab-notebook/navigation"
import type { AppView } from "@/features/lab-notebook/types"
import { cn } from "@/lib/utils"

interface SidebarProps {
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

export function Sidebar({ activeView, onViewChange }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <aside
      className={cn(
        "flex flex-col border-r border-border bg-sidebar transition-all duration-300",
        collapsed ? "w-16" : "w-64"
      )}
    >
      <div className="flex h-16 items-center justify-between border-b border-border px-4">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <Beaker className="h-4 w-4 text-primary-foreground" />
          </div>
          {!collapsed && <span className="font-semibold text-foreground">Lab Notebook AI</span>}
        </Link>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={() => setCollapsed(!collapsed)}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      </div>

      <nav className="flex-1 p-3">
        <ul className="space-y-1">
          {navItems.map((item) => {
            const Icon = navIcons[item.icon]

            return (
              <li key={item.id}>
                <button
                  type="button"
                  onClick={() => onViewChange(item.id)}
                  aria-current={activeView === item.id ? "page" : undefined}
                  className={cn(
                    "flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                    activeView === item.id
                      ? "bg-sidebar-accent text-sidebar-accent-foreground"
                      : "text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
                  )}
                >
                  <Icon className="h-5 w-5 shrink-0" />
                  {!collapsed && <span>{item.label}</span>}
                </button>
              </li>
            )
          })}
        </ul>
      </nav>

      {!collapsed && (
        <div className="border-t border-border p-4">
          <p className="text-xs text-muted-foreground">Lab Notebook AI v1.0</p>
        </div>
      )}
    </aside>
  )
}

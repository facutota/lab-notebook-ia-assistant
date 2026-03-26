"use client"

import { Activity, AlertTriangle, Bot, Clock, FlaskConical, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { ActivityItem, DashboardStat } from "@/features/lab-notebook/types"
import { StatusBadge } from "./status-badge"

interface DashboardViewProps {
  onNewProject: () => void
  onOpenAI: () => void
  stats: DashboardStat[]
  recentActivity: ActivityItem[]
}

const statIcons = {
  flask: FlaskConical,
  activity: Activity,
  alert: AlertTriangle,
} as const

export function DashboardView({ onNewProject, onOpenAI, stats, recentActivity }: DashboardViewProps) {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-foreground">Dashboard</h1>
        <p className="text-muted-foreground">Welcome back, Dr. Jane Doe</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {stats.map((stat) => {
          const Icon = statIcons[stat.icon]

          return (
            <Card key={stat.title} className="border-border/50 shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
                <div className={"rounded-lg p-2 " + stat.bgColor}>
                  <Icon className={"h-4 w-4 " + stat.color} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-foreground">{stat.value}</div>
                <p className="text-xs text-muted-foreground">{stat.description}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="border-border/50 shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg">Quick Actions</CardTitle>
            <CardDescription>Get started with common tasks</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-3 sm:grid-cols-2">
            <Button
              variant="outline"
              className="h-auto flex-col gap-2 py-6 hover:border-primary/30 hover:bg-accent"
              onClick={onNewProject}
            >
              <div className="rounded-lg bg-primary/10 p-2">
                <Plus className="h-5 w-5 text-primary" />
              </div>
              <span className="font-medium">Create Project</span>
              <span className="text-xs text-muted-foreground">Start a new research program</span>
            </Button>
            <Button
              variant="outline"
              className="h-auto flex-col gap-2 py-6 hover:border-primary/30 hover:bg-accent"
              onClick={onOpenAI}
            >
              <div className="rounded-lg bg-primary/10 p-2">
                <Bot className="h-5 w-5 text-primary" />
              </div>
              <span className="font-medium">Ask AI</span>
              <span className="text-xs text-muted-foreground">Get AI-powered insights</span>
            </Button>
          </CardContent>
        </Card>

        <Card className="border-border/50 shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg">Recent Activity</CardTitle>
            <CardDescription>Latest updates across projects and experiments</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-4">
              {recentActivity.map((activity) => (
                <li key={activity.id} className="flex items-start gap-3">
                  <div className="mt-1 rounded-full bg-secondary p-1.5">
                    <Clock className="h-3 w-3 text-muted-foreground" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-2">
                      <p className="truncate text-sm font-medium text-foreground">{activity.title}</p>
                      <StatusBadge status={activity.status} />
                    </div>
                    <p className="truncate text-xs text-muted-foreground">{activity.subtitle}</p>
                    <p className="text-xs text-muted-foreground">
                      {activity.action} • {activity.time}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

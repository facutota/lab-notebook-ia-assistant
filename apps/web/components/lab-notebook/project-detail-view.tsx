"use client"

import { ArrowLeft, Bot, Calendar, FolderOpen, FlaskConical, UserRound } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { Experiment, Project } from "@/features/lab-notebook/types"
import { StatusBadge } from "./status-badge"

interface ProjectDetailViewProps {
  project: Project
  onBack: () => void
  onOpenExperiment: (experiment: Experiment) => void
  onAnalyzeWithAI: () => void
}

export function ProjectDetailView({
  project,
  onBack,
  onOpenExperiment,
  onAnalyzeWithAI,
}: ProjectDetailViewProps) {
  const completedExperiments = project.experiments.filter((experiment) => experiment.status === "completed").length

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex items-start gap-3">
          <Button variant="ghost" size="icon" onClick={onBack} className="mt-0.5 shrink-0" aria-label="Back to projects">
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <div className="mb-1 flex items-center gap-3">
              <h1 className="text-2xl font-semibold text-foreground">{project.name}</h1>
              <StatusBadge status={project.status} />
            </div>
            <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
              <div className="flex items-center gap-1.5">
                <UserRound className="h-4 w-4" />
                <span>{project.lead}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Calendar className="h-4 w-4" />
                <span>Updated {project.updatedAt}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <FolderOpen className="h-4 w-4" />
                <span>{project.domain}</span>
              </div>
            </div>
          </div>
        </div>
        <div className="ml-10 flex gap-2 sm:ml-0">
          <Button onClick={onAnalyzeWithAI} className="gap-2">
            <Bot className="h-4 w-4" />
            Ask AI About Project
          </Button>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <Card className="border-border/50 shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg">Project Overview</CardTitle>
            <CardDescription>Program scope, focus area, and current context</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="leading-relaxed text-muted-foreground">{project.description}</p>
            <div className="flex flex-wrap gap-2">
              {project.tags.map((tag) => (
                <span key={tag} className="rounded-full border border-border bg-secondary px-3 py-1 text-xs text-secondary-foreground">
                  {tag}
                </span>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/50 shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg">Project Health</CardTitle>
            <CardDescription>Quick summary of delivery progress</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-3">
            <div className="rounded-xl border border-border bg-secondary/40 p-4">
              <p className="text-xs uppercase tracking-wide text-muted-foreground">Experiments</p>
              <p className="mt-1 text-2xl font-semibold text-foreground">{project.experiments.length}</p>
            </div>
            <div className="rounded-xl border border-border bg-secondary/40 p-4">
              <p className="text-xs uppercase tracking-wide text-muted-foreground">Completed</p>
              <p className="mt-1 text-2xl font-semibold text-foreground">{completedExperiments}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="border-border/50 shadow-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <FlaskConical className="h-5 w-5 text-primary" />
            Experiments in This Project
          </CardTitle>
          <CardDescription>Select an experiment to review notes, results, and attachments</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {project.experiments.length > 0 ? (
            project.experiments.map((experiment) => (
              <button
                key={experiment.id}
                type="button"
                onClick={() => onOpenExperiment(experiment)}
                className="flex w-full items-center justify-between rounded-xl border border-border bg-card p-4 text-left transition hover:border-primary/30 hover:shadow-sm"
              >
                <div className="min-w-0">
                  <div className="flex items-center gap-3">
                    <h3 className="truncate font-medium text-foreground">{experiment.name}</h3>
                    <StatusBadge status={experiment.status} />
                  </div>
                  <p className="mt-1 line-clamp-2 text-sm text-muted-foreground">{experiment.description}</p>
                </div>
                <span className="shrink-0 text-xs text-muted-foreground">{experiment.date}</span>
              </button>
            ))
          ) : (
            <div className="rounded-xl border border-dashed border-border bg-secondary/30 p-8 text-center">
              <p className="font-medium text-foreground">No experiments yet</p>
              <p className="mt-1 text-sm text-muted-foreground">
                This project is ready for its first experiment once the backend workflow is available.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

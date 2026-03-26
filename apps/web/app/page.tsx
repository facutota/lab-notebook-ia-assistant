"use client"

import { useMemo, useState } from "react"
import { Beaker } from "lucide-react"
import { AIAssistantView } from "@/components/lab-notebook/ai-assistant-view"
import { DashboardView } from "@/components/lab-notebook/dashboard-view"
import { ExperimentDetailView } from "@/components/lab-notebook/experiment-detail-view"
import { ExperimentsView } from "@/components/lab-notebook/experiments-view"
import { MobileSidebar } from "@/components/lab-notebook/mobile-sidebar"
import { NewExperimentModal } from "@/components/lab-notebook/new-experiment-modal"
import { ProjectDetailView } from "@/components/lab-notebook/project-detail-view"
import { SettingsView } from "@/components/lab-notebook/settings-view"
import { Sidebar } from "@/components/lab-notebook/sidebar"
import { TopBar } from "@/components/lab-notebook/top-bar"
import { buildDashboardStats, initialProjects, recentActivity } from "@/features/lab-notebook/data"
import type { AppView, Experiment, NewProjectInput, Project } from "@/features/lab-notebook/types"

export default function LabNotebookApp() {
  const [activeView, setActiveView] = useState<AppView>("dashboard")
  const [projects, setProjects] = useState<Project[]>(initialProjects)
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null)
  const [selectedExperimentId, setSelectedExperimentId] = useState<number | null>(null)
  const [showNewExperimentModal, setShowNewExperimentModal] = useState(false)

  const selectedProject = useMemo(
    () => projects.find((project) => project.id === selectedProjectId) ?? null,
    [projects, selectedProjectId]
  )
  const selectedExperiment = useMemo(
    () => selectedProject?.experiments.find((experiment) => experiment.id === selectedExperimentId) ?? null,
    [selectedProject, selectedExperimentId]
  )
  const dashboardStats = useMemo(() => buildDashboardStats(projects), [projects])

  const handleViewChange = (view: AppView | "new-experiment") => {
    if (view === "new-experiment") {
      setShowNewExperimentModal(true)
      return
    }

    setActiveView(view)
    setSelectedProjectId(null)
    setSelectedExperimentId(null)
  }

  const handleSelectProject = (project: Project) => {
    setSelectedProjectId(project.id)
    setSelectedExperimentId(null)
    setActiveView("projects")
  }

  const handleSelectExperiment = (experiment: Experiment) => {
    setSelectedExperimentId(experiment.id)
    setActiveView("projects")
  }

  const handleAnalyzeWithAI = () => {
    setActiveView("ai-assistant")
  }

  const handleCreateProject = (input: NewProjectInput) => {
    const nextProject: Project = {
      id: projects.reduce((maxId, project) => Math.max(maxId, project.id), 0) + 1,
      name: input.name,
      description: input.description,
      status: "pending",
      updatedAt: new Intl.DateTimeFormat("es-AR", {
        month: "short",
        day: "numeric",
        year: "numeric",
      }).format(new Date()),
      domain: input.domain,
      tags: input.tags.length > 0 ? input.tags : [input.domain],
      lead: "Dr. Jane Doe",
      experiments: [],
    }

    setProjects((currentProjects) => [nextProject, ...currentProjects])
    setShowNewExperimentModal(false)
    setSelectedProjectId(nextProject.id)
    setSelectedExperimentId(null)
    setActiveView("projects")
  }

  const renderContent = () => {
    if (selectedProject && selectedExperiment) {
      return (
        <ExperimentDetailView
          experiment={selectedExperiment}
          projectName={selectedProject.name}
          onBack={() => setSelectedExperimentId(null)}
          onAnalyzeWithAI={handleAnalyzeWithAI}
        />
      )
    }

    if (selectedProject) {
      return (
        <ProjectDetailView
          project={selectedProject}
          onBack={() => setSelectedProjectId(null)}
          onOpenExperiment={handleSelectExperiment}
          onAnalyzeWithAI={handleAnalyzeWithAI}
        />
      )
    }

    switch (activeView) {
      case "dashboard":
        return (
          <DashboardView
            onNewProject={() => setShowNewExperimentModal(true)}
            onOpenAI={() => setActiveView("ai-assistant")}
            stats={dashboardStats}
            recentActivity={recentActivity}
          />
        )
      case "projects":
        return <ExperimentsView projects={projects} onSelectProject={handleSelectProject} />
      case "ai-assistant":
        return <AIAssistantView />
      case "settings":
        return <SettingsView />
      default:
        return null
    }
  }

  return (
    <div className="flex h-screen bg-background">
      <div className="hidden md:block">
        <Sidebar activeView={activeView} onViewChange={handleViewChange} />
      </div>

      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex h-16 items-center justify-between border-b border-border bg-card px-4 md:hidden">
          <div className="flex items-center gap-2">
            <MobileSidebar activeView={activeView} onViewChange={handleViewChange} />
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
                <Beaker className="h-4 w-4 text-primary-foreground" />
              </div>
              <span className="font-semibold text-foreground">Lab Notebook AI</span>
            </div>
          </div>
        </header>

        <div className="hidden md:block">
          <TopBar onNewProject={() => setShowNewExperimentModal(true)} />
        </div>

        <main className="flex-1 overflow-y-auto p-4 md:p-6">{renderContent()}</main>
      </div>

      <NewExperimentModal
        open={showNewExperimentModal}
        onClose={() => setShowNewExperimentModal(false)}
        onCreate={handleCreateProject}
      />
    </div>
  )
}

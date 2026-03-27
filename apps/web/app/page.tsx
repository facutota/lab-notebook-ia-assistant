"use client"

import { useEffect, useMemo, useState } from "react"
import { Beaker } from "lucide-react"
import { AIAssistantView } from "@/components/lab-notebook/ai-assistant-view"
import { DashboardView } from "@/components/lab-notebook/dashboard-view"
import { ExperimentDetailView } from "@/components/lab-notebook/experiment-detail-view"
import { ExperimentsView } from "@/components/lab-notebook/experiments-view"
import { LoginView } from "@/components/lab-notebook/login-view"
import { MobileSidebar } from "@/components/lab-notebook/mobile-sidebar"
import { NewExperimentModal } from "@/components/lab-notebook/new-experiment-modal"
import { NewProjectModal } from "@/components/lab-notebook/new-project-modal"
import { ProjectDetailView } from "@/components/lab-notebook/project-detail-view"
import { SettingsView } from "@/components/lab-notebook/settings-view"
import { Sidebar } from "@/components/lab-notebook/sidebar"
import { TopBar } from "@/components/lab-notebook/top-bar"
import { buildDashboardStats, buildRecentActivity } from "@/features/lab-notebook/data"
import { getMyProfile, loginWithPassword, updateMyProfile } from "@/lib/auth/api"
import {
  createExperiment,
  createProject,
  listExperimentCategories,
  listExperimentsByProject,
  listProjects,
} from "@/lib/lab-notebook/api"
import type { AuthSession } from "@/lib/auth/types"
import type { AppView, Experiment, NewExperimentInput, NewProjectInput, Project } from "@/features/lab-notebook/types"

const AUTH_STORAGE_KEY = "alma-auth-session"

function buildUserName(email: string) {
  const localPart = email.split("@")[0] ?? ""
  const words = localPart
    .split(/[._-]+/)
    .map((part) => part.trim())
    .filter(Boolean)

  if (words.length === 0) {
    return email
  }

  return words.map((part) => part[0]!.toUpperCase() + part.slice(1)).join(" ")
}

function isAuthError(error: unknown) {
  if (!(error instanceof Error)) {
    return false
  }

  const message = error.message.toLowerCase()
  return message.includes("token expirado") || message.includes("401") || message.includes("unauthorized")
}

export default function LabNotebookApp() {
  const [activeView, setActiveView] = useState<AppView>("dashboard")
  const [projects, setProjects] = useState<Project[]>([])
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null)
  const [selectedExperimentId, setSelectedExperimentId] = useState<string | null>(null)
  const [showNewProjectModal, setShowNewProjectModal] = useState(false)
  const [showNewExperimentModal, setShowNewExperimentModal] = useState(false)
  const [loadingProjects, setLoadingProjects] = useState(false)
  const [projectError, setProjectError] = useState("")
  const [session, setSession] = useState<AuthSession | null>(null)

  const selectedProject = useMemo(
    () => projects.find((project) => project.id === selectedProjectId) ?? null,
    [projects, selectedProjectId]
  )
  const selectedExperiment = useMemo(
    () => selectedProject?.experiments.find((experiment) => experiment.id === selectedExperimentId) ?? null,
    [selectedProject, selectedExperimentId]
  )
  const dashboardStats = useMemo(() => buildDashboardStats(projects), [projects])
  const recentActivity = useMemo(() => buildRecentActivity(projects), [projects])

  const openNewProjectModal = () => {
    setShowNewExperimentModal(false)
    setShowNewProjectModal(true)
  }

  const openNewExperimentModal = () => {
    setShowNewProjectModal(false)
    setShowNewExperimentModal(true)
  }

  useEffect(() => {
    const storedSession = window.localStorage.getItem(AUTH_STORAGE_KEY)

    if (!storedSession) {
      return
    }

    try {
      setSession(JSON.parse(storedSession) as AuthSession)
    } catch {
      window.localStorage.removeItem(AUTH_STORAGE_KEY)
    }
  }, [])

  useEffect(() => {
    if (!session) {
      setProjects([])
      return
    }

    let cancelled = false

    const loadProjects = async () => {
      setLoadingProjects(true)
      setProjectError("")

      try {
        const nextProjects = await listProjects(session.accessToken)
        if (!cancelled) {
          setProjects(nextProjects)
        }
      } catch (error) {
        if (!cancelled) {
          if (isAuthError(error)) {
            handleSignOut()
            return
          }
          setProjectError(error instanceof Error ? error.message : "No se pudieron cargar los proyectos.")
        }
      } finally {
        if (!cancelled) {
          setLoadingProjects(false)
        }
      }
    }

    void loadProjects()

    return () => {
      cancelled = true
    }
  }, [session])

  const handleViewChange = (view: AppView | "new-experiment") => {
    if (view === "new-experiment") {
      openNewProjectModal()
      return
    }

    setActiveView(view)
    setSelectedProjectId(null)
    setSelectedExperimentId(null)
  }

  const handleSelectProject = async (project: Project) => {
    setSelectedProjectId(project.id)
    setSelectedExperimentId(null)
    setActiveView("projects")

    if (!session) {
      return
    }

    try {
      const experiments = await listExperimentsByProject(session.accessToken, project.id)
      setProjects((currentProjects) =>
        currentProjects.map((currentProject) =>
          currentProject.id === project.id ? { ...currentProject, experiments } : currentProject
        )
      )
      setProjectError("")
    } catch (error) {
      if (isAuthError(error)) {
        handleSignOut()
        return
      }
      setProjectError(error instanceof Error ? error.message : "No se pudieron cargar los experimentos.")
    }
  }

  const handleSelectExperiment = (experiment: Experiment) => {
    setSelectedExperimentId(experiment.id)
    setActiveView("projects")
  }

  const handleAnalyzeWithAI = () => {
    setActiveView("ai-assistant")
  }

  const handleLogin = async ({ email, password }: { email: string; password: string }) => {
    const tokens = await loginWithPassword(email, password)
    const nextSession: AuthSession = {
      email: email.trim(),
      ...tokens,
    }

    window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(nextSession))
    setSession(nextSession)
  }

  const handleSignOut = () => {
    window.localStorage.removeItem(AUTH_STORAGE_KEY)
    setSession(null)
    setSelectedProjectId(null)
    setSelectedExperimentId(null)
    setActiveView("dashboard")
  }

  const handleCreateProject = async (input: NewProjectInput) => {
    if (!session) {
      throw new Error("La sesión expiró. Vuelve a iniciar sesión.")
    }

    let nextProject: Project

    try {
      nextProject = await createProject(session.accessToken, input)
    } catch (error) {
      if (isAuthError(error)) {
        handleSignOut()
      }
      throw error
    }

    const hydratedProject: Project = {
      ...nextProject,
      domain: input.domain,
      tags: input.tags,
    }

    setProjects((currentProjects) => [hydratedProject, ...currentProjects])
    setShowNewProjectModal(false)
    setSelectedProjectId(hydratedProject.id)
    setSelectedExperimentId(null)
    setProjectError("")
    setActiveView("projects")
  }

  const handleCreateExperiment = async (input: NewExperimentInput) => {
    if (!session) {
      throw new Error("La sesión expiró. Vuelve a iniciar sesión.")
    }

    if (!selectedProjectId) {
      throw new Error("Seleccioná un proyecto antes de crear un experimento.")
    }

    let nextExperiment: Experiment

    try {
      nextExperiment = await createExperiment(session.accessToken, selectedProjectId, input)
    } catch (error) {
      if (isAuthError(error)) {
        handleSignOut()
      }
      throw error
    }

    setProjects((currentProjects) =>
      currentProjects.map((project) =>
        project.id === selectedProjectId
          ? { ...project, experiments: [nextExperiment, ...project.experiments], updatedAt: nextExperiment.date }
          : project
      )
    )
    setShowNewExperimentModal(false)
    setSelectedExperimentId(nextExperiment.id)
    setProjectError("")
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
          onNewExperiment={openNewExperimentModal}
        />
      )
    }

    switch (activeView) {
      case "dashboard":
        return (
          <>
            {projectError ? <p className="mb-4 text-sm text-destructive">{projectError}</p> : null}
            <DashboardView
              onNewProject={openNewProjectModal}
              onOpenAI={() => setActiveView("ai-assistant")}
              stats={dashboardStats}
              recentActivity={recentActivity}
            />
          </>
        )
      case "projects":
        return (
          <>
            {projectError ? <p className="mb-4 text-sm text-destructive">{projectError}</p> : null}
            {loadingProjects ? <p className="text-sm text-muted-foreground">Loading projects...</p> : null}
            <ExperimentsView projects={projects} onSelectProject={(project) => void handleSelectProject(project)} />
          </>
        )
      case "ai-assistant":
        return <AIAssistantView />
      case "settings":
        return (
          <SettingsView
            accessToken={session!.accessToken}
            onLoadProfile={getMyProfile}
            onSaveProfile={updateMyProfile}
            onAuthError={handleSignOut}
          />
        )
      default:
        return null
    }
  }

  if (!session) {
    return <LoginView onSubmit={handleLogin} />
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
          <TopBar
            onNewProject={openNewProjectModal}
            onSignOut={handleSignOut}
            userEmail={session.email}
            userName={buildUserName(session.email)}
          />
        </div>

        <main className="flex-1 overflow-y-auto p-4 md:p-6">{renderContent()}</main>
      </div>

      <NewProjectModal open={showNewProjectModal} onClose={() => setShowNewProjectModal(false)} onCreate={handleCreateProject} />

      <NewExperimentModal
        accessToken={session.accessToken}
        open={showNewExperimentModal}
        onClose={() => setShowNewExperimentModal(false)}
        onCreate={handleCreateExperiment}
        onLoadCategories={listExperimentCategories}
      />
    </div>
  )
}

import { getDomainApiBaseUrl } from "@/lib/auth/api"
import type {
  Experiment,
  ExperimentCategory,
  ExperimentStatus,
  NewExperimentInput,
  NewProjectInput,
  Project,
} from "@/features/lab-notebook/types"

interface DomainUser {
  nombre_completo?: string
}

interface DomainProject {
  id: string
  nombre: string
  descripcion: string
  dominio: string
  tags: string[]
  habilitado: boolean
  fecha_modificacion?: string | null
  fecha_creacion: string
  usuario?: DomainUser
}

interface DomainExperimentState {
  nombre?: string
}

interface DomainExperimentCategory {
  id: number
  nombre: string
}

interface DomainExperiment {
  id: string
  nombre: string
  descripcion: string
  habilitado?: boolean
  fecha_modificacion?: string | null
  fecha_creacion?: string
  estado_experimento?: DomainExperimentState | null
  categoria_experimento?: DomainExperimentCategory | null
}

function formatDate(value?: string | null) {
  if (!value) {
    return "Recently updated"
  }

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return "Recently updated"
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(date)
}

function mapStatus(value?: string | null, enabled = true): ExperimentStatus {
  if (!enabled) {
    return "failed"
  }

  switch ((value ?? "").trim().toLowerCase()) {
    case "completado":
    case "completed":
      return "completed"
    case "fallido":
    case "failed":
      return "failed"
    case "pendiente":
    case "pending":
      return "pending"
    default:
      return "active"
  }
}

function getAuthHeaders(accessToken: string) {
  return {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  }
}

async function parseError(response: Response) {
  try {
    const payload = (await response.json()) as { detail?: string }
    return payload.detail ?? "No se pudo completar la solicitud."
  } catch {
    return "No se pudo completar la solicitud."
  }
}

function mapProject(project: DomainProject): Project {
  return {
    id: project.id,
    name: project.nombre,
    lead: project.usuario?.nombre_completo ?? "Investigador",
    status: project.habilitado ? "active" : "failed",
    updatedAt: formatDate(project.fecha_modificacion ?? project.fecha_creacion),
    domain: project.dominio,
    tags: project.tags,
    description: project.descripcion,
    experiments: [],
  }
}

function mapExperiment(experiment: DomainExperiment): Experiment {
  return {
    id: experiment.id,
    name: experiment.nombre,
    status: mapStatus(experiment.estado_experimento?.nombre, experiment.habilitado ?? true),
    date: formatDate(experiment.fecha_modificacion ?? experiment.fecha_creacion),
    tags: experiment.categoria_experimento?.nombre ? [experiment.categoria_experimento.nombre] : [],
    description: experiment.descripcion,
  }
}

function mapExperimentCategory(category: DomainExperimentCategory): ExperimentCategory {
  return {
    id: category.id,
    name: category.nombre,
  }
}

export async function listProjects(accessToken: string): Promise<Project[]> {
  const response = await fetch(`${getDomainApiBaseUrl()}/proyectos/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  const payload = (await response.json()) as DomainProject[]
  return payload.map(mapProject)
}

export async function createProject(accessToken: string, input: NewProjectInput): Promise<Project> {
  const response = await fetch(`${getDomainApiBaseUrl()}/proyectos/`, {
    method: "POST",
    headers: getAuthHeaders(accessToken),
    body: JSON.stringify({
      nombre: input.name,
      descripcion: input.description,
      dominio: input.domain,
      tags: input.tags,
    }),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  const payload = (await response.json()) as DomainProject
  return mapProject(payload)
}

export async function listExperimentsByProject(accessToken: string, projectId: string): Promise<Experiment[]> {
  const response = await fetch(`${getDomainApiBaseUrl()}/experimentos/proyecto/${projectId}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  const payload = (await response.json()) as DomainExperiment[]
  return payload.map(mapExperiment)
}

export async function listExperimentCategories(accessToken: string): Promise<ExperimentCategory[]> {
  const response = await fetch(`${getDomainApiBaseUrl()}/experimentos/categorias`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  const payload = (await response.json()) as DomainExperimentCategory[]
  return payload.map(mapExperimentCategory)
}

export async function createExperiment(
  accessToken: string,
  projectId: string,
  input: NewExperimentInput
): Promise<Experiment> {
  const response = await fetch(`${getDomainApiBaseUrl()}/experimentos/`, {
    method: "POST",
    headers: getAuthHeaders(accessToken),
    body: JSON.stringify({
      nombre: input.name,
      descripcion: input.description,
      categoria_experimento_id: input.categoryId,
      proyecto_id: projectId,
    }),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  const payload = (await response.json()) as DomainExperiment
  return mapExperiment(payload)
}

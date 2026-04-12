import type { ChatExperimentContext, ChatResponse, ChatRequest } from "@/lib/chat/types"

const DEFAULT_ALMA_API_URL = "http://localhost:8000"

export function getChatApiBaseUrl() {
  const configuredUrl =
    process.env.NEXT_PUBLIC_ALMA_API_URL?.trim() || process.env.NEXT_PUBLIC_DOMAIN_API_URL?.trim()
  return (configuredUrl || DEFAULT_ALMA_API_URL).replace(/\/$/, "")
}

export function formatChatTimestamp() {
  return new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date())
}

function formatExperimentContext(experimentContext?: ChatExperimentContext) {
  if (!experimentContext) {
    return ""
  }

  const contextLines = [
    "Contexto del experimento:",
    `Proyecto: ${experimentContext.projectName} (${experimentContext.projectId})`,
    `Experimento: ${experimentContext.experimentName} (${experimentContext.experimentId})`,
    `Descripcion: ${experimentContext.description || "Sin descripcion"}`,
  ]

  if (experimentContext.tags.length > 0) {
    contextLines.push(`Tags: ${experimentContext.tags.join(", ")}`)
  }

  return contextLines.join("\n")
}

export function buildChatMessagePayload(
  input: string,
  attachments: File[],
  experimentContext?: ChatExperimentContext
): ChatRequest {
  const trimmedInput = input.trim() || "Analiza los archivos adjuntos y el contexto disponible."
  const formattedContext = formatExperimentContext(experimentContext)
  const message = formattedContext ? `${trimmedInput}\n\n${formattedContext}` : trimmedInput

  return {
    message,
    files: attachments.map((file) => ({
      name: file.name,
      type: file.type,
    })),
    experimentContext,
  }
}

export async function sendChatMessage(message: ChatRequest, attachments: File[] = []) {
  const hasAttachments = attachments.length > 0
  const endpoint = hasAttachments ? "/chat_upload" : "/chat"

  const response = await fetch(`${getChatApiBaseUrl()}${endpoint}`, {
    method: "POST",
    ...(hasAttachments
      ? {
          body: (() => {
            const formData = new FormData()
            formData.append("message", message.message)
            formData.append("persistence", "temporary")
            attachments.forEach((file) => {
              formData.append("files", file)
            })
            return formData
          })(),
        }
      : {
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(message),
        }),
  })

  const payload = (await response.json()) as ChatResponse

  if (!response.ok || payload.error) {
    throw new Error(payload.error ?? "The assistant could not answer right now.")
  }

  return payload
}

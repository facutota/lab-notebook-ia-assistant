import type { ChatExperimentContext, ChatResponse, ChatRequest } from "@/lib/chat/types"

const DEFAULT_ALMA_API_URL = "http://localhost:8000"

export function getChatApiBaseUrl() {
  const configuredUrl = process.env.NEXT_PUBLIC_ALMA_API_URL?.trim()
  return (configuredUrl || DEFAULT_ALMA_API_URL).replace(/\/$/, "")
}

export function formatChatTimestamp() {
  return new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date())
}

export function buildChatMessagePayload(
  input: string,
  attachments: File[],
  experimentContext?: ChatExperimentContext
): ChatRequest {
  const trimmedInput = input.trim()

  return {
    message: trimmedInput || "Analizá los archivos adjuntos y el contexto disponible.",
    files: attachments.map((file) => ({
      name: file.name,
      type: file.type,
    })),
    experimentContext,
  }
}

export async function sendChatMessage(message: ChatRequest) {
  const response = await fetch(`${getChatApiBaseUrl()}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(message),
  })

  const payload = (await response.json()) as ChatResponse

  if (!response.ok || payload.error) {
    throw new Error(payload.error ?? "The assistant could not answer right now.")
  }

  return payload
}

import type { ChatResponse } from "@/lib/chat/types"

const DEFAULT_API_URL = "http://localhost:8000"

export function getChatApiBaseUrl() {
  const configuredUrl = process.env.NEXT_PUBLIC_API_URL?.trim()
  return (configuredUrl || DEFAULT_API_URL).replace(/\/$/, "")
}

export function formatChatTimestamp() {
  return new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date())
}

export function buildChatMessagePayload(input: string, attachments: File[]) {
  const trimmedInput = input.trim()

  if (attachments.length === 0) {
    return trimmedInput
  }

  const attachmentSummary = attachments
    .map((file) => `${file.name}${file.type ? ` (${file.type})` : ""}`)
    .join(", ")

  return `${trimmedInput}\n\nAttached files: ${attachmentSummary}`
}

export async function sendChatMessage(message: string) {
  const response = await fetch(`${getChatApiBaseUrl()}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  })

  const payload = (await response.json()) as ChatResponse

  if (!response.ok || payload.error) {
    throw new Error(payload.error ?? "The assistant could not answer right now.")
  }

  return payload
}

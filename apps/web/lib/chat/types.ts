export interface ChatAttachment {
  name: string
  type: string
}

export interface ChatMessage {
  id: number
  role: "user" | "assistant"
  content: string
  timestamp: string
  attachments?: ChatAttachment[]
}

export interface ChatResponse {
  reply?: string
  error?: string
}

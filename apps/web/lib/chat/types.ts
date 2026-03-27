export interface ChatAttachment {
  name: string
  type: string
  blobUrl?: string
  fileId?: string
}

export interface ChatExperimentContext {
  experimentId: string
  experimentName: string
  projectId: string
  projectName: string
  description: string
  tags: string[]
}

export interface ChatRequest {
  message: string
  files: ChatAttachment[]
  experimentContext?: ChatExperimentContext
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

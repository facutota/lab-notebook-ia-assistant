"use client"

import { useEffect, useRef, useState } from "react"
import { Bot, LoaderCircle, Mic, Paperclip, Send, Sparkles, User, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { getSpeechRecognitionApi, getSpeechTranscript, type SpeechRecognitionInstance } from "@/lib/browser/speech-recognition"
import { buildChatMessagePayload, formatChatTimestamp, sendChatMessage } from "@/lib/chat/api"
import type { ChatMessage } from "@/lib/chat/types"
import { cn } from "@/lib/utils"

const initialMessages: ChatMessage[] = [
  {
    id: 1,
    role: "assistant",
    content:
      "Hello! I'm your Lab Notebook AI Assistant. I can help you analyze experiments, find patterns, suggest improvements, and answer questions about your research. How can I help you today?",
    timestamp: "Just now",
  },
]

const suggestedPrompts = [
  { icon: Sparkles, text: "Summarize this experiment" },
  { icon: Sparkles, text: "Find similar experiments" },
  { icon: Sparkles, text: "Suggest improvements" },
  { icon: Sparkles, text: "Analyze recent results" },
]

export function AIAssistantView() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages)
  const [input, setInput] = useState("")
  const [attachments, setAttachments] = useState<File[]>([])
  const [isSending, setIsSending] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const recognitionRef = useRef<SpeechRecognitionInstance | null>(null)
  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  const canSend = input.trim().length > 0 || attachments.length > 0

  const handleFilesSelected = (event: React.ChangeEvent<HTMLInputElement>) => {
    const nextFiles = Array.from(event.target.files ?? [])
    if (nextFiles.length === 0) {
      return
    }

    setAttachments((currentFiles) => [...currentFiles, ...nextFiles])
    event.target.value = ""
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" })
  }, [messages, isSending])

  const handleRemoveAttachment = (fileName: string) => {
    setAttachments((currentFiles) => currentFiles.filter((file) => file.name !== fileName))
  }

  const handleToggleMicrophone = () => {
    const speechRecognitionApi = getSpeechRecognitionApi()

    if (!speechRecognitionApi) {
      setError("Voice input is not available in this browser.")
      return
    }

    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop()
      setIsListening(false)
      return
    }

    setError(null)

    const recognition = new speechRecognitionApi()
    recognition.lang = "en-US"
    recognition.continuous = false
    recognition.interimResults = false

    recognition.onresult = (event) => {
      const transcript = getSpeechTranscript(event)
      setInput((currentValue) => `${currentValue}${currentValue ? " " : ""}${transcript}`.trim())
    }

    recognition.onerror = (event) => {
      setError(event.error === "not-allowed" ? "Microphone access was denied." : "Voice input failed.")
      setIsListening(false)
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognitionRef.current = recognition
    recognition.start()
    setIsListening(true)
  }

  const handleSend = async () => {
    if (!canSend || isSending) {
      return
    }

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: "user",
      content: input.trim() || "Attached files for analysis",
      timestamp: formatChatTimestamp(),
      attachments: attachments.map((file) => ({ name: file.name, type: file.type })),
    }
    const messagePayload = buildChatMessagePayload(input, attachments)

    setMessages((currentMessages) => [...currentMessages, userMessage])
    setInput("")
    setAttachments([])
    setError(null)
    setIsSending(true)

    try {
      const payload = await sendChatMessage(messagePayload)
      const assistantMessage: ChatMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: payload.reply ?? "The assistant returned an empty response.",
        timestamp: formatChatTimestamp(),
      }

      setMessages((currentMessages) => [...currentMessages, assistantMessage])
    } catch (caughtError) {
      const message = caughtError instanceof Error ? caughtError.message : "Unexpected chat error."
      setError(message)
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: `I couldn't reach the backend right now. ${message}`,
          timestamp: formatChatTimestamp(),
        },
      ])
    } finally {
      setIsSending(false)
    }
  }

  return (
    <div className="flex h-[calc(100vh-8rem)] flex-col">
      <div className="mb-4">
        <h1 className="flex items-center gap-2 text-2xl font-semibold text-foreground">
          <Bot className="h-6 w-6 text-primary" />
          AI Assistant
        </h1>
        <p className="text-muted-foreground">Get AI-powered insights about your experiments</p>
      </div>

      <Card className="flex flex-1 flex-col overflow-hidden border-border/50 shadow-sm">
        <CardContent className="flex-1 space-y-4 overflow-y-auto p-4">
          {messages.map((message) => (
            <div key={message.id} className={cn("flex gap-3", message.role === "user" && "flex-row-reverse")}>
              <div
                className={cn(
                  "flex h-8 w-8 shrink-0 items-center justify-center rounded-full",
                  message.role === "assistant"
                    ? "bg-primary text-primary-foreground"
                    : "bg-secondary text-secondary-foreground"
                )}
              >
                {message.role === "assistant" ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
              </div>
              <div
                className={cn(
                  "max-w-[80%] rounded-2xl px-4 py-3",
                  message.role === "assistant"
                    ? "bg-secondary text-secondary-foreground"
                    : "bg-primary text-primary-foreground"
                )}
              >
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                {message.attachments && message.attachments.length > 0 ? (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {message.attachments.map((attachment) => (
                      <span
                        key={`${message.id}-${attachment.name}`}
                        className={cn(
                          "rounded-full border px-2 py-1 text-[11px]",
                          message.role === "assistant"
                            ? "border-border/80 bg-background/70 text-foreground"
                            : "border-primary-foreground/30 bg-primary-foreground/10 text-primary-foreground"
                        )}
                      >
                        {attachment.name}
                      </span>
                    ))}
                  </div>
                ) : null}
                <span className="mt-1 block text-xs opacity-70">{message.timestamp}</span>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </CardContent>

        {messages.length === 1 && (
          <div className="px-4 pb-2">
            <p className="mb-2 text-xs text-muted-foreground">Suggested prompts:</p>
            <div className="flex flex-wrap gap-2">
              {suggestedPrompts.map((prompt) => (
                <Button
                  key={prompt.text}
                  variant="outline"
                  size="sm"
                  className="h-8 gap-1.5 text-xs hover:border-primary/30 hover:bg-accent"
                  onClick={() => setInput(prompt.text)}
                >
                  <prompt.icon className="h-3 w-3 text-primary" />
                  {prompt.text}
                </Button>
              ))}
            </div>
          </div>
        )}

        <div className="border-t border-border p-4">
          {attachments.length > 0 ? (
            <div className="mb-3 flex flex-wrap gap-2">
              {attachments.map((file) => (
                <span
                  key={`${file.name}-${file.lastModified}`}
                  className="inline-flex items-center gap-2 rounded-full border border-border bg-secondary px-3 py-1 text-xs text-secondary-foreground"
                >
                  {file.name}
                  <button
                    type="button"
                    className="rounded-full text-muted-foreground transition hover:text-foreground"
                    onClick={() => handleRemoveAttachment(file.name)}
                    aria-label={`Remove ${file.name}`}
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              ))}
            </div>
          ) : null}

          {attachments.length > 0 ? (
            <p className="mb-3 text-xs text-muted-foreground">
              Los archivos se adjuntan en la interfaz y hoy se envían al backend como referencia por nombre y tipo.
            </p>
          ) : null}

          {error ? <p className="mb-3 text-sm text-destructive">{error}</p> : null}

          <form
            onSubmit={(event) => {
              event.preventDefault()
              void handleSend()
            }}
            className="space-y-3"
          >
            <div className="rounded-2xl border border-border bg-secondary/60 p-2 shadow-xs">
              <Textarea
                placeholder="Ask about your experiments..."
                value={input}
                onChange={(event) => setInput(event.target.value)}
                className="min-h-24 resize-none border-0 bg-transparent px-2 py-2 shadow-none focus-visible:ring-0"
                aria-label="Ask the AI assistant"
              />
              <div className="flex items-center justify-between gap-2 border-t border-border/60 px-1 pt-2">
                <div className="flex items-center gap-2">
                  <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept="image/*,.pdf,.csv,.txt,.doc,.docx"
                    className="hidden"
                    onChange={handleFilesSelected}
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon-sm"
                    className="rounded-full"
                    onClick={() => fileInputRef.current?.click()}
                    aria-label="Attach files"
                  >
                    <Paperclip className="h-4 w-4" />
                  </Button>
                  <Button
                    type="button"
                    variant={isListening ? "default" : "ghost"}
                    size="icon-sm"
                    className="rounded-full"
                    onClick={handleToggleMicrophone}
                    aria-label={isListening ? "Stop voice input" : "Start voice input"}
                  >
                    <Mic className="h-4 w-4" />
                  </Button>
                </div>

                <Button type="submit" size="icon" disabled={!canSend || isSending} className="rounded-full">
                  {isSending ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                </Button>
              </div>
            </div>
          </form>
        </div>
      </Card>
    </div>
  )
}

declare global {
  interface Window {
    webkitSpeechRecognition?: SpeechRecognitionConstructor
    SpeechRecognition?: SpeechRecognitionConstructor
  }
}

export interface SpeechRecognitionConstructor {
  new (): SpeechRecognitionInstance
}

export interface SpeechRecognitionInstance {
  continuous: boolean
  interimResults: boolean
  lang: string
  onresult: ((event: SpeechRecognitionEventLike) => void) | null
  onerror: ((event: { error: string }) => void) | null
  onend: (() => void) | null
  start: () => void
  stop: () => void
}

export interface SpeechRecognitionEventLike {
  resultIndex: number
  results: ArrayLike<SpeechRecognitionResultLike>
}

export interface SpeechRecognitionResultLike {
  0: { transcript: string }
  isFinal: boolean
  length: number
}

export function getSpeechRecognitionApi() {
  if (typeof window === "undefined") {
    return null
  }

  return window.SpeechRecognition ?? window.webkitSpeechRecognition ?? null
}

export function getSpeechTranscript(event: SpeechRecognitionEventLike) {
  return Array.from(event.results)
    .slice(event.resultIndex)
    .map((result) => result[0].transcript)
    .join(" ")
}

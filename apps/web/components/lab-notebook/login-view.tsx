"use client"

import { type FormEvent, useState } from "react"
import { Beaker, LoaderCircle, LogIn } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"

interface LoginViewProps {
  onSubmit: (credentials: { email: string; password: string }) => Promise<void>
  onMicrosoftLogin: () => Promise<void>
}

export function LoginView({ onSubmit, onMicrosoftLogin }: LoginViewProps) {
  const [email, setEmail] = useState("admin@demo.com")
  const [password, setPassword] = useState("1a2b3c")
  const [errorMessage, setErrorMessage] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setErrorMessage("")
    setIsSubmitting(true)

    try {
      await onSubmit({ email, password })
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No se pudo iniciar sesión.")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleMicrosoftLogin = async () => {
    setErrorMessage("")
    setIsSubmitting(true)

    try {
      await onMicrosoftLogin()
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No se pudo iniciar sesión con Microsoft.")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-4 py-10">
      <Card className="w-full max-w-md">
        <CardHeader className="gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary text-primary-foreground">
              <Beaker className="h-5 w-5" />
            </div>
            <div>
              <CardTitle>Ingresar a ALMA</CardTitle>
              <CardDescription>ALMA, la solucion para gestionar y acelerar tus experimentos.</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <form className="space-y-5" onSubmit={handleSubmit}>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  id="email"
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="admin@demo.com"
                  required
                />
              </Field>

              <Field>
                <FieldLabel htmlFor="password">Contraseña</FieldLabel>
                <Input
                  id="password"
                  type="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Ingresá tu contraseña"
                  required
                />
              </Field>
            </FieldGroup>

            <FieldError>{errorMessage}</FieldError>

            <Button type="submit" className="w-full gap-2" disabled={isSubmitting}>
              {isSubmitting ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <LogIn className="h-4 w-4" />}
              {isSubmitting ? "Ingresando..." : "Iniciar sesión"}
            </Button>

            <Button type="button" variant="outline" className="w-full" disabled={isSubmitting} onClick={() => void handleMicrosoftLogin()}>
              Ingresar con Microsoft
            </Button>
          </form>
        </CardContent>
      </Card>
    </main>
  )
}

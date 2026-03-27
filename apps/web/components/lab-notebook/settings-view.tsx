"use client"

import { useEffect, useState } from "react"
import { User, Bell, Shield, Palette } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import type { UserProfile } from "@/lib/auth/types"

interface SettingsViewProps {
  accessToken: string
  onLoadProfile: (accessToken: string) => Promise<UserProfile>
  onSaveProfile: (accessToken: string, input: { firstName: string; lastName: string }) => Promise<UserProfile>
  onAuthError: () => void
}

export function SettingsView({ accessToken, onLoadProfile, onSaveProfile, onAuthError }: SettingsViewProps) {
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [email, setEmail] = useState("")
  const [loadingProfile, setLoadingProfile] = useState(true)
  const [savingProfile, setSavingProfile] = useState(false)
  const [profileError, setProfileError] = useState("")
  const [profileMessage, setProfileMessage] = useState("")

  useEffect(() => {
    let cancelled = false

    const loadProfile = async () => {
      setLoadingProfile(true)
      setProfileError("")

      try {
        const profile = await onLoadProfile(accessToken)
        if (!cancelled) {
          setFirstName(profile.firstName)
          setLastName(profile.lastName)
          setEmail(profile.email)
        }
      } catch (error) {
        if (!cancelled) {
          if (error instanceof Error && error.message.toLowerCase().includes("token expirado")) {
            onAuthError()
            return
          }
          setProfileError(error instanceof Error ? error.message : "No se pudo cargar el perfil.")
        }
      } finally {
        if (!cancelled) {
          setLoadingProfile(false)
        }
      }
    }

    void loadProfile()

    return () => {
      cancelled = true
    }
  }, [accessToken, onLoadProfile])

  const handleSaveProfile = async () => {
    setSavingProfile(true)
    setProfileError("")
    setProfileMessage("")

    try {
      const profile = await onSaveProfile(accessToken, { firstName, lastName })
      setFirstName(profile.firstName)
      setLastName(profile.lastName)
      setEmail(profile.email)
      setProfileMessage("Perfil actualizado.")
    } catch (error) {
      if (error instanceof Error && error.message.toLowerCase().includes("token expirado")) {
        onAuthError()
        return
      }
      setProfileError(error instanceof Error ? error.message : "No se pudo guardar el perfil.")
    } finally {
      setSavingProfile(false)
    }
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-2xl font-semibold text-foreground">Settings</h1>
        <p className="text-muted-foreground">Manage your account and preferences</p>
      </div>

      <Card className="border-border/50 shadow-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <User className="h-5 w-5 text-primary" />
            Profile
          </CardTitle>
          <CardDescription>Manage your personal information</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {profileError ? <p className="text-sm text-destructive">{profileError}</p> : null}
          {profileMessage ? <p className="text-sm text-primary">{profileMessage}</p> : null}
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="firstName">First Name</Label>
              <Input id="firstName" value={firstName} onChange={(event) => setFirstName(event.target.value)} disabled={loadingProfile || savingProfile} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="lastName">Last Name</Label>
              <Input id="lastName" value={lastName} onChange={(event) => setLastName(event.target.value)} disabled={loadingProfile || savingProfile} />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" value={email} readOnly disabled />
          </div>
          <Button onClick={() => void handleSaveProfile()} disabled={loadingProfile || savingProfile}>
            {savingProfile ? "Saving..." : "Save Changes"}
          </Button>
        </CardContent>
      </Card>

      <Card className="border-border/50 shadow-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Bell className="h-5 w-5 text-primary" />
            Notifications
          </CardTitle>
          <CardDescription>Configure how you receive updates</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Email Notifications</Label>
              <p className="text-sm text-muted-foreground">
                Receive updates about your experiments via email
              </p>
            </div>
            <Switch defaultChecked />
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>AI Analysis Alerts</Label>
              <p className="text-sm text-muted-foreground">
                Get notified when AI analysis is complete
              </p>
            </div>
            <Switch defaultChecked />
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Weekly Digest</Label>
              <p className="text-sm text-muted-foreground">
                Receive a weekly summary of your research activity
              </p>
            </div>
            <Switch />
          </div>
        </CardContent>
      </Card>

      <Card className="border-border/50 shadow-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Shield className="h-5 w-5 text-primary" />
            Security
          </CardTitle>
          <CardDescription>Manage your account security</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Two-Factor Authentication</Label>
              <p className="text-sm text-muted-foreground">
                Add an extra layer of security to your account
              </p>
            </div>
            <Button variant="outline" size="sm">
              Enable
            </Button>
          </div>
          <Separator />
          <div className="space-y-2">
            <Label>Change Password</Label>
            <div className="flex gap-2">
              <Input type="password" placeholder="Current password" className="flex-1" />
              <Button variant="outline">Update</Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="border-border/50 shadow-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Palette className="h-5 w-5 text-primary" />
            Appearance
          </CardTitle>
          <CardDescription>Customize the look and feel</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Compact Mode</Label>
              <p className="text-sm text-muted-foreground">
                Use smaller spacing for a denser interface
              </p>
            </div>
            <Switch />
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Show Experiment Previews</Label>
              <p className="text-sm text-muted-foreground">
                Display preview cards inside each project workspace
              </p>
            </div>
            <Switch defaultChecked />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

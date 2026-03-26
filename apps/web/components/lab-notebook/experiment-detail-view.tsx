"use client"

import {
  ArrowLeft,
  Bot,
  Calendar,
  ChartBar,
  Clock,
  Edit,
  FileText,
  Paperclip,
  Tag,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getExperimentAttachments, getExperimentTimeline } from "@/features/lab-notebook/data"
import type { Experiment } from "@/features/lab-notebook/types"
import { StatusBadge } from "./status-badge"

interface ExperimentDetailViewProps {
  experiment: Experiment
  projectName: string
  onBack: () => void
  onAnalyzeWithAI: () => void
}

export function ExperimentDetailView({
  experiment,
  projectName,
  onBack,
  onAnalyzeWithAI,
}: ExperimentDetailViewProps) {
  const experimentAttachments = getExperimentAttachments(experiment)
  const experimentTimeline = getExperimentTimeline(experiment)

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex items-start gap-3">
          <Button
            variant="ghost"
            size="icon"
            onClick={onBack}
            className="mt-0.5 shrink-0"
            aria-label="Back to experiments"
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <div className="mb-1 flex items-center gap-3">
              <h1 className="text-2xl font-semibold text-foreground">{experiment.name}</h1>
              <StatusBadge status={experiment.status} />
            </div>
            <p className="mb-3 text-sm text-muted-foreground">Project: {projectName}</p>
            <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
              <div className="flex items-center gap-1.5">
                <Calendar className="h-4 w-4" />
                <span>{experiment.date}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Tag className="h-4 w-4" />
                <span>{experiment.tags.join(", ")}</span>
              </div>
            </div>
          </div>
        </div>
        <div className="ml-10 flex gap-2 sm:ml-0">
          <Button variant="outline" className="gap-2">
            <Edit className="h-4 w-4" />
            Edit
          </Button>
          <Button onClick={onAnalyzeWithAI} className="gap-2">
            <Bot className="h-4 w-4" />
            Analyze with AI
          </Button>
        </div>
      </div>

      <Tabs defaultValue="notes" className="w-full">
        <TabsList className="w-full justify-start bg-secondary">
          <TabsTrigger value="notes" className="gap-2">
            <FileText className="h-4 w-4" />
            Notes
          </TabsTrigger>
          <TabsTrigger value="results" className="gap-2">
            <ChartBar className="h-4 w-4" />
            Results
          </TabsTrigger>
          <TabsTrigger value="attachments" className="gap-2">
            <Paperclip className="h-4 w-4" />
            Attachments
          </TabsTrigger>
        </TabsList>

        <TabsContent value="notes" className="mt-4">
          <Card className="border-border/50 shadow-sm">
            <CardContent className="p-6">
              <div className="prose prose-sm max-w-none">
                <h3 className="mb-3 text-lg font-semibold text-foreground">Experiment Overview</h3>
                <p className="mb-4 leading-relaxed text-muted-foreground">{experiment.description}</p>

                <h4 className="mb-2 text-base font-semibold text-foreground">Objectives</h4>
                <ul className="mb-4 list-inside list-disc space-y-1 text-muted-foreground">
                  <li>Determine baseline measurements</li>
                  <li>Analyze response under controlled conditions</li>
                  <li>Compare results with theoretical predictions</li>
                  <li>Document any anomalies or unexpected behaviors</li>
                </ul>

                <h4 className="mb-2 text-base font-semibold text-foreground">Methodology</h4>
                <p className="mb-4 leading-relaxed text-muted-foreground">
                  Standard laboratory protocols were followed with modifications for temperature control.
                  Samples were collected at 30-minute intervals over a 24-hour period. All measurements
                  were taken in triplicate to ensure statistical significance.
                </p>

                <h4 className="mb-2 text-base font-semibold text-foreground">Observations</h4>
                <p className="leading-relaxed text-muted-foreground">
                  Initial results show promising trends. Further analysis is required to draw definitive
                  conclusions. The AI assistant has identified several patterns worth investigating further.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="results" className="mt-4">
          <Card className="border-border/50 shadow-sm">
            <CardContent className="p-6">
              <div className="flex flex-col items-center justify-center py-12">
                <div className="mb-4 rounded-full bg-primary/10 p-4">
                  <ChartBar className="h-8 w-8 text-primary" />
                </div>
                <h3 className="mb-1 text-lg font-medium text-foreground">Results Visualization</h3>
                <p className="max-w-md text-center text-sm text-muted-foreground">
                  Charts and data visualizations will be displayed here once the experiment data is fully
                  processed.
                </p>
                <Button variant="outline" className="mt-4">Upload Results Data</Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="attachments" className="mt-4">
          <Card className="border-border/50 shadow-sm">
            <CardHeader>
              <CardTitle className="text-lg">Attached Files</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {experimentAttachments.map((file) => (
                  <li
                    key={file.name}
                    className="flex items-center justify-between rounded-lg border border-border bg-secondary/50 p-3"
                  >
                    <div className="flex items-center gap-3">
                      <div className="rounded-lg bg-primary/10 p-2">
                        <FileText className="h-4 w-4 text-primary" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-foreground">{file.name}</p>
                        <p className="text-xs text-muted-foreground">{file.size}</p>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm">Download</Button>
                  </li>
                ))}
              </ul>
              <Button variant="outline" className="mt-4 w-full gap-2">
                <Paperclip className="h-4 w-4" />
                Add Attachment
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <Card className="border-border/50 shadow-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Clock className="h-5 w-5 text-primary" />
            Activity Timeline
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="relative">
            <div className="absolute bottom-0 left-3 top-0 w-px bg-border" />
            <ul className="space-y-4">
              {experimentTimeline.map((item, index) => (
                <li key={item.id} className="relative flex gap-4 pl-8">
                  <div
                    className={
                      "absolute left-0 top-1.5 flex h-6 w-6 items-center justify-center rounded-full border-2 border-background " +
                      (index === 0 ? "bg-primary" : "bg-secondary")
                    }
                  >
                    <div
                      className={
                        "h-2 w-2 rounded-full " +
                        (index === 0 ? "bg-primary-foreground" : "bg-muted-foreground")
                      }
                    />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-foreground">{item.action}</p>
                    <p className="text-xs text-muted-foreground">{item.time} • {item.user}</p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

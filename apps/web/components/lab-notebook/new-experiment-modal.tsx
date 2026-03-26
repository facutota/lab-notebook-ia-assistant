"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm, useWatch } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import type { NewProjectInput } from "@/features/lab-notebook/types"

interface NewExperimentModalProps {
  open: boolean
  onClose: () => void
  onCreate: (input: NewProjectInput) => void
}

const newExperimentSchema = z.object({
  name: z.string().trim().min(1, "Project name is required"),
  description: z.string().trim().min(1, "Description is required"),
  category: z.string().trim().min(1, "Domain is required"),
  tags: z.string().trim(),
})

type NewExperimentFormValues = z.infer<typeof newExperimentSchema>

export function NewExperimentModal({ open, onClose, onCreate }: NewExperimentModalProps) {
  const {
    control,
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<NewExperimentFormValues>({
    resolver: zodResolver(newExperimentSchema),
    defaultValues: {
      name: "",
      description: "",
      category: "",
      tags: "",
    },
  })

  const selectedCategory = useWatch({ control, name: "category" })

  const handleCreate = (values: NewExperimentFormValues) => {
    onCreate({
      name: values.name.trim(),
      description: values.description.trim(),
      domain: values.category,
      tags: values.tags
        .split(",")
        .map((tag) => tag.trim())
        .filter(Boolean),
    })
    reset()
  }

  const handleOpenChange = (nextOpen: boolean) => {
    if (nextOpen === false) {
      reset()
      onClose()
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Create New Project</DialogTitle>
          <DialogDescription>
            Set up a new project to organize related experiments under one research goal.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(handleCreate)} className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="name">Project Name</Label>
            <Input id="name" placeholder="e.g., Stem Cell Response Program" aria-invalid={Boolean(errors.name)} {...register("name")} />
            {errors.name ? <p className="text-sm text-destructive">{errors.name.message}</p> : null}
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Research Objective</Label>
            <Textarea
              id="description"
              placeholder="Describe the project scope, hypotheses, and expected outcomes..."
              rows={4}
              aria-invalid={Boolean(errors.description)}
              {...register("description")}
            />
            {errors.description ? <p className="text-sm text-destructive">{errors.description.message}</p> : null}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="category">Domain</Label>
              <Select
                value={selectedCategory}
                onValueChange={(value) =>
                  setValue("category", value, { shouldDirty: true, shouldValidate: true })
                }
              >
                <SelectTrigger id="category">
                  <SelectValue placeholder="Select domain" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="genetics">Genetics</SelectItem>
                  <SelectItem value="biochemistry">Biochemistry</SelectItem>
                  <SelectItem value="microbiology">Microbiology</SelectItem>
                  <SelectItem value="pharmacology">Pharmacology</SelectItem>
                  <SelectItem value="cell-biology">Cell Biology</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
              {errors.category ? <p className="text-sm text-destructive">{errors.category.message}</p> : null}
            </div>

            <div className="space-y-2">
              <Label htmlFor="tags">Tags</Label>
              <Input id="tags" placeholder="e.g., RNA, PCR" {...register("tags")} />
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" type="button" onClick={() => handleOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              Create Project
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

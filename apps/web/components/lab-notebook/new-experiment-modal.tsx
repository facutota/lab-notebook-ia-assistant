"use client"

import { useEffect, useState } from "react"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
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
import type { ExperimentCategory, NewExperimentInput } from "@/features/lab-notebook/types"

interface NewExperimentModalProps {
  accessToken: string
  open: boolean
  onClose: () => void
  onCreate: (input: NewExperimentInput) => Promise<void>
  onLoadCategories: (accessToken: string) => Promise<ExperimentCategory[]>
}

const newExperimentSchema = z.object({
  name: z.string().trim().min(1, "Experiment name is required"),
  description: z.string().trim().min(1, "Description is required"),
  categoryId: z.string().trim().min(1, "Category is required"),
})

type NewExperimentFormValues = z.infer<typeof newExperimentSchema>

export function NewExperimentModal({
  accessToken,
  open,
  onClose,
  onCreate,
  onLoadCategories,
}: NewExperimentModalProps) {
  const [categories, setCategories] = useState<ExperimentCategory[]>([])
  const [categoriesError, setCategoriesError] = useState("")

  const {
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
      categoryId: "",
    },
  })

  useEffect(() => {
    if (!open) {
      return
    }

    let cancelled = false

    const loadCategories = async () => {
      try {
        setCategoriesError("")
        const nextCategories = await onLoadCategories(accessToken)
        if (!cancelled) {
          setCategories(nextCategories)
        }
      } catch (error) {
        if (!cancelled) {
          setCategories([])
          setCategoriesError(error instanceof Error ? error.message : "Could not load categories.")
        }
      }
    }

    void loadCategories()

    return () => {
      cancelled = true
    }
  }, [accessToken, onLoadCategories, open])

  const handleCreate = async (values: NewExperimentFormValues) => {
    await onCreate({
      name: values.name.trim(),
      description: values.description.trim(),
      categoryId: Number(values.categoryId),
    })
    reset()
  }

  const handleOpenChange = (nextOpen: boolean) => {
    if (nextOpen === false) {
      reset()
      setCategoriesError("")
      onClose()
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>New Experiment</DialogTitle>
          <DialogDescription>
            Complete the experiment details for this project.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(handleCreate)} className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="name">Experiment Name</Label>
            <Input id="name" placeholder="e.g., PCR Validation Run 01" aria-invalid={Boolean(errors.name)} {...register("name")} />
            {errors.name ? <p className="text-sm text-destructive">{errors.name.message}</p> : null}
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Experiment Description</Label>
            <Textarea
              id="description"
              placeholder="Describe the goal, protocol, or expected outcome..."
              rows={4}
              aria-invalid={Boolean(errors.description)}
              {...register("description")}
            />
            {errors.description ? <p className="text-sm text-destructive">{errors.description.message}</p> : null}
          </div>

          <div className="space-y-2">
            <Label htmlFor="categoryId">Experiment Category</Label>
            <Select onValueChange={(value) => setValue("categoryId", value, { shouldDirty: true, shouldValidate: true })}>
              <SelectTrigger id="categoryId" aria-invalid={Boolean(errors.categoryId)}>
                <SelectValue placeholder="Select experiment category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((category) => (
                  <SelectItem key={category.id} value={String(category.id)}>
                    {category.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {errors.categoryId ? <p className="text-sm text-destructive">{errors.categoryId.message}</p> : null}
            {categoriesError ? <p className="text-sm text-destructive">{categoriesError}</p> : null}
          </div>

          <DialogFooter>
            <Button variant="outline" type="button" onClick={() => handleOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting || categories.length === 0}>
              Save Experiment
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

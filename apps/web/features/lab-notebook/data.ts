import type {
  ActivityItem,
  Attachment,
  DashboardStat,
  Experiment,
  Project,
  TimelineEvent,
} from "@/features/lab-notebook/types"

export const initialProjects: Project[] = [
  {
    id: 1,
    name: "Stem Cell Response Program",
    lead: "Dr. Jane Doe",
    status: "active",
    updatedAt: "Mar 15, 2024",
    domain: "Genetics",
    tags: ["RNA", "Stem Cells", "Transcriptomics"],
    description: "Longitudinal project focused on how stem cells respond to nutrient and stress changes.",
    experiments: [
      {
        id: 101,
        name: "Gene Expression Analysis",
        status: "completed",
        date: "Mar 15, 2024",
        tags: ["Genetics", "RNA"],
        description: "Analyzing gene expression patterns in stem cells under various conditions.",
      },
      {
        id: 102,
        name: "Cell Culture Growth",
        status: "active",
        date: "Mar 12, 2024",
        tags: ["Cell Biology", "Growth"],
        description: "Monitoring cell culture growth rates under different nutrient conditions.",
      },
    ],
  },
  {
    id: 2,
    name: "Protein Behavior Initiative",
    lead: "Dr. Emily Carter",
    status: "active",
    updatedAt: "Mar 14, 2024",
    domain: "Biochemistry",
    tags: ["Proteins", "Simulation", "Enzymes"],
    description: "Program exploring protein folding and enzyme kinetics across simulated and wet-lab setups.",
    experiments: [
      {
        id: 201,
        name: "Protein Folding Simulation",
        status: "active",
        date: "Mar 14, 2024",
        tags: ["Proteins", "Simulation"],
        description: "Simulating protein folding dynamics using molecular dynamics.",
      },
      {
        id: 202,
        name: "Enzyme Kinetics Study",
        status: "pending",
        date: "Mar 8, 2024",
        tags: ["Biochemistry", "Enzymes"],
        description: "Studying enzyme kinetics and reaction rates.",
      },
    ],
  },
  {
    id: 3,
    name: "Resistance and Safety Validation",
    lead: "Dr. Miguel Alvarez",
    status: "failed",
    updatedAt: "Mar 10, 2024",
    domain: "Microbiology",
    tags: ["Antibiotics", "Screening", "Pharmacology"],
    description: "Project validating bacterial resistance profiles and drug interaction safety envelopes.",
    experiments: [
      {
        id: 301,
        name: "Drug Interaction Test",
        status: "failed",
        date: "Mar 10, 2024",
        tags: ["Pharmacology", "Testing"],
        description: "Testing drug interactions between compound A and compound B.",
      },
      {
        id: 302,
        name: "Bacterial Resistance Analysis",
        status: "completed",
        date: "Mar 5, 2024",
        tags: ["Microbiology", "Antibiotics"],
        description: "Analyzing antibiotic resistance patterns in bacterial cultures.",
      },
    ],
  },
]

export const recentActivity: ActivityItem[] = [
  {
    id: 1,
    title: "Stem Cell Response Program",
    subtitle: "Gene Expression Analysis",
    action: "Results updated",
    time: "2 hours ago",
    status: "completed",
  },
  {
    id: 2,
    title: "Protein Behavior Initiative",
    subtitle: "Protein Folding Simulation",
    action: "AI analysis requested",
    time: "4 hours ago",
    status: "active",
  },
  {
    id: 3,
    title: "Stem Cell Response Program",
    subtitle: "Cell Culture Growth",
    action: "New notes added",
    time: "Yesterday",
    status: "active",
  },
  {
    id: 4,
    title: "Resistance and Safety Validation",
    subtitle: "Drug Interaction Test",
    action: "Experiment failed",
    time: "2 days ago",
    status: "failed",
  },
]

export function flattenExperiments(projects: Project[]): Experiment[] {
  return projects.flatMap((project) => project.experiments)
}

export function buildDashboardStats(projects: Project[]): DashboardStat[] {
  const experiments = flattenExperiments(projects)
  const activeProjects = projects.filter((project) => project.status === "active").length
  const totalExperiments = experiments.length
  const activeExperiments = experiments.filter((experiment) => experiment.status === "active").length
  const failedExperiments = experiments.filter((experiment) => experiment.status === "failed").length

  return [
    {
      title: "Active Projects",
      value: String(activeProjects),
      description: String(projects.length) + " total programs",
      icon: "flask",
      color: "text-primary",
      bgColor: "bg-primary/10",
    },
    {
      title: "Running Experiments",
      value: String(activeExperiments),
      description: String(totalExperiments) + " tracked across projects",
      icon: "activity",
      color: "text-success",
      bgColor: "bg-success/10",
    },
    {
      title: "Experiments at Risk",
      value: String(failedExperiments),
      description: failedExperiments > 0 ? "Require follow-up review" : "No incidents",
      icon: "alert",
      color: "text-destructive",
      bgColor: "bg-destructive/10",
    },
  ]
}

export function getExperimentTimeline(experiment: Experiment): TimelineEvent[] {
  return [
    {
      id: 1,
      action: "Experiment created",
      time: `${experiment.date} - 09:00 AM`,
      user: "Dr. Jane Doe",
    },
    {
      id: 2,
      action: "Protocol reviewed",
      time: `${experiment.date} - 11:30 AM`,
      user: "Lab Assistant",
    },
    {
      id: 3,
      action: "Analysis started",
      time: `${experiment.date} - 02:00 PM`,
      user: "AI Assistant",
    },
  ]
}

export function getExperimentAttachments(experiment: Experiment): Attachment[] {
  const baseName = experiment.name.toLowerCase().replace(/\s+/g, "-")

  return [
    { name: `${baseName}-raw-data.csv`, size: "2.4 MB" },
    { name: `${baseName}-protocol.pdf`, size: "1.1 MB" },
    { name: `${baseName}-figures.zip`, size: "18.6 MB" },
  ]
}

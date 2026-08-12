export type Language = "en" | "zh";

export type Command =
  | { kind: "help" }
  | { kind: "task"; goal: string }
  | { kind: "quick"; goal: string }
  | { kind: "queue" }
  | { kind: "status"; issue: number }
  | { kind: "assign"; issue: number; agentId: string };

export interface TaskSummary {
  number: number;
  title: string;
  url: string;
  state: string;
  labels: string[];
}

export interface GitHubPort {
  createTask(goal: string): Promise<TaskSummary>;
  listQueue(): Promise<TaskSummary[]>;
  getTask(issue: number): Promise<TaskSummary>;
  assign(issue: number, agentId: string): Promise<TaskSummary>;
}

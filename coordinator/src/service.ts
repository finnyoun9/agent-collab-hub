import type { Command, GitHubPort, Language, TaskSummary } from "./types.js";

function labels(task: TaskSummary): string {
  return task.labels.length ? task.labels.join(", ") : "-";
}

export class CoordinatorService {
  constructor(
    private readonly github: GitHubPort,
    private readonly lang: Language,
  ) {}

  async execute(command: Command): Promise<string> {
    switch (command.kind) {
      case "help":
        return this.lang === "zh"
          ? [
              "Agent Hub 已连接。",
              "/task <目标> 创建任务",
              "/quick <目标> 创建并分配给 bench-workbuddy",
              "/queue 查看队列",
              "/status <编号> 查看状态",
              "/assign <编号> <agent-id> 分配任务",
            ].join("\n")
          : [
              "Agent Hub is connected.",
              "/task <goal> create a task",
              "/quick <goal> create and assign to bench-workbuddy",
              "/queue list the queue",
              "/status <number> show status",
              "/assign <number> <agent-id> assign a task",
            ].join("\n");
      case "task": {
        const task = await this.github.createTask(command.goal);
        return this.renderTask(this.lang === "zh" ? "任务已创建" : "Task created", task);
      }
      case "quick": {
        const task = await this.github.createTask(command.goal);
        const assigned = await this.github.assign(task.number, "bench-workbuddy");
        return this.renderTask(
          this.lang === "zh"
            ? "快速任务已创建并分配给 bench-workbuddy"
            : "Quick task created and assigned to bench-workbuddy",
          assigned,
        );
      }
      case "queue": {
        const tasks = await this.github.listQueue();
        if (!tasks.length) return this.lang === "zh" ? "当前没有开放任务。" : "No open tasks.";
        return tasks.map((task) => this.renderTask("", task)).join("\n\n");
      }
      case "status":
        return this.renderTask(
          this.lang === "zh" ? "任务状态" : "Task status",
          await this.github.getTask(command.issue),
        );
      case "assign":
        return this.renderTask(
          this.lang === "zh" ? `已分配给 ${command.agentId}` : `Assigned to ${command.agentId}`,
          await this.github.assign(command.issue, command.agentId),
        );
    }
  }

  private renderTask(prefix: string, task: TaskSummary): string {
    const parts = [prefix, `#${task.number} ${task.title}`, labels(task), task.url];
    return parts.filter(Boolean).join("\n");
  }
}

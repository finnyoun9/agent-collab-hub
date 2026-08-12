import { execFile } from "node:child_process";
import { promisify } from "node:util";
import type { GitHubPort, TaskSummary } from "./types.js";

const execFileAsync = promisify(execFile);
const AGENTS = new Set([
  "bench-codex",
  "bench-workbuddy",
  "mac-claude-client",
  "mac-claude-vscode",
]);

interface GhIssue {
  number: number;
  title: string;
  url: string;
  state: string;
  labels: Array<{ name: string }>;
}

function taskSummary(issue: GhIssue): TaskSummary {
  return {
    number: issue.number,
    title: issue.title,
    url: issue.url,
    state: issue.state,
    labels: issue.labels.map((label) => label.name),
  };
}

export class GhCliGitHub implements GitHubPort {
  constructor(
    private readonly repo: string,
    private readonly ghPath = "gh",
  ) {}

  private async gh(args: string[]): Promise<string> {
    const { stdout } = await execFileAsync(this.ghPath, args, {
      encoding: "utf8",
      windowsHide: true,
      maxBuffer: 1024 * 1024,
    });
    return stdout.trim();
  }

  async createTask(goal: string): Promise<TaskSummary> {
    const body = [
      "## Goal / 目标",
      "",
      goal,
      "",
      "## Source / 来源",
      "",
      "Created from the dedicated Feishu group / 由飞书专项群创建",
      "",
      "## Acceptance criteria / 验收标准",
      "",
      "To be refined during triage / 在分流阶段补充",
    ].join("\n");
    const url = await this.gh([
      "issue",
      "create",
      "--repo",
      this.repo,
      "--title",
      `[Task/任务]: ${goal.slice(0, 80)}`,
      "--body",
      body,
      "--label",
      "state:triage",
    ]);
    const number = Number(url.match(/\/(\d+)$/u)?.[1]);
    if (!number) throw new Error(`Cannot parse issue number from ${url}`);
    return this.getTask(number);
  }

  async listQueue(): Promise<TaskSummary[]> {
    const output = await this.gh([
      "issue",
      "list",
      "--repo",
      this.repo,
      "--state",
      "open",
      "--limit",
      "20",
      "--json",
      "number,title,url,state,labels",
    ]);
    return (JSON.parse(output) as GhIssue[]).map(taskSummary);
  }

  async getTask(issue: number): Promise<TaskSummary> {
    const output = await this.gh([
      "issue",
      "view",
      String(issue),
      "--repo",
      this.repo,
      "--json",
      "number,title,url,state,labels",
    ]);
    return taskSummary(JSON.parse(output) as GhIssue);
  }

  async assign(issue: number, agentId: string): Promise<TaskSummary> {
    if (!AGENTS.has(agentId)) throw new Error(`Unknown agent: ${agentId}`);
    const current = await this.getTask(issue);
    const oldLabels = current.labels.filter(
      (label) => label.startsWith("agent:") || label.startsWith("state:"),
    );
    const editArgs = [
      "issue",
      "edit",
      String(issue),
      "--repo",
      this.repo,
      "--add-label",
      `agent:${agentId}`,
      "--add-label",
      "state:ready",
    ];
    for (const label of oldLabels) editArgs.push("--remove-label", label);
    await this.gh(editArgs);
    await this.gh([
      "issue",
      "comment",
      String(issue),
      "--repo",
      this.repo,
      "--body",
      `ASSIGNED\nAgent: ${agentId}\nSource: Feishu coordinator`,
    ]);
    return this.getTask(issue);
  }
}

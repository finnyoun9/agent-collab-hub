import { describe, expect, it } from "vitest";
import { CoordinatorService } from "./service.js";
import type { GitHubPort, TaskSummary } from "./types.js";

const task: TaskSummary = {
  number: 7,
  title: "[Task/任务]: UART DMA",
  url: "https://example.test/issues/7",
  state: "OPEN",
  labels: ["state:triage"],
};

const github: GitHubPort = {
  createTask: async () => task,
  listQueue: async () => [task],
  getTask: async () => task,
  assign: async () => ({ ...task, labels: ["state:ready", "agent:bench-opencode"] }),
};

describe("CoordinatorService", () => {
  it("renders Chinese task creation", async () => {
    const service = new CoordinatorService(github, "zh");
    await expect(service.execute({ kind: "task", goal: "UART DMA" })).resolves.toContain(
      "任务已创建",
    );
  });

  it("renders the queue", async () => {
    const service = new CoordinatorService(github, "en");
    await expect(service.execute({ kind: "queue" })).resolves.toContain("#7");
  });

  it("creates and assigns a quick task to the configured default worker", async () => {
    const service = new CoordinatorService(github, "zh");
    await expect(service.execute({ kind: "quick", goal: "修正文档链接" })).resolves.toContain(
      "bench-opencode",
    );
  });
});

import type { Command } from "./types.js";

function normalizedText(value: string): string {
  const text = value
    .replace(/<at\b[^>]*>.*?<\/at>/giu, " ")
    .replace(/@_user_\d+/gu, " ")
    .replace(/\s+/gu, " ")
    .trim();
  return text.replace(/^@\S+\s+(?=\/)/u, "");
}

export function parseCommand(input: string): Command {
  const text = normalizedText(input);
  if (!text || text === "/help" || text === "帮助") return { kind: "help" };
  if (text === "/queue" || text === "队列") return { kind: "queue" };

  const task = text.match(/^\/task\s+(.+)$/iu);
  if (task?.[1]) return { kind: "task", goal: task[1].trim() };

  const quick = text.match(/^\/quick\s+(.+)$/iu);
  if (quick?.[1]) return { kind: "quick", goal: quick[1].trim() };

  const status = text.match(/^\/status\s+#?(\d+)$/iu);
  if (status?.[1]) return { kind: "status", issue: Number(status[1]) };

  const assign = text.match(/^\/assign\s+#?(\d+)\s+([a-z0-9-]+)$/iu);
  if (assign?.[1] && assign[2]) {
    return { kind: "assign", issue: Number(assign[1]), agentId: assign[2] };
  }

  return { kind: "task", goal: text };
}

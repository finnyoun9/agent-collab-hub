import { describe, expect, it } from "vitest";
import { parseCommand } from "./commands.js";

describe("parseCommand", () => {
  it("parses task commands", () => {
    expect(parseCommand("/task 实现 UART DMA")).toEqual({
      kind: "task",
      goal: "实现 UART DMA",
    });
  });

  it("parses assignment", () => {
    expect(parseCommand("/assign #12 bench-workbuddy")).toEqual({
      kind: "assign",
      issue: 12,
      agentId: "bench-workbuddy",
    });
  });

  it("removes Feishu mention markup", () => {
    expect(parseCommand("<at user_id=\"x\">Agent Hub</at> /queue")).toEqual({
      kind: "queue",
    });
  });

  it("removes a plain-text Feishu mention before a command", () => {
    expect(parseCommand("@Coconut /assign 10 bench-workbuddy")).toEqual({
      kind: "assign",
      issue: 10,
      agentId: "bench-workbuddy",
    });
  });
});

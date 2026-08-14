import { describe, expect, it } from "vitest";
import { MessageDeduper } from "./dedupe.js";

describe("MessageDeduper", () => {
  it("accepts one delivery and rejects a retry", () => {
    const deduper = new MessageDeduper();
    expect(deduper.accept("message-1")).toBe(true);
    expect(deduper.accept("message-1")).toBe(false);
  });

  it("evicts old message IDs", () => {
    const deduper = new MessageDeduper(1);
    expect(deduper.accept("message-1")).toBe(true);
    expect(deduper.accept("message-2")).toBe(true);
    expect(deduper.accept("message-1")).toBe(true);
  });
});

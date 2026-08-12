import * as lark from "@larksuiteoapi/node-sdk";
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { parseCommand } from "./commands.js";
import { GhCliGitHub } from "./github.js";
import { CoordinatorService } from "./service.js";
import { rememberChatId } from "./state.js";
import type { Language } from "./types.js";

const appId = process.env.LARK_APP_ID;
const appSecret = process.env.LARK_APP_SECRET;
if (!appId || !appSecret) {
  throw new Error(
    "LARK_APP_ID and LARK_APP_SECRET must be configured in the process environment",
  );
}

const repo = process.env.GITHUB_REPO ?? "finnyoun9/agent-collab-hub";
const lang: Language = process.env.COLLAB_LANG === "en" ? "en" : "zh";
const windowsGh = "C:\\Program Files\\GitHub CLI\\gh.exe";
const ghPath =
  process.env.GH_PATH ?? (process.platform === "win32" && existsSync(windowsGh) ? windowsGh : "gh");
const statePath = resolve(process.cwd(), ".state", "coordinator.json");
const service = new CoordinatorService(new GhCliGitHub(repo, ghPath), lang);

const client = new lark.Client({
  appId,
  appSecret,
  appType: lark.AppType.SelfBuild,
  domain: lark.Domain.Feishu,
});

const eventDispatcher = new lark.EventDispatcher({}).register({
  "im.message.receive_v1": async (data) => {
    const message = data.message;
    const chatId = message.chat_id;
    if (!chatId || !message.content || message.message_type !== "text") return;

    const content = JSON.parse(message.content) as { text?: string };
    if (!content.text) return;
    await rememberChatId(statePath, chatId);

    let reply: string;
    try {
      reply = await service.execute(parseCommand(content.text));
    } catch (error) {
      reply = `${lang === "zh" ? "处理失败" : "Failed"}: ${(error as Error).message}`;
    }

    await client.im.message.create({
      params: { receive_id_type: "chat_id" },
      data: {
        receive_id: chatId,
        msg_type: "text",
        content: JSON.stringify({ text: reply }),
      },
    });
  },
});

const wsClient = new lark.WSClient({
  appId,
  appSecret,
  domain: lark.Domain.Feishu,
  loggerLevel: lark.LoggerLevel.info,
});

console.log(`Agent Hub starting for ${repo}; waiting for Feishu messages...`);
await wsClient.start({ eventDispatcher });

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname } from "node:path";

interface State {
  chatId?: string;
}

export async function rememberChatId(path: string, chatId: string): Promise<void> {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, `${JSON.stringify({ chatId } satisfies State, null, 2)}\n`, {
    encoding: "utf8",
  });
}

export async function readChatId(path: string): Promise<string | undefined> {
  try {
    const state = JSON.parse(await readFile(path, "utf8")) as State;
    return state.chatId;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return undefined;
    throw error;
  }
}

# Bench 飞书协调器

当前版本负责：

- 通过飞书 WebSocket 长连接接收专项群消息；
- 创建、查询和分配 GitHub Issue；
- 记住首个有效消息的群 `chat_id`，只保存在忽略的 `.state/`；
- 用 GitHub 保存唯一可信任务状态。

当前版本不会自动操作 WorkBuddy、Codex Desktop 或 Claude 客户端。

## 安全配置

先在飞书开放平台重置已经暴露过的 App Secret。新 Secret 只写入 Windows 用户环境变量：

```powershell
[Environment]::SetEnvironmentVariable("LARK_APP_ID", "<app-id>", "User")
[Environment]::SetEnvironmentVariable("LARK_APP_SECRET", "<new-secret>", "User")
```

不要把真实值写进 `.env`、Issue、Git、终端参数或聊天消息。

## 安装和验证

```powershell
cd D:\Project\agent-collab-hub\coordinator
& 'C:\Users\yyfxy\AppData\Local\hermes\node\npm.cmd' install
& 'C:\Users\yyfxy\AppData\Local\hermes\node\npm.cmd' run check
```

## 飞书后台

1. 开启机器人能力。
2. 在“事件与回调 → 事件配置”选择长连接。
3. 订阅 `im.message.receive_v1`。
4. 发布应用版本。
5. 把机器人加入专项群。

卡片按钮会在后续版本使用 `card.action.trigger`；当前 MVP 先用文本指令验证主链路。

## 启动

```powershell
cd D:\Project\agent-collab-hub\coordinator
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

看到下面输出表示正在等待飞书事件：

```text
Agent Hub starting for finnyoun9/agent-collab-hub; waiting for Feishu messages...
```

## 群内命令

在群里 @机器人 后发送：

```text
/help
/task <目标>
/queue
/status <issue 编号>
/assign <issue 编号> <agent-id>
```

例如：

```text
@Agent Hub /task 验证 UART circular DMA 是否丢字节
@Agent Hub /assign 4 bench-workbuddy
```

分配给 WorkBuddy 后，你仍然需要打开 WorkBuddy，把 Issue URL 交给它，并在客户端里处理权限确认。
